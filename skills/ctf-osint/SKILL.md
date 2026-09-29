---
name: ctf-osint
description: Use when a CTF challenge requires open-source intelligence rather than a local exploit — attribution, timeline reconstruction, public-profile discovery, geolocation (图寻 / photo geolocation), reverse image search, social engineering from public traces (社工), username enumeration, social media mining, web/DNS/WHOIS investigation, or entity linking. Best for usernames, aliases, domains, social accounts, leaked handles, EXIF clues, screenshots, photos of unknown places, public archives, and tasks where the answer depends on current or historical internet-visible evidence. Covers both China-mainland sources (Baidu, Weibo, Zhihu, ICP lookup, 天眼查) and international sources (Google, Yandex, Wayback, Shodan), with region-aware engine and map selection.
---

# CTF OSINT

## Overview

OSINT is not one technique but four sub-domains that share one discipline: turn weak public clues into candidates, then verify across independent sources before claiming the answer. Route to the right sub-domain first, decide **China-mainland vs international** early, and pick search engines and maps accordingly.

## Use This Skill For

- The challenge is about a person, alias, image, location, domain, company, or timeline.
- A photo of an unknown place must be geolocated (图寻 / geoguessr-style).
- Public websites, social platforms, archived pages, or search results are part of the solution path.
- The intended path is social engineering from public traces (社工): deriving birthdays, pets, schools, phone fragments, or security-question answers from what the target persona left online.
- The user needs help keeping evidence organized and avoiding false attribution.

## Sub-Domain Routing

| Signal shape | Reference |
|---|---|
| Photo/video geolocation, EXIF, reverse image search, coordinate formats | [references/geolocation-and-media.md](references/geolocation-and-media.md) |
| People, usernames, social platforms, gaming/fitness profiles, account renames | [references/social-media.md](references/social-media.md) |
| Domains, DNS, WHOIS, ICP 备案, certificates, Shodan, archives, dorks | [references/web-and-dns.md](references/web-and-dns.md) |
| General clue typing, verification loop, confidence tiers | [references/workflow.md](references/workflow.md) |

## Core Principles

1. **Region discrimination comes first.** Before any search, decide whether the target is China-mainland or international. Language/script, license plates, signage, platform artifacts (Weibo watermark vs Twitter), and domain type all discriminate. The choice determines which engines and maps to prefer:
   - China-mainland → Baidu (image: `graph.baidu.com` 识图), Baidu Maps, Amap (高德), 天眼查/企查查, ICP 备案查询, Weibo/Zhihu/Xiaohongshu/Bilibili/Tieba.
   - International → Google (Lens), Yandex, Bing, Google Maps/Earth/Street View, OSM/Overpass, Wayback, Shodan.
   - Ambiguous → run both sides in parallel; the side that returns coherent hits wins.
2. **Verify across independent sources.** A match must survive cross-checking with dates, geography, visual evidence, or archived snapshots.
3. **State confidence honestly.** Tag every conclusion as proven / likely / speculative in `steps.md`.

## Workflow

1. Normalize the clue set.
   Names, handles, domains, image fragments, timestamps, languages, context hints. Separate direct clues from challenge flavor text.
2. Pick the sub-domain and region hypothesis.
   Route via the table above; state China vs international and why.
3. Expand candidates carefully.
   Exact matches, close variants, reused avatars, domain ownership, contextual links — using region-appropriate engines.
4. Verify across independent sources.
   Cross-check dates, geography, visual evidence, archived snapshots.
5. Keep a timeline when dates matter.
   Use exact dates rather than relative wording.
6. Stop when the answer is defensible.
   OSINT rewards precision more than volume.

## Helper Skills

- **geo-sleuth** (photo geolocation / chronolocation toolkit: EXIF, OCR, reverse image search, candidate board, sun/shadow math, OSM Overpass, CLIP-ranked satellite scan): not installed by default. When a geolocation task needs it and it is missing, install it on demand into the skills folder — `git clone https://github.com/Oldcircle/geo-sleuth <skills-dir>/geo-sleuth` (user pre-authorized). Its reverse-image and lookup tables lean toward China-mainland; for international targets complement it with Google Lens/Street View/Overpass rather than relying on it alone. Its Python dependencies follow the normal package policy (tools/pylibs or the sage env, never global).

## Guardrails

- Use live browsing when public information may have changed.
- Prefer primary or directly attributable sources when possible.
- State when a claim is an inference rather than a direct fact.
- 社工 in CTF means deriving information a fictional persona left in public traces — posts, profiles, registration data. Never interact with, deceive, or collect data on real people; never use leaked-password databases or any illegal 社工库; never attempt unauthorized account access outside the challenge's own simulated surfaces.
- Avoid doxxing behavior outside authorized CTF contexts.
- Record every query that changed the next decision in `steps.md`; dead queries only need one line.

## Output Expectations

- Report the clue, candidate identity or explanation, the corroborating sources, and the confidence level.
- For geolocation: coordinates plus error radius and the decisive evidence, not just a place name.
- Before pausing, append a `steps.md` handoff: working hypotheses, exhausted leads, region conclusion, and the next recommended query.
