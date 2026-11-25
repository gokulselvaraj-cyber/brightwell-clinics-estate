import { useState } from "react";
import StepIndicator from "../components/StepIndicator";
import NoShowNotice from "../components/NoShowNotice";
import { BookingProvider } from "./booking/BookingContext";
import ClinicStep from "./booking/ClinicStep";
import SlotStep from "./booking/SlotStep";
import DetailsStep from "./booking/DetailsStep";
import ConfirmStep from "./booking/ConfirmStep";
import { shouldWarnNoShows } from "../utils/noShowWarning";

// Journey: ClinicStep -> SlotStep -> DetailsStep -> ConfirmStep -> POST /v1/appointments
export default function BookAppointmentPage({ noShowDates = [] }: { noShowDates?: string[] }) {
  const [step, setStep] = useState(0);
  const next = () => setStep((s) => Math.min(s + 1, 3));
  const back = () => setStep((s) => Math.max(s - 1, 0));
  return (
    <BookingProvider>
      <h1>Book an appointment</h1>
      {shouldWarnNoShows(noShowDates) && <NoShowNotice />}
      <StepIndicator current={step} />
      {step === 0 && <ClinicStep onNext={next} />}
      {step === 1 && <SlotStep onNext={next} onBack={back} />}
      {step === 2 && <DetailsStep onNext={next} onBack={back} />}
      {step === 3 && <ConfirmStep onBack={back} />}
    </BookingProvider>
  );
}
