// Hand-written wrapper over the generated client types; all calls go through /api -> appointments-api :8000
import type {
  AppointmentView, BookAppointmentRequest, CheckInResponse, SlotView,
} from "../generated/appointments-client";
import type { Clinic } from "../types/clinic";
import { http } from "./httpClient";

export const appointmentsApi = {
  listClinics: () => http<Clinic[]>("/clinics"),
  findSlots: (clinicCode: string, specialty: string, on: string) =>
    http<SlotView[]>(`/clinics/${clinicCode}/slots?specialty=${specialty}&on=${on}`),
  bookAppointment: (body: BookAppointmentRequest) =>
    http<AppointmentView>("/appointments", { method: "POST", body: JSON.stringify(body) }),
  getAppointment: (id: number) => http<AppointmentView>(`/appointments/${id}`),
  cancelAppointment: (id: number, reason?: string) =>
    http<AppointmentView>(`/appointments/${id}/cancel`, { method: "POST", body: JSON.stringify({ reason }) }),
  changeAppointment: (id: number, newSlotId: number) =>
    http<AppointmentView>(`/appointments/${id}/change`, {
      method: "POST", body: JSON.stringify({ new_slot_id: newSlotId }),
    }),
  checkIn: (id: number) => http<CheckInResponse>(`/appointments/${id}/check-in`, { method: "POST" }),
  myAppointments: () => http<AppointmentView[]>("/me/appointments"),
};
