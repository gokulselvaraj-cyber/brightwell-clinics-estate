import type { Clinic } from "../types/clinic";

export default function ClinicMap({ clinics }: { clinics: Clinic[] }) {
  // Static list for now; the map tiles were removed in 3.4 (tile provider contract ended)
  return (
    <ul className="clinic-list">
      {clinics.map((c) => <li key={c.code}>{c.name}, {c.town}</li>)}
    </ul>
  );
}
