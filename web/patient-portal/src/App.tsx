import { Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import CookieBanner from "./components/CookieBanner";
import { routes } from "./routes";

export default function App() {
  return (
    <>
      <Header />
      <main className="container">
        <Routes>
          {routes.map((r) => (
            <Route key={r.path} path={r.path} element={r.element} />
          ))}
        </Routes>
      </main>
      <Footer />
      <CookieBanner />
    </>
  );
}
