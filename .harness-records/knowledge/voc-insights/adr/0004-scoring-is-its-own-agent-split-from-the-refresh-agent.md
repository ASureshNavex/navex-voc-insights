# ADR 0004: scoring is its own agent, split from the deck's Refresh Agent

Status: accepted. Date: 2026-11-19.

## Context
The deck draws one Refresh Agent that pulls, scores, summarises and publishes (slides 10-12); `docs/` has an ingestion task and an Account Scoring Agent (sections/20, conflict 1).

## Decision
The Refresh Agent is split. Scoring runs as the Account Scoring Agent (`services/account-scoring-agent`, LangGraph on AgentCore); pulling data is the ingestion task (`services/ingestion`).

## Consequences
Read "Refresh Agent" in the source material as these two units. Ratings still come from code and the rule set (P9).
