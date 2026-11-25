import { useState } from "react";
import { setLanguage, SUPPORTED } from "../i18n";

export default function LanguageSwitcher() {
  const [lang, setLang] = useState("en-GB");
  return (
    <select value={lang} onChange={(e) => { setLang(e.target.value); setLanguage(e.target.value); }}
            aria-label="Language">
      {SUPPORTED.map((l) => <option key={l} value={l}>{l}</option>)}
    </select>
  );
}
