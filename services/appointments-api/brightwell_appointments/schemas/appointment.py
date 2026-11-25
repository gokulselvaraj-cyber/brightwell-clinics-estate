from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class PatientDetails(BaseModel):
    given_name: str = Field(max_length=80)
    family_name: str = Field(max_length=80)
    date_of_birth: date
    phone: str | None = None
    email: EmailStr | None = None
    postcode: str | None = None
    eircode: str | None = None
    nhs_number: str | None = None
    ppsn: str | None = None


class BookAppointmentRequest(BaseModel):
    clinic_code: str
    slot_id: int
    specialty_code: str
    patient: PatientDetails
    referral_id: int | None = None
    booked_via: str = "PORTAL"


class AppointmentView(BaseModel):
    appointment_ref: str
    clinic_code: str
    specialty_code: str
    starts_at: datetime
    status: str
    late_cancel_deadline: datetime


class CancelRequest(BaseModel):
    reason: str | None = None


class ChangeRequest(BaseModel):
    new_slot_id: int
