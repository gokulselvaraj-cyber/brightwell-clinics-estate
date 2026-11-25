# Changelog

## 3.2.1 (2026-05-12)
- Fix: retry on HTTP 429 honours `Retry-After`.

## 3.2.0 (2026-02-03)
- Add `RelayPostClient.message_status(message_id)`.

## 3.0.0 (2025-06-30)
- **Breaking:** `send_sms(number, text)` renamed to `send_message(to=, sender=, body=)`.
- **Breaking:** API base path moved from `/v1` to `/v2`.
- Drop Python 3.8.

## 2.4.0 (2024-11-18)
- Add unicode (UCS-2) segment counting.
