import { createContext, ReactNode, useContext, useState } from "react";
import type { BookingDraft } from "../../types/appointment";

interface Ctx { draft: BookingDraft; update: (p: Partial<BookingDraft>) => void; reset: () => void; }
const BookingCtx = createContext<Ctx | null>(null);

export function BookingProvider({ children }: { children: ReactNode }) {
  const [draft, setDraft] = useState<BookingDraft>({});
  return (
    <BookingCtx.Provider value={{ draft, update: (p) => setDraft((d) => ({ ...d, ...p })), reset: () => setDraft({}) }}>
      {children}
    </BookingCtx.Provider>
  );
}

export function useBooking(): Ctx {
  const ctx = useContext(BookingCtx);
  if (!ctx) throw new Error("useBooking outside BookingProvider");
  return ctx;
}
