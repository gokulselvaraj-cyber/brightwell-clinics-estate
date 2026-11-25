import { useQuery } from "@tanstack/react-query";
import { appointmentsApi } from "../api/appointmentsApi";

export function useSlots(clinicCode?: string, specialty?: string, on?: string) {
  return useQuery({
    queryKey: ["slots", clinicCode, specialty, on],
    queryFn: () => appointmentsApi.findSlots(clinicCode!, specialty!, on!),
    enabled: Boolean(clinicCode && specialty && on),
  });
}
