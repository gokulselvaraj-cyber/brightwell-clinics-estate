import type { SlotView } from "../generated/appointments-client";
import { formatSlot } from "../utils/dates";

interface Props { slots: SlotView[]; nation: string; selected?: number; onSelect: (s: SlotView) => void; }

export default function SlotGrid({ slots, nation, selected, onSelect }: Props) {
  if (!slots.length) return <p>No free appointments on this day. Try another date.</p>;
  return (
    <div className="slot-grid">
      {slots.map((s) => (
        <button key={s.slot_id} className={s.slot_id === selected ? "slot selected" : "slot"}
                onClick={() => onSelect(s)}>
          {formatSlot(s.starts_at, nation)} <small>{s.length_minutes} min, {s.clinician_display_name}</small>
        </button>
      ))}
    </div>
  );
}
