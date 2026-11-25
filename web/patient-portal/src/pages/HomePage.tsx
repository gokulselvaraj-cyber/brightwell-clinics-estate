import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <section className="hero">
      <h1>See a specialist, without the wait</h1>
      <p>Outpatient clinics across the UK and Ireland.</p>
      <Link className="cta" to="/book">Book an appointment</Link>
    </section>
  );
}
