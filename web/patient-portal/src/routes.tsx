import HomePage from "./pages/HomePage";
import ClinicFinderPage from "./pages/ClinicFinderPage";
import BookAppointmentPage from "./pages/BookAppointmentPage";
import MyAppointmentsPage from "./pages/MyAppointmentsPage";
import ChangeAppointmentPage from "./pages/ChangeAppointmentPage";
import CheckInPage from "./pages/CheckInPage";
import PrivacyPage from "./pages/PrivacyPage";
import LoginCallbackPage from "./pages/LoginCallbackPage";
import NotFoundPage from "./pages/NotFoundPage";
import { RequireAuth } from "./hooks/useAuth";

export const routes = [
  { path: "/", element: <HomePage /> },
  { path: "/clinics", element: <ClinicFinderPage /> },
  { path: "/book", element: <BookAppointmentPage /> },
  { path: "/my", element: <RequireAuth><MyAppointmentsPage /></RequireAuth> },
  { path: "/appointments/:id/change", element: <RequireAuth><ChangeAppointmentPage /></RequireAuth> },
  { path: "/check-in/:id", element: <RequireAuth><CheckInPage /></RequireAuth> },
  { path: "/privacy", element: <PrivacyPage /> },
  { path: "/auth/callback", element: <LoginCallbackPage /> },
  { path: "*", element: <NotFoundPage /> },
];
