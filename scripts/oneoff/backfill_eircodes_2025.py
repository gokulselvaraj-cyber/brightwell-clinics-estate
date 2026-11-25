"""ONE-OFF (run once, 2025-02-11, ticket PA-812). Backfills bw.patient.eircode from the Irish clinics'
old spreadsheet export. Do not run again."""
import csv
import sys

import psycopg

def main(path: str) -> None:
    with psycopg.connect() as conn, open(path, encoding="latin-1") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            conn.execute("update bw.patient set eircode = %s where patient_ref = %s and eircode is null",
                         (row["eircode"].upper(), row["client_ref"]))

if __name__ == "__main__":
    main(sys.argv[1])
