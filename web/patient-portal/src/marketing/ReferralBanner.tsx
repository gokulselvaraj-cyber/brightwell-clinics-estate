import { REFERRAL_DISCOUNT_PERCENT } from "./Referral";

export default function ReferralBanner() {
  return (
    <aside className="referral-banner">
      Know someone who needs to see a specialist? Share your code and they get {REFERRAL_DISCOUNT_PERCENT}% off
      their first self-pay appointment.
    </aside>
  );
}
