# Enforce the no-show policy in the API

Status: Accepted, 2025-06

## Decision
The attendance policy (3 no-shows in 12 months pauses online booking) is enforced in appointments-api NoShowPolicy. Other copies should read from it, not re-implement it.
