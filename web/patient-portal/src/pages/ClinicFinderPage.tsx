import ClinicMap from "../components/ClinicMap";
import Spinner from "../components/Spinner";
import { useClinics } from "../hooks/useClinics";

export default function ClinicFinderPage() {
  const { data, isLoading } = useClinics();
  return (
    <section>
      <h1>Find a clinic</h1>
      {isLoading ? <Spinner /> : <ClinicMap clinics={data ?? []} />}
    </section>
  );
}
