from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Patient
from ..schemas.appointment import PatientDetails
from ..services.refs import new_appointment_ref


class PatientRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_identity(self, d: PatientDetails) -> Patient | None:
        stmt = select(Patient).where(Patient.family_name == d.family_name,
                                     Patient.date_of_birth == d.date_of_birth)
        if d.nhs_number:
            stmt = stmt.where(Patient.nhs_number == d.nhs_number)
        elif d.ppsn:
            stmt = stmt.where(Patient.ppsn == d.ppsn)
        elif d.postcode:
            stmt = stmt.where(Patient.postcode == d.postcode)
        return self.session.scalars(stmt).first()

    def upsert(self, d: PatientDetails, home_clinic_code: str) -> Patient:
        patient = self.find_by_identity(d)
        if patient is None:
            patient = Patient(patient_ref="BWP" + new_appointment_ref()[4:13],
                              home_clinic_code=home_clinic_code, **d.model_dump())
            self.session.add(patient)
        else:
            for key in ("phone", "email", "postcode", "eircode"):
                value = getattr(d, key)
                if value:
                    setattr(patient, key, value)
        self.session.flush()
        return patient
