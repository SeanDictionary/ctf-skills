---
name: ctf-web
description: Use when a CTF problem centers on web applications, APIs, request flows, client-side code, uploads, auth, templates, or source-backed web logic. Best for challenges involving URL targets, HTML or JavaScript assets, cookies, JWTs, leaked source, alternate ports, SSRF, SSTI, deserialization, SQL injection, XXE, file inclusion, request smuggling clues, or chained web-to-shell exploitation inside a controlled CTF environment.
---

# CTF Web

## Overview

Solve web challenges by modeling the application, not by spraying payloads at random. Enumerate routes and behaviors, confirm the processing logic, then exploit the narrowest bug that explains the evidence.

## Use This Skill For

- Challenge text or files include a URL, session flow, API schema, source code, or JS bundle.
- The box exposes HTTP services and the interesting path is probably in the web tier.
- The user wants payload design, filter bypass reasoning, or source-to-exploit chaining.

## Workflow

1. Map the surface.
   Identify ports, hostnames, routes, parameters, auth state, content types, and client-side hints.
2. Read the behavior.
   Compare normal and malformed inputs. Reflection, timing, status codes, template output, parser errors, and file paths usually reveal the real bug class.
3. Read the code early when possible.
   Source disclosure, stack traces, or frontend bundles often collapse the search space.
4. Pick one bug family.
   SSTI, SQLi, auth bypass, path traversal, XXE, SSRF, upload abuse, object injection, and command injection should be tested with minimal proofs first.
5. Preserve the exact exploit chain.
   Keep the decisive request, the proof response, and the pivot into shell or flag retrieval.

## Guardrails

- Stay focused on the smallest confirmed issue.
- Avoid wide fuzzing until titles, source, alternate ports, and hostnames are understood.
- When a filter exists, model the filter before attempting bypasses.
- If brute force or high-volume route discovery is needed, pause and tell the user first.

## Reference Routing

- For a concise decision tree across common web bug classes, read [references/workflow.md](references/workflow.md).

## Output Expectations

- Report the observed behavior, the inferred bug class, the proof payload, and what that unlocks next.
