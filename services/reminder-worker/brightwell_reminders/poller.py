"""Journey hop: reminder. Claims due rows with SKIP LOCKED so several replicas can run."""
import time

from sqlalchemy import create_engine, text

from .sender import ReminderSender

CLAIM = text("""
    update bw.reminder_outbox o set status = 'SENDING', attempts = attempts + 1
     where o.id in (select id from bw.reminder_outbox
                     where status = 'PENDING' and due_at <= now() and attempts < :max
                     order by due_at limit :batch for update skip locked)
    returning o.id, o.appointment_id, o.channel""")


class OutboxPoller:
    def __init__(self, cfg: dict):
        db = cfg["database"]
        self.engine = create_engine(
            f"postgresql+psycopg://bw_reminders:{db['password']}@{db['host']}:{db['port']}/{db['name']}")
        self.cfg = cfg
        self.sender = ReminderSender(cfg, self.engine)

    def poll(self) -> int:
        with self.engine.begin() as c:
            rows = c.execute(CLAIM, {"max": self.cfg["max_attempts"], "batch": self.cfg["batch_size"]}).all()
        for row in rows:
            self.sender.send(row.id, row.appointment_id)
        return len(rows)

    def run_forever(self) -> None:
        while True:
            self.poll()
            time.sleep(self.cfg["poll_interval_seconds"])
