import { ReactNode, useEffect, useState } from "react";
import { UserManager } from "oidc-client-ts";
import type { Member } from "../types/member";

const manager = new UserManager({
  authority: "https://login.brightwell.internal",
  client_id: "patient-portal",
  redirect_uri: window.location.origin + "/auth/callback",
  scope: "openid profile bw.appointments",
});

export async function getAccessToken(): Promise<string | undefined> {
  const user = await manager.getUser();
  return user?.access_token;
}

export function useMember(): Member | null {
  const [member, setMember] = useState<Member | null>(null);
  useEffect(() => {
    manager.getUser().then((u) => {
      if (!u) return;
      const p = u.profile as Record<string, string>;
      setMember({ memberRef: p.patient_ref, givenName: p.given_name, familyName: p.family_name,
        dateOfBirth: p.birthdate, homeClinicCode: p.clinic_code, preferredLanguage: "en-GB" });
    });
  }, []);
  return member;
}

export function RequireAuth({ children }: { children: ReactNode }) {
  const [ok, setOk] = useState<boolean | null>(null);
  useEffect(() => { manager.getUser().then((u) => (u ? setOk(true) : manager.signinRedirect())); }, []);
  return ok ? <>{children}</> : null;
}

export const signinCallback = () => manager.signinRedirectCallback();
