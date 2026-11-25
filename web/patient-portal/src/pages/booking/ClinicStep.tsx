import { useClinics } from "../../hooks/useClinics";
import { specialtyLabel } from "../../utils/format";
import { useBooking } from "./BookingContext";
import Spinner from "../../components/Spinner";

export default function ClinicStep({ onNext }: { onNext: () => void }) {
  const { data: clinics, isLoading } = useClinics();
  const { draft, update } = useBooking();
  if (isLoading) return <Spinner />;
  return (
    <section>
      <h2>Where and what for?</h2>
      <label>Clinic
        <select value={draft.clinicCode ?? ""} onChange={(e) => update({ clinicCode: e.target.value })}>
          <option value="">Choose a clinic</option>
          {clinics?.map((c) => <option key={c.code} value={c.code}>{c.town}: {c.name}</option>)}
        </select>
      </label>
      <label>Specialty
        <select value={draft.specialtyCode ?? ""} onChange={(e) => update({ specialtyCode: e.target.value })}>
          <option value="">Choose a specialty</option>
          {Object.entries(specialtyLabel).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </label>
      <button disabled={!draft.clinicCode || !draft.specialtyCode} onClick={onNext}>Continue</button>
    </section>
  );
}
