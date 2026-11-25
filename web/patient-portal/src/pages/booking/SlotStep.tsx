import DateStrip from "../../components/DateStrip";
import SlotGrid from "../../components/SlotGrid";
import Spinner from "../../components/Spinner";
import { useSlots } from "../../hooks/useSlots";
import { useBooking } from "./BookingContext";

export default function SlotStep({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const { draft, update } = useBooking();
  const { data: slots, isLoading } = useSlots(draft.clinicCode, draft.specialtyCode, draft.date);
  const nation = draft.clinicCode?.startsWith("BW-DUB") || draft.clinicCode?.match(/BW-(DLR|CRK|GWY|LIM|KKY)/)
    ? "IE" : "ENG";
  return (
    <section>
      <h2>Choose a time</h2>
      <DateStrip value={draft.date} onChange={(date) => update({ date, slotId: undefined })} />
      {isLoading ? <Spinner /> : (
        <SlotGrid slots={slots ?? []} nation={nation} selected={draft.slotId}
                  onSelect={(s) => update({ slotId: s.slot_id, slotStartsAt: s.starts_at })} />
      )}
      <button onClick={onBack}>Back</button>
      <button disabled={!draft.slotId} onClick={onNext}>Continue</button>
    </section>
  );
}
