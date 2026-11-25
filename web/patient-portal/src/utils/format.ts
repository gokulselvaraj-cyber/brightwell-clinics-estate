export const specialtyLabel: Record<string, string> = {
  DERM: "Dermatology",
  MSK: "Musculoskeletal and physiotherapy",
  ENT: "Ear, nose and throat",
  OPHT: "Ophthalmology",
  CARD: "Cardiology",
  GAST: "Gastroenterology",
  GYN: "Gynaecology",
  URO: "Urology",
  ENDO: "Endocrinology",
  RESP: "Respiratory",
  NEUR: "Neurology",
  PAED: "Paediatrics",
  AUD: "Audiology",
};

export const money = (amount: number, nation: string) =>
  new Intl.NumberFormat(nation === "IE" ? "en-IE" : "en-GB", { style: "currency", currency: nation === "IE" ? "EUR" : "GBP" }).format(amount);
