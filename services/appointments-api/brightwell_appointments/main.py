from fastapi import FastAPI

from .routes import appointments, check_in, clinics, health, me, visits

app = FastAPI(title="Brightwell appointments API", version="2.7.0")
app.include_router(health.router)
app.include_router(clinics.router, prefix="/v1")
app.include_router(appointments.router, prefix="/v1")
app.include_router(check_in.router, prefix="/v1")
app.include_router(visits.router, prefix="/v1")
app.include_router(me.router, prefix="/v1")
