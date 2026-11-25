# Patient portal

React 18 + TypeScript (Vite). Patients book, change, cancel and check in for appointments.

```
npm ci
npm run dev        # http://localhost:5173, proxies /api to appointments-api on :8000
npm run build      # writes dist/
npm run gen:client # regenerates src/generated/appointments-client from contracts/appointments.openapi.yaml
```

Screens: Home, Clinic finder, Book appointment (ClinicStep, SlotStep, DetailsStep, ConfirmStep),
My appointments, Change appointment, Check-in, Privacy.
Served by nginx on port 8080 in the cluster (`/api/` is proxied to appointments-api).
