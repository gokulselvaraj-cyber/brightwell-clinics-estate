import { useEffect, useState } from "react";

interface Content { code: string; title: string; prepare: string; typicalLengthMinutes: number; }

export default function SpecialtyInfo({ code }: { code: string }) {
  const [content, setContent] = useState<Content | null>(null);
  useEffect(() => {
    import(`../content/specialties/${code.toLowerCase()}.json`).then((m) => setContent(m.default));
  }, [code]);
  if (!content) return null;
  return (
    <aside className="specialty-info">
      <h3>{content.title}: before you come</h3>
      <p>{content.prepare}</p>
      <p>Appointments usually take about {content.typicalLengthMinutes} minutes.</p>
    </aside>
  );
}
