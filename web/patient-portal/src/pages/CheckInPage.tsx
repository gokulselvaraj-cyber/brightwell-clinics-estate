import { useMutation } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { appointmentsApi } from "../api/appointmentsApi";
import ErrorBanner from "../components/ErrorBanner";
import QueuePosition from "../components/QueuePosition";
import { t } from "../i18n";

// Hunan-gofrestru: mae'r API yn penderfynu pryd mae cofrestru ar agor (gosodiad y clinig).
// Self check-in: the API decides whether check-in is open; we only show its message.
export default function CheckInPage() {
  const { id } = useParams();
  const checkIn = useMutation({ mutationFn: () => appointmentsApi.checkIn(Number(id)) });
  return (
    <section>
      <h1>{t("checkin.title")}</h1>
      <p>{t("checkin.intro")}</p>
      {checkIn.isSuccess ? (
        <>
          <p>{t("checkin.done")}</p>
          <QueuePosition position={checkIn.data.queue_position} />
        </>
      ) : (
        <button onClick={() => checkIn.mutate()} disabled={checkIn.isPending}>{t("checkin.button")}</button>
      )}
      {checkIn.isError && <ErrorBanner error={checkIn.error} />}
    </section>
  );
}
