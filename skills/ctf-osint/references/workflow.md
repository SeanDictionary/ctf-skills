# Workflow

## First Pass

- Extract exact strings, visual text, language hints, domains, timestamps, and geographic clues.
- Separate direct clues from challenge flavor text.
- Decide the sub-domain (geolocation / people / infrastructure) and the region hypothesis (China-mainland vs international) before searching.

## Clue Typing

| Clue type | What it gives you | First move |
|---|---|---|
| Username/handle | Cross-platform identity | Username enumeration, then per-platform deep dive |
| Photo of a place | Coordinates | Region discrimination, then reverse image search on crops |
| Photo of a person | Identity | Face-capable reverse search (Yandex international, Baidu China) |
| Domain | Ownership, infrastructure, timeline | WHOIS, ICP 备案 (China), DNS, Wayback |
| Company/org name | Registration data | 天眼查/企查查 (China), state registries (international) |
| Phone number | Region, carrier, platform registrations | Prefix tables; check which platforms bind it |
| Timestamps | Timeline anchoring | Correlate with archives, post history, logs |
| EXIF | Device, GPS, time | exiftool first; note platforms that strip it |

## Verification Loop

- Find a candidate.
- Cross-check with an independent source (different engine, different platform, archived snapshot).
- Check exact dates and historical consistency.
- Confirm the same identity or object is still the best explanation.
- Only then treat it as proven; everything else stays tagged likely/speculative.

## Confidence Tiers

Tag conclusions in `steps.md`:

- **proven**: two or more independent sources agree, or primary evidence (EXIF GPS, official registry).
- **likely**: strong single source plus consistent context.
- **speculative**: pattern match only — never build the next three steps on it silently.

## Common Mistakes

- Treating the first search hit as truth.
- Ignoring username reuse across platforms.
- Missing archived versions when current pages changed.
- Confusing plausible inference with proven identity.
- Using the wrong region's engines: Baidu for a Russian town, or Google for a Weibo watermark — region discrimination exists to prevent exactly this.
- Spray-and-pray queries: every query should follow from the previous result.
