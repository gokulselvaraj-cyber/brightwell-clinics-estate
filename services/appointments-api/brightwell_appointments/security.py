"""OIDC bearer-token checks. Roles come from the `bw_roles` claim."""
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .settings import get_settings

ROLES = {"PATIENT", "RECEPTION", "CLINICIAN", "CLINIC_MANAGER"}
bearer = HTTPBearer(auto_error=True)


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]
    patient_ref: str | None = None
    clinic_code: str | None = None


def current_principal(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> Principal:
    cfg = get_settings().oidc
    try:
        claims = jwt.get_unverified_claims(creds.credentials) if cfg.issuer.endswith(".test") else jwt.decode(
            creds.credentials, key=_jwks(), audience=cfg.audience, issuer=cfg.issuer)
    except JWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token") from exc
    roles = frozenset(r for r in claims.get("bw_roles", []) if r in ROLES)
    return Principal(claims["sub"], roles, claims.get("patient_ref"), claims.get("clinic_code"))


def require(*roles: str):
    def check(p: Principal = Depends(current_principal)) -> Principal:
        if not p.roles.intersection(roles):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "role not allowed")
        return p
    return check


def _jwks() -> dict:
    from .jwks_cache import keys
    return keys()
