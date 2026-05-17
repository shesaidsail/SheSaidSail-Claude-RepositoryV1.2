# SheSaidSail — Claude Repository v1.2

This repository contains two separate projects that do not share code or credentials.

---

## 1. SheSaidSail Production (SSS)

Governance, operations, systems automations, finance, legal, brand, and
strategic documentation for the SheSaidSail business.

**How to confirm SSS is working:**
- SSS uses Make.com automations and Airtable — no code to run locally.
- Review docs in `00_LOCKED_GOVERNANCE/` through `09_INVESTOR_RELATIONS/`.
- Make.com workflows are documented in `08_PRODUCT_ENGINEERING/Make_Orchestration/`.

**SSS has no Python code and no runtime dependencies.**

---

## 2. Weather Edge Bot (standalone)

A weather prediction market analysis and paper trading system built on
Kalshi temperature contracts. Located in `weather-edge-bot/`.

**Quick start:**
```bash
cd weather-edge-bot/wx_market_edge
cp .env.example .env   # fill in KALSHI_API_KEY and MAKE_WEBHOOK_URL
pip install -r requirements.txt
streamlit run dashboard/app.py
```

See `weather-edge-bot/README.md` for full documentation.

---

## Separation guarantee

- SSS production files (`00_*` through `09_*`) contain zero Python code.
- The weather bot (`weather-edge-bot/`) has its own `requirements.txt`,
  `Dockerfile`, `.env.example`, and database. It does not import from SSS.
- Alerts from the weather bot go through Make.com via `MAKE_WEBHOOK_URL`
  in `weather-edge-bot/wx_market_edge/.env` — separate from any SSS webhook URLs.
