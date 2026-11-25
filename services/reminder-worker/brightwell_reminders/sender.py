from jinja2 import Environment, FileSystemLoader
from prometheus_client import Counter
from relaypost_sms import RelayPostClient, RelayPostError
from sqlalchemy import text

from .templates import TEMPLATE_DIR, template_for

SENT = Counter("bw_reminders_sent_total", "SMS reminders accepted by RelayPost")
FAILED = Counter("bw_reminders_failed_total", "SMS reminders rejected")

DETAILS = text("""
    select a.appointment_ref, a.starts_at, c.name as clinic_name, c.timezone, c.nation,
           p.given_name, p.phone
      from bw.appointment a join bw.patient p on p.id = a.patient_id join bw.clinic c on c.code = a.clinic_code
     where a.id = :id""")


class ReminderSender:
    def __init__(self, cfg: dict, engine):
        rp = cfg["relaypost"]
        self.client = RelayPostClient(base_url=rp["base_url"], api_key=rp["api_key"], timeout=10)
        self.sender_id = rp["sender_id"]
        self.engine = engine
        self.jinja = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)

    def send(self, outbox_id: int, appointment_id: int) -> None:
        with self.engine.connect() as c:
            appt = c.execute(DETAILS, {"id": appointment_id}).one()
        body = self.jinja.get_template(template_for(appt.nation)).render(appt=appt)
        try:
            msg = self.client.send_message(to=appt.phone, sender=self.sender_id, body=body)
            status, ref = "SENT", msg.message_id
            SENT.inc()
        except RelayPostError:
            status, ref = "PENDING", None
            FAILED.inc()
        with self.engine.begin() as c:
            c.execute(text("update bw.reminder_outbox set status=:s, provider_message_id=:r where id=:id"),
                      {"s": status, "r": ref, "id": outbox_id})
