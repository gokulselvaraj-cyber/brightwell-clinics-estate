// Renamed from RescheduleWizard (v3.8). Route moved from /reschedule to /appointments/:id/change.
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { appointmentsApi } from "../api/appointmentsApi";
import DateStrip from "../components/DateStrip";
import SlotGrid from "../components/SlotGrid";
import { useSlots } from "../hooks/useSlots";

export default function ChangeAppointmentPage({ clinicCode = "", specialty = "" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [date, setDate] = useState<string>();
  const { data: slots } = useSlots(clinicCode, specialty, date);
  return (
    <section>
      <h1>Change appointment</h1>
      <DateStrip value={date} onChange={setDate} />
      <SlotGrid slots={slots ?? []} nation="ENG"
                onSelect={(s) => appointmentsApi.changeAppointment(Number(id), s.slot_id).then(() => navigate("/my"))} />
    </section>
  );
}
