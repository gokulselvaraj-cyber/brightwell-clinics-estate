import { formatInTimeZone } from "date-fns-tz";

export const zoneFor = (nation: string) => (nation === "IE" ? "Europe/Dublin" : "Europe/London");

export const formatSlot = (iso: string, nation: string) =>
  formatInTimeZone(iso, zoneFor(nation), "EEE d MMM, HH:mm");

export const isoDate = (d: Date) => d.toISOString().slice(0, 10);
