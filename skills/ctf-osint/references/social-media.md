# Social Media OSINT (including 社工 from public traces)

## Username Enumeration

- [whatsmyname.app](https://whatsmyname.app) — username across 700+ sites
- [namechk.com](https://namechk.com) — cross-platform check
- Search `"username"` in quotes on platform-specific search
- Username metadata mining: trailing digits can be postal codes (`35170` = Bruz, France), birth years (`jsmith1998`), area codes (`212nyc`), country codes (`44uk`)

**Platform false positives** (200 but no real profile): Telegram `t.me/USER` always renders a "Contact" page — check for "View" in the title; TikTok shows "Couldn't find this account"; Instagram login-walls regardless.

## Platform Priority

- International CTF personas: Twitter/X, Tumblr, GitHub, Reddit, Bluesky, Mastodon, Steam, Spotify/SoundCloud, Strava/Garmin (GPS leaks), Pastebin, linktr.ee/bio.link
- China-mainland personas: 微博, 知乎, 小红书, 抖音, B站, QQ空间, 百度贴吧, 豆瓣, 微信公众号 (via 搜狗微信搜索)

## Account Rename Tracing

- Twitter numeric User IDs persist across renames: `https://x.com/i/user/<id>` works after username changes; find IDs in archived JSON-LD.
- Wayback CDX API: `curl "http://web.archive.org/cdx/search/cdx?url=twitter.com/USERNAME*&output=json"`; t.co shortlinks in archived tweets reveal old usernames.
- Snowflake IDs encode timestamps: `(id >> 22) + 1288834974657` = Unix ms.
- Chain: known username → archives → new username → re-enumerate across all platforms → repeat until the flag platform appears.

## Platform-Specific Techniques

- **Twitter/X**: syndication API `https://syndication.twitter.com/srv/timeline-profile/screen-name/NAME`; Nitter mirrors; EXIF stripped.
- **Tumblr**: blog existence via `curl -sI https://NAME.tumblr.com` (look for `x-tumblr-user` header); post data embedded as JSON in HTML (`"content":[`); avatar at `/avatar/512` — always inspect at max resolution (visual stego hotspot).
- **Bluesky**: public API, no auth — `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=...`; search filters `from:` `since:` `has:images`. Unicode homoglyph stego: non-ASCII codepoints encode bits (skip auto-inserted smart quotes); decode with per-character ASCII=0/homoglyph=1, 8 bits per char.
- **Discord**: flags hide in role names, server description, stickers, embeds, animated emoji frames (extract GIF frames — brief frames carry data). Enumerate via API with a user token.
- **Strava/fitness**: public activity maps leak home/work neighborhoods even with privacy zones; segment leaderboards reveal locations.
- **Gaming**: WoW (Raider.IO, WoWProgress), Steam (`steamcommunity.com/id/NAME`, steamid.io), Minecraft (NameMC — name history), guild rosters cross-reference to other platforms.
- **微博/知乎/小红书**: search handle on Baidu with `site:weibo.com` etc.; 小红书 posts frequently embed location tags; 知乎 answers leak occupation/school/timeline details ideal for 社工 questions.

## Multi-Platform Chain Pattern

Typical CTF flow: image with hidden EXIF → username → enumeration → platform X hints at platform Y → flag on the final platform (Spotify playlist description, BlueSky post, Tumblr avatar, 抖音 video caption). Flag locations by platform: Spotify (playlist names/descriptions, song-title acrostics), SoundCloud (track description), Reddit (post/comments), Smule (recordings), 公众号 (article text or image stego).

## 社工 (Social Engineering from Public Traces)

In CTF this means reconstructing a **fictional persona's** secrets from what they posted — never interacting with or deceiving real people, and never touching illegal 社工库.

High-yield derivations:
- Security-question answers: pet name, mother's maiden name, first school, birthplace — scattered across posts, profiles, and comment threads.
- Birthdays: platform "joined" anniversaries, zodiac mentions, 生日动态.
- Phone/email fragments: partially masked contacts in screenshots, registration bindings discoverable via password-reset flows **on the challenge's own simulated services only**.
- Occupation/education/schedule: 知乎 bio, LinkedIn, posting-time patterns (timezone fingerprint).
- Favorite phrases / passwords: reused handles, pet names, keyboard patterns — CTF personas usually reuse one secret everywhere; the flag is often exactly this.

Method: build a persona dossier first (timeline, relationships, locations), then answer the challenge's questions from it. Record every derivation step in `steps.md` with the source post.
