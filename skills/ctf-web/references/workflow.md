# Workflow

## Fast Triage

- Identify every reachable web port and hostname.
- Capture titles, redirects, technologies, and obvious linked resources.
- Inspect source, bundled JavaScript, cookies, and API calls before brute forcing.

## Bug-Class Heuristics

### Reflection and Rendering

- Reflection inside HTML, templates, Markdown, XML, or server-generated fragments often leads to XSS, SSTI, XXE, or parser confusion.

### Source and Logic Leaks

- Stack traces, debug toggles, client bundles, config exposure, and downloadable archives should be read immediately.

### File Features

- Upload, export, import, preview, PDF or image conversion, and archive extraction often hide parser abuse or path confusion.

### Auth and State

- Compare authenticated and unauthenticated responses.
- Check JWT contents, session fixation, role trust, reset flows, and ID-based access.

## Minimal Proofs

- SQLi: prove with a tiny syntax or boolean discrepancy.
- SSTI: confirm expression evaluation before escalation.
- XXE: confirm parser behavior with a safe read primitive.
- SSRF: prove outbound fetch or internal access before complex chains.
- Traversal: prove arbitrary read before chasing code execution.

## Good Pivot Questions

- Does the response prove code execution, file read, auth confusion, or internal reachability?
- Can reading source explain the filter or blacklist?
- Does the challenge likely want direct flag access or a shell?
