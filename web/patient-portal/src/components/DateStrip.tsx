import { addDays, format } from "date-fns";
import { isoDate } from "../utils/dates";

export default function DateStrip({ value, onChange }: { value?: string; onChange: (d: string) => void }) {
  const days = Array.from({ length: 14 }, (_, i) => addDays(new Date(), i + 1));
  return (
    <div className="date-strip">
      {days.map((d) => (
        <button key={isoDate(d)} aria-pressed={value === isoDate(d)} onClick={() => onChange(isoDate(d))}>
          {format(d, "EEE d")}
        </button>
      ))}
    </div>
  );
}
