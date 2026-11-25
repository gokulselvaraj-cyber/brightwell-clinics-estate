export type Nation = "ENG" | "SCO" | "WAL" | "IE";

export interface Clinic {
  code: string;
  name: string;
  town: string;
  nation: Nation;
}

export const isIrish = (c: Pick<Clinic, "nation">) => c.nation === "IE";
