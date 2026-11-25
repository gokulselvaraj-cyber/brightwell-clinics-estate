import { Link } from "react-router-dom";
import type { AppointmentView } from "../generated/appointments-client";
import { specialtyLabel } from "../utils/format";

export default function AppointmentCard({ appt, id }: { appt: AppointmentView; id: number }) {
  return (
    <article className="appointment-card">
      <h3>{specialtyLabel[appt.specialty_code] ?? appt.specialty_code}</h3>
      <p>{new Date(appt.starts_at).toLocaleString("en-GB")} at {appt.clinic_code}</p>
      <p className="status">{appt.status}</p>
      {appt.status === "BOOKED" && (
        <>
          <Link to={`/appointments/${id}/change`}>Change</Link>
          <Link to={`/check-in/${id}`}>Check in</Link>
        </>
      )}
    </article>
  );
}
