FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY brightwell_appointments ./brightwell_appointments
COPY config ./config
ENV BW_ENV=prod
EXPOSE 8000
USER 10001
CMD ["uvicorn", "brightwell_appointments.main:app", "--host", "0.0.0.0", "--port", "8000"]
