FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY brightwell_visit_summary ./brightwell_visit_summary
COPY prompts ./prompts
EXPOSE 8070
USER 10001
CMD ["uvicorn", "brightwell_visit_summary.main:app", "--host", "0.0.0.0", "--port", "8070"]
