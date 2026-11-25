"""Wednesday 25 November 2026, as data. Counts are derived, never hard-coded."""

DATE_LINE = "WEDNESDAY — 25 NOVEMBER 2026"
FOOTER = (
    "Sources: Reuters, AP, AFP, Al Jazeera, ABS, USTR · "
    "all stories dated Wed 25 Nov 2026 (UTC)"
)

LEAD = {
    "tag": "TRADE · MARKETS",
    "headline": "Trump fires new tariff salvo as AI stocks slide",
    "bullets": [
        "US proposes tariffs of 15–35% on 14 economies incl. China, EU, Japan and India; China faces the highest rates",
        "Nasdaq falls 4% and the S&P 500 2.8% as the AI sell-off deepens",
        "Chip stocks lead the fall; the Nasdaq 100 fund gives back almost all of Monday's rally",
    ],
}

TILES = [
    {
        "tag": "MIDDLE EAST · HORMUZ",
        "headline": "More tankers hit mines in Hormuz",
        "deck": "Iran says two more oil tankers hit mines and caught fire; it tells ships to coordinate passage",
        "continent": "Middle East",
        "icon": "tanker",
    },
    {
        "tag": "EUROPE · UKRAINE",
        "headline": "Drones hit two Russian refineries",
        "deck": "Ukraine strikes Samara oil plants; Russian attack cuts power in five Ukrainian regions",
        "continent": "Europe",
        "icon": "refinery",
    },
    {
        "tag": "ASIA · CHIPS",
        "headline": "'Huang effect' fades in a day",
        "deck": "Kospi −6.2%, Taiex −4.8%; SK Hynix −11%",
        "continent": "Asia",
        "icon": "chip",
    },
]

REGIONS = [
    {
        "name": "EUROPE",
        "color": "#2B5FA8",
        "continent": "Europe",
        "items": [
            {"lead": "Germany", "text": 'Merz: Russia "wants more than Ukraine"'},
            {"lead": "Russia", "text": "Putin vows retaliation over refinery attacks"},
            {"lead": "Moscow", "text": "envoy says Europeans must visit before joining peace talks"},
            {"lead": "UK", "text": "moves military planes into hangars to guard against drones (reports)"},
        ],
    },
    {
        "name": "MIDDLE EAST",
        "color": "#B5462E",
        "continent": "Middle East",
        "items": [
            {"lead": "Yemen", "text": "coalition orders Hodeidah evacuation; Houthis threaten Saudi Red Sea ports"},
            {"lead": "Saudi Arabia", "text": "Houthis claim drone attack on Ras Tanura refinery"},
            {"lead": "Iran", "text": "accuses US of using AI in strikes"},
        ],
    },
    {
        "name": "ASIA",
        "color": "#C08A1E",
        "continent": "Asia",
        "items": [
            {"lead": "Japan", "text": "Nikkei −2.8%; SoftBank sinks about 16% intraday"},
            {"lead": "Taiwan", "text": "TSMC down 9.4% intraday; MediaTek hits limit-down"},
            {"lead": "Japan", "text": "approval of Takaichi's China policy falls to 44%"},
            {"lead": "India", "text": "faces proposed US duties of up to 25%"},
        ],
    },
    {
        "name": "AFRICA",
        "color": "#8A5A2B",
        "continent": "Africa",
        "items": [
            {"lead": "South Africa", "text": 'court voids "Farmgate" findings against Ramaphosa'},
            {"lead": "Zambia", "text": "opposition leader Mundubile denies treason plot"},
            {"lead": "Somalia", "text": "speaker accuses Kenya, Ethiopia, Uganda over al-Shabaab"},
        ],
    },
    {
        "name": "AMERICAS",
        "color": "#2E7D5B",
        "continent": "Americas",
        "items": [
            {"lead": "Iowa", "text": "Army detonates 5 tons of lead azide; nearby residents told to stay indoors"},
            {"lead": "Spain", "text": "Abrego Garcia lands in Madrid after leaving the US"},
            {"lead": "Argentina", "text": "economy enters technical recession"},
            {"lead": "Chile", "text": "7 convicted over 2024 Valparaíso wildfire that killed 138"},
        ],
    },
    {
        "name": "OCEANIA",
        "color": "#1F8A8A",
        "continent": "Oceania",
        "items": [
            {"lead": "Australia", "text": "inflation jumps to 4.9%, a three-year high"},
            {"lead": "Papua New Guinea", "text": "launches 16 Days of Activism against gender violence"},
        ],
    },
    {
        "name": "MARKETS",
        "color": "#6B4FA0",
        "continent": None,
        "items": [
            {"lead": "Wall St", "text": "Nasdaq 100 briefly 20% below its record, near bear territory"},
            {"lead": "Dow", "text": "falls 738 points, or 1.5%"},
        ],
    },
    {
        "name": "WORLD",
        "color": "#7A7A7A",
        "continent": None,
        "items": [
            {"lead": "UN", "text": "Day to End Violence against Women: 5 women and girls killed every hour by partners or family"},
            {"lead": "UN", "text": "16 Days of Activism against gender violence begin"},
            {"lead": "US", "text": "markets shut Thursday for Thanksgiving"},
        ],
    },
]


def story_count() -> int:
    regional = sum(len(region["items"]) for region in REGIONS)
    return 1 + len(TILES) + regional


def continent_count() -> int:
    names = {tile["continent"] for tile in TILES if tile["continent"]}
    names.update(region["continent"] for region in REGIONS if region["continent"])
    return len(names)


def strapline() -> str:
    stories = story_count()
    continents = continent_count()
    story_word = "STORY" if stories == 1 else "STORIES"
    continent_word = "CONTINENT" if continents == 1 else "CONTINENTS"
    return f"{stories} {story_word} · {continents} {continent_word}"


if __name__ == "__main__":
    print(story_count())
    print(strapline())
