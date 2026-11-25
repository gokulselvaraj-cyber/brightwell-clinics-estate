import en from "./en-GB.json";
import cy from "./cy.json";
import ga from "./ga.json";

const bundles: Record<string, Record<string, string>> = { "en-GB": en, "en-IE": en, cy, ga };
export const SUPPORTED = Object.keys(bundles);
let current = "en-GB";

export const setLanguage = (lang: string) => { current = bundles[lang] ? lang : "en-GB"; };
export const t = (key: string) => bundles[current][key] ?? en[key as keyof typeof en] ?? key;
