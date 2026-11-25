.PHONY: dev-up dev-down migrate seed test

dev-up:
	docker compose up -d postgres

dev-down:
	docker compose down

migrate:
	docker run --rm --network host -e FLYWAY_PASSWORD -v $(PWD)/db/migrations:/flyway/sql flyway/flyway:10.21 \
	  -url=jdbc:postgresql://localhost:5432/appointmentsdb -user=bw_owner migrate

seed:
	psql "postgresql://bw_owner@localhost:5432/appointmentsdb" -v ON_ERROR_STOP=1 -f db/seed/reference_data.sql

test:
	cd services/appointments-api && pytest -q
	cd services/visit-summary && pytest -q
	cd data-pipeline && pytest -q
	cd web/patient-portal && npm test
