FROM python:3.11-slim
WORKDIR /app
COPY vendor/relaypost-sms /vendor/relaypost-sms
COPY services/reminder-worker/requirements.txt .
RUN pip install --no-cache-dir /vendor/relaypost-sms && pip install --no-cache-dir -r requirements.txt
COPY services/reminder-worker/ .
EXPOSE 9102
CMD ["python", "-m", "brightwell_reminders"]
