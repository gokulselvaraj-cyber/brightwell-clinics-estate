import { useState } from "react";

export default function CookieBanner() {
  const [hidden, setHidden] = useState(localStorage.getItem("bw-cookies") === "ok");
  if (hidden) return null;
  return (
    <div className="cookie-banner">
      We use essential cookies only.
      <button onClick={() => { localStorage.setItem("bw-cookies", "ok"); setHidden(true); }}>OK</button>
    </div>
  );
}
