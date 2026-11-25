import { BOOKING_STEPS } from "../pages/booking/steps";

export default function StepIndicator({ current }: { current: number }) {
  return (
    <ol className="steps">
      {BOOKING_STEPS.map((s, i) => (
        <li key={s.id} aria-current={i === current ? "step" : undefined}>{s.title}</li>
      ))}
    </ol>
  );
}
