# Geolocation and Media Analysis

## Region Discrimination (do this first)

Before searching, classify the target as China-mainland, international, or ambiguous. Every later choice (search engine, map, reverse image engine) hangs on this.

**China-mainland markers:**
- Simplified Chinese signage; 蓝牌 (blue civilian license plates, 绿牌 green NEV plates)
- Baidu/Weibo/Xiaohongshu watermarks; Amap or Baidu Maps UI in screenshots
- 门楼/arch gate architecture, 招牌 conventions, Chinese utility pole and bollard styles
- Shared bikes (Meituan yellow, Hello blue, Qingju), China Post green, 便利店 chains (全家/罗森/便利蜂)
- .cn / .com.cn domains, ICP 备案号 footer (e.g. 京ICP备xxxx号)

**International markers:**
- Latin/Cyrillic/Arabic/Korean/Japanese script; non-blue plate colors
- Google Street View car artifacts, Waze/Google Maps UI
- Country shortcuts:

| Feature | Region |
|---|---|
| Kanji + blue highway signs | Japan |
| Cyrillic + wide boulevards | Russia/CIS |
| White X-shape crossing signs | Canada |
| Yellow diamond warning signs | USA/Canada |
| Green autobahn signs | Germany |
| Brown tourist signs | France |
| Bollards with red reflectors | Netherlands |
| Left-hand traffic | UK/Japan/Australia/HK and others |

**Ambiguous → run both engine families in parallel and compare hit coherence.**

## Engine and Map Selection by Region

| Need | China-mainland | International |
|---|---|---|
| Reverse image search | Baidu 识图 (`graph.baidu.com`) | Google Lens, Yandex (best for scenes/faces), Bing, TinEye (exact match) |
| Web search | Baidu, 搜狗 (WeChat index), 360 | Google, Bing, Yandex |
| Maps / satellite | Baidu Maps, Amap (高德), 天地图 | Google Maps/Earth, OSM |
| Street-level | 百度全景 / Amap 街景 | Google Street View |
| Business lookup | 大众点评, 天眼查/企查查, 美团 | Google Maps business search, Yelp |
| POI queries | Amap API | Overpass Turbo (OSM) |

Rationale: Baidu's index of mainland content is dramatically better than Google's, and Baidu Maps/街景 covers where Street View does not; the reverse holds outside mainland China. Yandex reverse image search often beats Google Lens on scenes and faces even for Western targets.

## Reverse Image Search Discipline

- **Crop before searching.** Google Lens and Baidu both perform far better on a cropped distinctive element (shop sign, facade, landmark) than a full scene. Crop to the sign, search; crop to the storefront, search again.
- Try multiple engines before giving up; they index different webs.
- Partial readable text: search the readable fragment in quotes (`"Aguas de Lind"`), with city/country context words appended.
- Reflected/mirrored text: flip the image (`convert in.jpg -flop out.jpg` or PIL `FLIP_LEFT_RIGHT`), then read and search.
- Avatar/profile-picture reuse is a strong identity link across platforms.

## Metadata Extraction

```bash
exiftool image.jpg           # EXIF: GPS, device, timestamps
pdfinfo document.pdf         # PDF metadata
mediainfo video.mp4          # video metadata
```

- Twitter strips EXIF on upload — don't hunt stego in Twitter-served images. Tumblr preserves more in avatars than post images.
- **Visual stego check**: view at full resolution, inspect all corners/edges for tiny low-contrast text (black-on-dark, white-on-light). Avatars are a favorite hiding spot.

## Geolocation Techniques

- Process of elimination: country → region → city → street.
- Cross-reference multiple features (rail + power lines + mountains + coastline).
- Infrastructure maps: [OpenInfrastructureMap](https://openinframap.org) (power), [OpenRailwayMap](https://www.openrailwaymap.org) (rail).
- Named businesses: search the brand + 分店/locations, then pin the exact branch against terrain. Restaurant/brand geolocation is one of the highest-yield moves.
- Google Maps **Photos tab** (crowd-sourced): when reverse search fails because the image is original, search the candidate place name and compare tourist photos of the same scene.
- Sun/shadow math and Street View coverage enumeration for hard targets.

## Coordinate Formats

- **MGRS**: grid pattern like `4V FH 246 677` → online converter → lat/long.
- **Google Plus Codes**: `XXXX+XX` (local) or `8FVC9G8F+6W` (global), charset `23456789CFGHJMPQRVWX`, always contains `+`. Read from a dropped pin in Google Maps; ~14m precision.
- **What3Words**: 3m x 3m squares; the exact square matters — match the camera position, not the subject; try 5-10 adjacent squares.
- MGRS/W3W/PlusCodes challenges: identify the spot with normal geolocation first, then convert precisely.

## Overpass Turbo (OSM POI queries)

For "a business of type X near a landmark of type Y in city Z":

```text
[out:json][timeout:25];
{{geocodeArea:CityName}}->.a;
node["railway"="subway_entrance"](area.a)->.m;
node(around.m:10)["shop"~"newsagent|kiosk"];
out body; >; out skel qt;
```

Useful tags: `shop` (newsagent/kiosk/bakery), `amenity` (cafe/bank/atm), `tourism` (hotel/attraction), `railway` (station/subway_entrance). The `around` proximity filter replaces hours of map browsing. Verify survivors in Street View or 百度全景.

## Street View Panorama Matching

When the challenge image is a crop of a panorama:
1. Extract visual features (road type, vehicles, poles, vegetation, building style).
2. Narrow the region, enumerate panorama coverage there.
3. Feature-match candidates (ORB + BFMatcher, color histograms, patch comparison) and combine rankings.
4. Distinctive elements beat holistic similarity: road surface, vehicle makes, utility pole design, container colors.

## IP Geolocation

```bash
curl "http://ip-api.com/json/IP"      # no key
curl "https://ipinfo.io/IP/json"
```

Correlate with login history, telemetry, ASN lookups; note VPN/proxy possibilities.

## geo-sleuth Helper

For heavy geolocation tasks, use the geo-sleuth skill (EXIF/OCR intake, candidate board with likelihood ranking, plate/area-code/driving-side lookup tables, sun math, CLIP-ranked satellite scan, street view matching). Install on demand if missing:

```bash
git clone https://github.com/Oldcircle/geo-sleuth <skills-dir>/geo-sleuth
```

Caveats: its reverse-image integrations (Baidu/Yandex) and lookup tables lean toward China-mainland targets. For international targets, complement it with Google Lens, Street View enumeration, and Overpass rather than trusting its rankings alone. Its Python dependencies install per the normal package policy (tools/pylibs + session PYTHONPATH, or the sage env — never global).
