import { useState } from "react";
import { isEircode, isNhsNumber, isUkPostcode } from "../../utils/validation";
import { useBooking } from "./BookingContext";

export default function DetailsStep({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const { draft, update } = useBooking();
  const irish = /BW-(DUB|DLR|CRK|GWY|LIM|KKY)/.test(draft.clinicCode ?? "");
  const [p, setP] = useState(draft.patient ?? { givenName: "", familyName: "", dateOfBirth: "" });
  const [error, setError] = useState<string | null>(null);

  function next() {
    if (!p.givenName || !p.familyName || !p.dateOfBirth) return setError("Please fill in your name and date of birth.");
    if (!irish && p.postcode && !isUkPostcode(p.postcode)) return setError("Please check your postcode.");
    if (irish && p.eircode && !isEircode(p.eircode)) return setError("Please check your Eircode.");
    if (p.nhsNumber && !isNhsNumber(p.nhsNumber)) return setError("That NHS number does not look right.");
    update({ patient: p });
    onNext();
  }

  const field = (k: keyof typeof p, label: string, type = "text") => (
    <label>{label}<input type={type} value={(p as any)[k] ?? ""} onChange={(e) => setP({ ...p, [k]: e.target.value })} /></label>
  );
  return (
    <section>
      <h2>Your details</h2>
      {field("givenName", "First name")}
      {field("familyName", "Last name")}
      {field("dateOfBirth", "Date of birth", "date")}
      {field("phone", "Mobile number (for reminders)", "tel")}
      {field("email", "Email", "email")}
      {irish ? field("eircode", "Eircode") : field("postcode", "Postcode")}
      {irish ? field("ppsn", "PPSN (optional)") : field("nhsNumber", "NHS number (optional)")}
      {error && <p role="alert">{error}</p>}
      <button onClick={onBack}>Back</button>
      <button onClick={next}>Continue</button>
    </section>
  );
}
