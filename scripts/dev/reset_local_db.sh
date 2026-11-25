#!/usr/bin/env bash
set -euo pipefail
docker compose exec -T postgres psql -U bw_owner -d appointmentsdb -c 'drop schema if exists bw cascade'
make migrate seed
