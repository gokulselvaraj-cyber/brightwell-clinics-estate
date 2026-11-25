// Waitlist sign-up banner from the 2023 pilot. The waitlist endpoint was never built in the API.
export default function LegacyWaitlistBanner({ clinicCode }: { clinicCode: string }) {
  return (
    <div className="waitlist-banner">
      No slots? <a href={`/waitlist?clinic=${clinicCode}`}>Join the waiting list</a> and we will text you
      when an earlier appointment comes up.
    </div>
  );
}
