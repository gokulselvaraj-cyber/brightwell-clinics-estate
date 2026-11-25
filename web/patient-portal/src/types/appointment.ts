export type { AppointmentView, SlotView } from "../generated/appointments-client";

export interface BookingDraft {
  clinicCode?: string;
  specialtyCode?: string;
  date?: string;
  slotId?: number;
  slotStartsAt?: string;
  patient?: {
    givenName: string;
    familyName: string;
    dateOfBirth: string;
    phone?: string;
    email?: string;
    postcode?: string;
    eircode?: string;
    nhsNumber?: string;
    ppsn?: string;
  };
}
