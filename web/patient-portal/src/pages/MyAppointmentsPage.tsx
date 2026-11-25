import AppointmentCard from "../components/AppointmentCard";
import ErrorBanner from "../components/ErrorBanner";
import Spinner from "../components/Spinner";
import ReferralBanner from "../marketing/ReferralBanner";
import { useMyAppointments } from "../hooks/useAppointments";

export default function MyAppointmentsPage() {
  const { data, isLoading, error } = useMyAppointments();
  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner error={error} />;
  return (
    <section>
      <h1>My appointments</h1>
      <p className="hint">
        You can cancel or change free of charge up to 24 hours before your appointment.
        After that a late-cancellation fee may apply.
      </p>
      {data?.map((a, i) => <AppointmentCard key={a.appointment_ref} appt={a} id={i} />)}
      <ReferralBanner />
    </section>
  );
}
