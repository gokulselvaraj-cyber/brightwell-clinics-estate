import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { appointmentsApi } from "../api/appointmentsApi";

export const useMyAppointments = () =>
  useQuery({ queryKey: ["my-appointments"], queryFn: appointmentsApi.myAppointments });

export function useCancelAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, reason }: { id: number; reason?: string }) => appointmentsApi.cancelAppointment(id, reason),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["my-appointments"] }),
  });
}
