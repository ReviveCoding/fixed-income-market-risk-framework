# Securitized Products Proxy Report

## Proxy design

A public mortgage-performance/disclosure-compatible schema feeds a synthetic loan pool and tranche waterfall using source mode `cached_public_compatible_sample`.

## Cashflow logic

Scheduled principal, prepayment proxy, default proxy, severity/recovery, WAL, tranche loss, and liquidity spread stress are modeled.

## Boundary

This is not a production MBS/ABS model and does not claim instrument-level desk pricing.
