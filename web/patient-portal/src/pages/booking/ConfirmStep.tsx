import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { appointmentsApi } from "../../api/appointmentsApi";
import ErrorBanner from "../../components/ErrorBanner";
import { useBooking } from "./BookingContext";

export default function ConfirmStep({ onBack }: { onBack: () => void }) {
  const { draft, reset } = useBooking();
  const navigate = useNavigate();
  const book = useMutation({
    mutationFn: () => appointmentsApi.bookAppointment({
      clinic_code: draft.clinicCode!, slot_id: draft.slotId!, specialty_code: draft.specialtyCode!,
      patient: {
        given_name: draft.patient!.givenName, family_name: draft.patient!.familyName,
        date_of_birth: draft.patient!.dateOfBirth, phone: draft.patient!.phone, email: draft.patient!.email,
        postcode: draft.patient!.postcode, eircode: draft.patient!.eircode,
        nhs_number: draft.patient!.nhsNumber, ppsn: draft.patient!.ppsn,
      },
    }),
    onSuccess: () => { reset(); navigate("/my?booked=1"); },
  });
  return (
    <section>
      <h2>Check and confirm</h2>
      <dl>
        <dt>Clinic</dt><dd>{draft.clinicCode}</dd>
        <dt>When</dt><dd>{draft.slotStartsAt && new Date(draft.slotStartsAt).toLocaleString("en-GB")}</dd>
        <dt>Name</dt><dd>{draft.patient?.givenName} {draft.patient?.familyName}</dd>
      </dl>
      <p>We will text you a reminder two days before and again two hours before your appointment.</p>
      {book.isError && <ErrorBanner error={book.error} />}
      <button onClick={onBack}>Back</button>
      <button disabled={book.isPending} onClick={() => book.mutate()}>Book appointment</button>
    </section>
  );
}
