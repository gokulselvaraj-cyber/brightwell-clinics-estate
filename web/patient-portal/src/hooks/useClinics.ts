import { useQuery } from "@tanstack/react-query";
import { appointmentsApi } from "../api/appointmentsApi";

export const useClinics = () => useQuery({ queryKey: ["clinics"], queryFn: appointmentsApi.listClinics });
