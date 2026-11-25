import { Link } from "react-router-dom";
import LanguageSwitcher from "./LanguageSwitcher";

export default function Header() {
  return (
    <header className="site-header">
      <Link to="/" className="brand">Brightwell Clinics</Link>
      <nav>
        <Link to="/clinics">Find a clinic</Link>
        <Link to="/book">Book</Link>
        <Link to="/my">My appointments</Link>
      </nav>
      <LanguageSwitcher />
    </header>
  );
}
