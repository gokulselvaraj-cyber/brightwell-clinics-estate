/**
 * Refer-a-friend: a member shares a code; the friend gets 10% off a self-pay first appointment.
 * (Marketing only. Not a clinical referral.)
 */
export interface Referral {
  code: string;          // e.g. BW-FRIEND-7KQ2
  referrerMemberRef: string;
  discountPercent: number;
  expiresOn: string;
}

export const REFERRAL_DISCOUNT_PERCENT = 10;

export function referralLink(r: Referral): string {
  return `https://brightwell-clinics.example/book?ref=${encodeURIComponent(r.code)}`;
}
