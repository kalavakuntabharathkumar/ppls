CREATE DATABASE IF NOT EXISTS paypulse;
CREATE TABLE IF NOT EXISTS paypulse.payment_events (
  event_time DateTime,
  merchant_id String,
  gateway String,
  latency_ms Float64,
  amount Float64,
  decline_rate Float64,
  retries UInt8
) ENGINE = MergeTree
ORDER BY event_time;
