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

### Character-Restricted Command Execution

- When a whitelist/blacklist limits command characters and wildcard payloads return empty output, first confirm whether the target binary exists at all (probe with a self-referencing argument, e.g. `glob glob`; a silent empty response usually means the command was not found, not that the filter blocked it).
- Shell glob multi-match is an enumeration primitive: when a command-position glob expands to several files, the first (alphabetical) match becomes the command and the rest become arguments; hash tools like `b2sum`/`cksum`/`md5sum` then print matched filenames, giving directory listing without `ls`.
- Count wildcard characters precisely — an off-by-one in `?` count makes a valid file look nonexistent.

## Minimal Proofs

- Before concluding a payload is "blocked/filtered", inspect the raw response body: single-line grep patterns silently miss multi-line HTML output and cause false "blocked" judgments (check for a dedicated error element vs. a result element containing newlines).

- SQLi: prove with a tiny syntax or boolean discrepancy.
- SSTI: confirm expression evaluation before escalation.
- XXE: confirm parser behavior with a safe read primitive.
- SSRF: prove outbound fetch or internal access before complex chains.
- Traversal: prove arbitrary read before chasing code execution.

## Good Pivot Questions

- Does the response prove code execution, file read, auth confusion, or internal reachability?
- Can reading source explain the filter or blacklist?
- Does the challenge likely want direct flag access or a shell?
