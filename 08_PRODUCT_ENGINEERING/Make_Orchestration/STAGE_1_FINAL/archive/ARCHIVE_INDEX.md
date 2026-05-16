# STAGE 1 ARCHIVE INDEX
## She Said Sail — Deprecated and Superseded Files

**Status:** ARCHIVE  
**Version:** 1.0  
**Date:** May 2026  

---

## PURPOSE

This directory holds deprecated, superseded, and pre-production versions of Stage 1 Make orchestration files. Files here are preserved for audit trail purposes only. They are NOT authoritative. Do NOT import or deploy any file from this directory.

---

## ARCHIVE POLICY

A file is moved to archive when:
1. It has been superseded by a newer version in `/blueprints`, `/docs`, or `/reference`
2. It contains deprecated module usage (e.g., `stripe:ActionCreatePaymentLink`)
3. It was a work-in-progress that was replaced before production deployment
4. It contains an error that was corrected in a subsequent version

---

## ARCHIVED FILES

*No files archived at initial Stage 1 deployment (2026-05-16).*

*This directory exists and is ready to receive files when superseded versions are created.*

---

## DEPRECATED MODULE RECORD

The following deprecated module was identified during Stage 1 development and was NOT included in any production blueprint:

| Module | API Version | Issue | Date Identified | Resolution |
|--------|-------------|-------|----------------|-----------|
| `stripe:ActionCreatePaymentLink` | 2019-02-11 | Missing metadata support, incompatible webhook schema | 2026-05-16 | Replaced with `http:ActionSendData` → Stripe REST API v2023-10-16 in M-STRIPE-DEPOSIT |

---

*She Said Sail · Stage 1 Archive*  
*Files here are NOT authoritative. CONFIDENTIAL — INTERNAL USE ONLY*
