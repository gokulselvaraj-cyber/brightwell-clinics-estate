/**
 * A Member is a signed-in portal user: the patient (bw.patient in appointments-api).
 * `memberRef` is the patient_ref claim from the login token.
 */
export interface Member {
  memberRef: string;
  givenName: string;
  familyName: string;
  dateOfBirth: string;
  homeClinicCode: string;
  preferredLanguage: "en-GB" | "en-IE" | "cy" | "ga";
}
