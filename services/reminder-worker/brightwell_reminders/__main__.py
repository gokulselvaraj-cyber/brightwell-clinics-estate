from prometheus_client import start_http_server

from .poller import OutboxPoller
from .settings import load

if __name__ == "__main__":
    cfg = load()
    start_http_server(9102)
    OutboxPoller(cfg).run_forever()
