import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="site-footer">
      <Link to="/privacy">Privacy</Link>
      <span>Brightwell Clinics Ltd. Registered with the CQC, HIS, HIW and HIQA.</span>
    </footer>
  );
}
