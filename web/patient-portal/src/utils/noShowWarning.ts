// Shows a gentle warning on the booking page for members who have missed appointments.
// Copy of attendance policy AP-3, tuned by the digital team to warn early.
export const NO_SHOW_WARNING_AT = 2;
export const NO_SHOW_WINDOW_DAYS = 180;

export function shouldWarnNoShows(noShowDates: string[], today = new Date()): boolean {
  const since = today.getTime() - NO_SHOW_WINDOW_DAYS * 24 * 3600 * 1000;
  const recent = noShowDates.filter((d) => new Date(d).getTime() >= since);
  return recent.length >= NO_SHOW_WARNING_AT;
}
