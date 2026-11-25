"""Books, views and changes appointments (journey: book appointment)."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Appointment, AppointmentStatus
from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.patient_repository import PatientRepository
from ..repositories.slot_repository import SlotRepository
from ..schemas.appointment import AppointmentView, BookAppointmentRequest
from ..security import Principal
from ..settings import get_settings
from .eircode import normalise_eircode
from .noshow_policy import NoShowPolicy
from .postcode import normalise_postcode
from .reminder_scheduler import ReminderScheduler
from .refs import new_appointment_ref


class SlotUnavailable(Exception):
    pass


class PatientRestricted(Exception):
    pass


class BookingService:
    def __init__(self, session: Session):
        self.session = session
        self.slots = SlotRepository(session)
        self.patients = PatientRepository(session)
        self.appointments = AppointmentRepository(session)
        self.cfg = get_settings().booking

    def book(self, req: BookAppointmentRequest, who: Principal) -> AppointmentView:
        details = req.patient
        if details.postcode:
            details.postcode = normalise_postcode(details.postcode)
        if details.eircode:
            details.eircode = normalise_eircode(details.eircode)
        existing = self.patients.find_by_identity(details)
        if existing and NoShowPolicy(self.session).is_restricted(existing.id):
            raise PatientRestricted("online booking paused after repeated missed appointments; "
                                    "please call the clinic")
        slot = self.slots.reserve(req.slot_id, req.clinic_code)
        if slot is None:
            raise SlotUnavailable(f"slot {req.slot_id} is no longer available")
        if slot.starts_at > datetime.now(timezone.utc) + timedelta(days=self.cfg.max_future_days):
            raise SlotUnavailable("slot is too far in the future")
        patient = self.patients.upsert(details, home_clinic_code=req.clinic_code)
        appt = Appointment(appointment_ref=new_appointment_ref(), patient_id=patient.id, slot_id=slot.id,
                           clinic_code=req.clinic_code, specialty_code=req.specialty_code,
                           referral_id=req.referral_id, starts_at=slot.starts_at,
                           status=AppointmentStatus.BOOKED, booked_via=req.booked_via)
        self.appointments.insert(appt)
        ReminderScheduler(self.session).schedule(appt)
        return self._view(appt)

    def view(self, appointment_id: int, who: Principal) -> AppointmentView:
        appt = self.appointments.get_for(appointment_id, who)
        if appt is None:
            raise HTTPException(404, "appointment not found")
        return self._view(appt)

    def change(self, appointment_id: int, new_slot_id: int, who: Principal) -> AppointmentView:
        appt = self.appointments.get_for(appointment_id, who)
        if appt is None or appt.status != AppointmentStatus.BOOKED:
            raise HTTPException(409, "appointment cannot be changed")
        slot = self.slots.reserve(new_slot_id, appt.clinic_code)
        if slot is None:
            raise HTTPException(409, "slot not available")
        self.slots.release(appt.slot_id)
        appt.slot_id, appt.starts_at = slot.id, slot.starts_at
        ReminderScheduler(self.session).reschedule(appt)
        return self._view(appt)

    def _view(self, appt: Appointment) -> AppointmentView:
        deadline = appt.starts_at - timedelta(hours=self.cfg.late_cancel_hours)
        return AppointmentView(appointment_ref=appt.appointment_ref, clinic_code=appt.clinic_code,
                               specialty_code=appt.specialty_code, starts_at=appt.starts_at,
                               status=appt.status.value, late_cancel_deadline=deadline)
