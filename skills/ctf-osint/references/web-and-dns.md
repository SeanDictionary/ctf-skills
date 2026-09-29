# Web and DNS OSINT

## Google Dorking

```text
site:example.com filetype:pdf
intitle:"index of" password
inurl:admin
"confidential" filetype:doc
```

Google Image `tbs=` filters: `itp:face` (faces only — strips logos/screenshots, ideal for profile-photo hunting), `itp:clipart`, `ic:specific,isc:green`, `ic:trans`, `isz:l` (large), `isz:lt,islt:2mp`. Combine with `site:` and `after:YYYY-MM-DD`.

For China-mainland targets, Baidu equivalents: `site:`, `inurl:`, `filetype:`, plus 搜狗 for WeChat 公众号 article search.

## DNS

```bash
dig -t txt subdomain.ctf.domain.com   # flags often live in TXT of subdomains, not root
dig -t any domain.com
dig axfr @ns.domain.com domain.com    # zone transfer attempt
```

Always sweep TXT, CNAME, MX for CTF domains and their subdomains.

## WHOIS

```bash
whois example.com    # registrant, creation/expiry dates, name servers
whois 1.2.3.4        # IP: NetName, OrgName, CIDR, abuse contact
whois -h whois.radb.net AS12345   # ASN
```

- Timeline correlation: domain registration dates vs challenge events.
- Historical WHOIS (pre-privacy): SecurityTrails, WhoisXML, Wayback.
- Reverse WHOIS: find other domains by the same registrant email/org.

## China-Specific Infrastructure

- **ICP 备案查询**: beian.miit.gov.cn or 站长工具 — mainland-hosted websites must carry a 备案号 (footer, e.g. 京ICP备xxxxxx号-1); the number reveals the registering company and unlocks 天眼查/企查查 pivots.
- **天眼查 / 企查查 / 爱企查**: company registration (法定代表人, 注册资本, shareholding, historical names), useful when a domain, app, or 公众号 belongs to a shell company.
- 搜狗微信搜索: index of WeChat 公众号 articles — often the only place a China persona's "blog" exists.

## Certificates and Services

- Censys / crt.sh: certificate transparency logs — subdomain discovery and hidden hosts.
- Shodan fingerprint pivots: `ssh.fingerprint:"MD5:..."` or `ssl.cert.fingerprint:"SHA256"` to de-anonymize services behind CDN/Tor.
- Fake banners: a port answering on 22/80 isn't necessarily SSH/HTTP — `nmap -sV` or plain `nc target 22` to read the actual banner; flags hide in custom banners on standard ports.

## Archives

```bash
curl "http://web.archive.org/cdx/search/cdx?url=example.com*&output=json&fl=timestamp,original,statuscode"
```

Deleted posts, old profiles, pre-privacy WHOIS, previous site versions. Also check archive.today snapshots; for China-mainland pages check 百度快照 when Wayback has nothing.

## Code Platforms

- Git repos are audit logs of every author: `git shortlog -sne`, `git log --format="%an <%ae>%n%cn <%ce>" | sort -u`; recovered emails are candidate logins for the challenge's own portals.
- GitHub-wide: `gh api users/NAME/events/public --paginate | jq -r '.[] | .payload.commits[]?.author.email'`.
- Check repo issues/comments, wiki history, `.mailmap`, `CONTRIBUTORS`.
- `.DS_Store` files leak directory listings: `curl -sO https://target/.DS_Store && python3 -m dsstore .DS_Store`.

## Google Docs/Sheets

Public export endpoints: `/export?format=csv`, `/pub`, `/gviz/tq?tqx=out:csv`, `/htmlview`. Sheet IDs are stable across sharing-setting changes.

## Resources

- Shodan / Censys — devices, certificates
- VirusTotal — file/URL reputation
- Wayback Machine / archive.today / 百度快照 — history
- bgp.tools — ASN
