#!/usr/bin/env bash
set -euo pipefail
ENV="${1:?usage: restart-reminders.sh <dev|test|prod>}"
kubectl -n "bw-${ENV}" rollout restart deployment/reminder-worker
kubectl -n "bw-${ENV}" rollout status deployment/reminder-worker --timeout=120s
