#!/usr/bin/env python3
"""Render the front page for make.fun's news-image-20261118 entry.

A dense broadsheet front page for Wednesday 18 November 2026 carrying
150 numbered stories across six continents, a dot-grid world map with
story markers, a featured lead, a numbers box, a wire ticker and a
sources line. Drawn at 2048x2048 with Pillow, downscaled to the
shipped 1024x1024 entry.png. Deterministic: fixed data, fixed fonts,
no randomness, no clock, no network.
Run:  python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024 * S
OUT = "entry.png"

PAPER = (247, 243, 234)
INK = (20, 23, 29)
GREY = (92, 96, 104)
RED = (178, 30, 40)
NAVY = (18, 36, 62)
PANEL = (232, 237, 242)
LANDC = (58, 84, 110)
HAIR = (196, 188, 172)
DETAIL = (74, 78, 86)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
try:
    def F(name, size):
        return ImageFont.truetype(f"{FONT_DIR}/{name}", size)
    F("LiberationSans-Bold.ttf", 20)
except Exception:
    FONT_DIR = "/usr/share/fonts/truetype/dejavu"
    def F(name, size):
        return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

def bold(size): return F("LiberationSans-Bold.ttf", size)
def reg(size):  return F("LiberationSans-Regular.ttf", size)

# ------------------------------------------------------------- story data
# (headline, short detail, lon or None, lat or None) — numbered in order.
LEAD = ("IRAN AND US TRADE BLOWS ACROSS THE GULF",
        "Iranian drones target US forces in Bahrain - intercepted, CENTCOM says. "
        "Tankers ablaze in the Strait of Hormuz after mine strikes. "
        "US hits a missile site on Qeshm Island; Kuwait reports interceptions.",
        50.6, 26.2)

SECTIONS = [
    ("ASIA", RED, [
        ("Iran and US trade blows in the Gulf", "drones down, tankers ablaze", 50.6, 26.2),
        ("Gaza ceasefire 'near collapse'", "Board of Peace warns", 34.3, 31.4),
        ("WFP: one hot meal every two days", "in Gaza displacement camps", 34.3, 31.5),
        ("Gaza families back to kerosene", "cooking-gas shortage bites", 34.4, 31.4),
        ("Kuwait intercepts drones", "Bahrain sounds the all-clear", 47.98, 29.4),
        ("IRGC chief in Iraq for talks", "amid Kataib Hezbollah tension", 44.4, 33.3),
        ("Israel elects Kahana speaker", "Knesset picks Eisenkot ally", 35.2, 31.8),
        ("Hezbollah wary of Syria's Sharaa", "Knesset briefing reveals", 35.5, 33.5),
        ("Trump lands in Manila", "Quad talks before China trip", 121.0, 14.6),
        ("Hundreds detained in Manila", "protesting Trump's visit", 121.0, 14.7),
        ("Philippines hands ASEAN chair over", "Singapore takes the helm", 121.0, 14.5),
        ("Modi proposes free e-visas", "at ASEAN-India summit", 121.0, 14.6),
        ("ASEAN, China stall on sea code", "South China Sea talks short", 114.1, 22.5),
        ("Marcos, Takaichi chair summit", "AZEC clean-energy push", 121.0, 14.6),
        ("East Asia unites on online fraud", "leaders back joint action", 121.0, 14.6),
        ("APEC opens in Shenzhen", "Xi, Putin, Trump in focus", 114.1, 22.5),
        ("COP31 draft: faster fossil exit", "tough talks ahead in Antalya", 30.7, 36.9),
        ("US presses UN agency on Taiwan", "flight curbs; China hits back", 121.0, 23.7),
        ("Taiwan: China 'mobilising voters'", "agencies cite five tactics", 120.9, 23.7),
        ("Japan protests airspace violations", "two aircraft, Tokyo says", 139.7, 35.7),
        ("Takaichi meets Trump in Manila", "ahead of his Xi-Putin summit", 121.0, 14.6),
        ("Japan proposes Asian energy agency", "offers idle oil storage", 139.7, 35.6),
        ("India condemns tanker attack", "21 of 24 crew ashore in Oman", 56.2, 26.2),
        ("Earthshot Prize night in Mumbai", "William & Kate play cricket", 72.9, 19.1),
        ("India electronics exports up 44%", "to $31.97bn this year", 77.2, 28.6),
        ("Amazon's $7bn for India renewables", "investment runs to 2030", 77.2, 28.6),
        ("India, Egypt explore trade pact", "Goyal concludes Cairo visit", 31.2, 30.0),
        ("India joins Pax Silica initiative", "US-led AI chips alliance", 77.2, 28.6),
        ("India re-elected to ITU Council", "for the 2027-2030 term", 77.2, 28.6),
        ("Nvidia halts H200 shipments", "to customers in China", 114.1, 22.6),
        ("Phuket shophouse fire kills 11", "blaze on Thai resort island", 98.4, 7.9),
        ("Indonesia apologises for haze", "to Singapore and Malaysia", 106.8, -6.2),
        ("Delhi students protest pollution", "as smog chokes the capital", 77.2, 28.7),
        ("Imran Khan writes to judges", "jailed ex-PM seeks care", 73.1, 33.7),
        ("S Korea AI-glasses exam scandal", "cheating fears grow", 127.0, 37.0),
        ("Kim's daughter in ski photos", "rare images at resort", 127.5, 40.5),
        ("Manipur shutdown after killings", "four Naga civilians dead", 93.9, 24.8),
        ("Cyclone Akvan strengthens", "Chennai-Yangon flights cut", 88.0, 14.0),
        ("India beat Pakistan 2-1 in Dhaka", "record 10th SAFF title", 90.4, 23.8),
        ("Dhoni ends IPL playing career", "to mentor Chennai Super Kings", 80.3, 13.1),
        ("Jay Shah re-elected ICC chairman", "second consecutive term", 72.9, 19.0),
        ("India to host 2029 Champions Trophy", "also 2031 World Cup", 77.2, 28.6),
        ("Modi at East Asia Summit", "peaceful Indo-Pacific vision", 121.0, 14.6),
    ]),
    ("EUROPE", (36, 86, 166), [
        ("Ukraine hits Crimea Bridge again", "second day of strikes", 34.5, 45.2),
        ("UN: 372 civilians killed in Ukraine", "October toll, HRMMU says", 31.6, 50.4),
        ("Zelensky seeks more air defences", "and fighter jets, again", 30.5, 50.4),
        ("UK gives £240m for Ukraine", "air-defence package", -0.1, 51.5),
        ("EU adds €15m for mine clearance", "in Ukraine", 4.35, 50.85),
        ("EU picks five for peace talks", "to represent Europe", 4.35, 50.8),
        ("US envoys shuttle Kyiv-Moscow", "between Putin and Zelenskyy", 30.5, 50.5),
        ("UK sanctions 8 settlement firms", "over West Bank expansion", -0.1, 51.6),
        ("Latvia approves new government", "Kulbergs wins vote", 24.1, 56.9),
        ("French strikes swell", "unions join nationwide action", 2.35, 48.9),
        ("Barcelona erupts after strike", "violence follows general strike", 2.2, 41.4),
        ("EU probes Spain train crash", "prosecutor investigates", -3.7, 40.4),
        ("Prague trains collide", "passengers and drivers hurt", 14.4, 50.1),
        ("Serbian pilot dies in MiG-29 crash", "near Stara Pazova", 20.2, 44.9),
        ("Seven flights face bomb threats", "across Europe", 10.0, 50.0),
        ("300+ migrants rescued", "off Spain's Canary Islands", -15.6, 28.1),
        ("Five EU states plan Rwanda hub", "for migrant returns", 4.4, 50.8),
        ("EU tells TikTok to fix its feed", "'harmful' For You page", 4.35, 50.9),
        ("EU accuses Temu of DSA breach", "illegal, unsafe goods on sale", 4.4, 50.9),
        ("EU backs €9.5bn Dutch wind farms", "two offshore projects", 5.1, 52.1),
        ("EU approves German energy aid", "for energy-intensive firms", 13.4, 52.5),
        ("Montenegro closes EU chapter 16", "24 of 33 now shut", 19.3, 42.4),
        ("EU economy 'more resilient'", "Commission's 2026 verdict", 4.35, 50.85),
        ("UK climate targets at risk", "if EV rules weaken - advisers", -0.1, 51.4),
        ("Deutsche Bank 'ignored warnings'", "on risky clients - probe", 8.7, 50.1),
        ("Sweden: more government talks", "Speaker sets new round", 18.1, 59.3),
        ("US jet wrecked at Irish airport", "while parked, feds say", -8.9, 52.7),
        ("Netherlands quits Eurovision 2027", "over Israel 'sensitivities'", 5.3, 52.1),
        ("Five EU states set fossil exit", "phase-out plans at COP31", 30.7, 36.8),
        ("Russia's brown bears double", "to a record 300,000", 90.0, 60.0),
        ("Alcaraz sweeps Tiafoe 6-2 6-2", "ATP Finals opener", 7.7, 45.1),
        ("Ronaldinho plays again at 46", "for Italy's Ravenna", 12.2, 44.4),
        ("Ukrainian freediver sets record", "deepest competitive dive", 31.0, 49.0),
        ("Irish boxer Lee Reeves dies, 31", "three months after injury", -8.2, 53.2),
        ("Olympian Ciara Mageean dies, 34", "Irish athletics champion", -6.3, 53.3),
    ]),
    ("NORTH AMERICA", (46, 125, 79), [
        ("Nvidia revenue doubles", "$115.8bn; no Huang return", -122.0, 37.4),
        ("Merchant jailed 27 years", "in Trump murder-for-hire plot", -74.0, 40.7),
        ("Trump-BBC deposition delayed", "$10bn case; new date 22 Jan", -77.0, 38.9),
        ("Dow plunges 848 points", "tech sell-off before earnings", -74.0, 40.8),
        ("White House drops FDA nominee", "Heidi Overton withdrawn", -77.0, 38.9),
        ("Democrats push stock-trade ban", "for members of Congress", -77.0, 38.9),
        ("Outages sweep US industries", "White House urges calm", -87.6, 41.8),
        ("Data centres 'use states' power'", "study warns on AI demand", -77.5, 39.0),
        ("US loses measles-free status", "PAHO confirms loss", -99.0, 31.0),
        ("Fed's Cook snubs White House", "refuses to attend hearing", -77.0, 38.8),
        ("Republicans scramble on FCC pick", "third Trump nominee sought", -77.1, 38.9),
        ("Trump: Iran plot report serious", "dirty-bomb claim 'very serious'", -77.0, 39.0),
        ("US seeks $50.1bn for air traffic", "FAA upgrade needs Congress", -77.0, 38.9),
        ("California bars Waymo freeways", "self-driving cars restricted", -122.4, 37.8),
        ("Voyager 1 reaches one light-day", "25.9bn km; signals take 24h", -118.2, 34.1),
        ("SpaceX catches falling Starship", "booster snatched in Texas", -97.2, 25.9),
        ("Haiti: Moise's widow to run", "for president, enrolment shuts", -72.3, 18.5),
        ("Canada, China extend trade deals", "Xi meets Carney pre-APEC", -75.7, 45.4),
        ("Haiti-US friendly in Cincinnati", "fans despite ICE fears", -84.5, 39.1),
        ("WNBA chief eyes stake buyback", "Engelbert explores reclaim", -74.0, 40.6),
        ("Disney revenue up 16%", "to $25.9bn in fourth quarter", -118.3, 34.0),
        ("Microsoft: Copilot is 'new OS'", "Ignite keynote claim", -122.1, 47.6),
        ("Raye leads Grammy nominations", "Styles snubbed", -118.2, 34.0),
    ]),
    ("SOUTH AMERICA", (122, 79, 163), [
        ("Brazil moves on Enel licence", "regulator to end concession", -46.6, -23.5),
        ("Norway enters Brazil salmon", "tariff-free deal alarms Chile", -47.9, -15.8),
        ("Isolated Awa make rare contact", "first in decades, Maranhao", -45.0, -4.0),
        ("Storms batter southern Brazil", "Porto Alegre on orange alert", -51.2, -30.0),
        ("Ecuador fishermen sue US", "over drone strike on boat", -80.5, -1.0),
        ("Hegseth to visit Colombia", "will deliver a C-130 Hercules", -74.1, 4.7),
        ("ASUR's $1.5bn Colombia airports", "five airports to expand", -75.6, 6.2),
        ("Caribbean fears EU threat", "to citizenship programmes", -59.6, 13.2),
        ("Colombia sacks gaming chief", "Coljuegos' Vives removed", -74.1, 4.6),
        ("First LatAm helicopter lease", "H145 to Mexico's COTEMAR", -99.1, 19.4),
    ]),
    ("AFRICA", (199, 116, 0), [
        ("Ebola cases double in DR Congo", "11,300 cases, 5,500 deaths", 30.3, 1.6),
        ("Sudan files UN complaint", "over Ethiopia drone attacks", 32.5, 15.6),
        ("UN confirms 2,230 Sudan deaths", "1,630 by drones this year", 32.5, 15.5),
        ("Congo peace efforts stall", "violence in the east goes on", 29.2, -1.7),
        ("Guinea jails 224 over gold", "unauthorised-mining crackdown", -11.0, 10.5),
        ("Kigali treaty nears 90%", "HFC phase-down ratifications", 30.1, -1.9),
        ("Nigeria threatens traders", "over underweight goods", 7.5, 9.1),
        ("Nigeria Senate: bar the violent", "INEC urged to disqualify", 7.5, 9.0),
        ("Nigeria police seize launcher", "grenade launcher, machine gun", 3.4, 6.5),
        ("AfDB lends Nigeria $500m", "governance, energy transition", 7.5, 9.2),
        ("ENGIE closes Egypt wind deal", "900MW Gulf of Suez 3 farm", 33.8, 26.8),
        ("Trinasolar's $200m Zambia solar", "power-generation boost", 28.3, -15.4),
        ("Ramaphosa launches wind farm", "Seriti Green project", 25.6, -28.7),
        ("Ruto hosts western leaders", "State House development tour", 36.8, -1.3),
        ("Kenya opposition unites early", "single candidate for 2027", 36.8, -1.4),
        ("Mozambique's Mondlane on trial", "opposition chief at top court", 32.6, -25.9),
        ("ECOWAS targets rice self-supply", "100% by 2035", 7.5, 9.1),
        ("Africa tightens animal controls", "disease controls up", 38.8, 9.0),
        ("Accra summit eyes $170bn gap", "Africa infrastructure push", -0.2, 5.6),
        ("Nigeria coach up for CAF award", "Flamingos' Busari nominated", 7.5, 9.0),
    ]),
    ("OCEANIA", (14, 125, 134), [
        ("Australia sanctions settlers", "Wong targets West Bank firms", 149.1, -35.3),
        ("150 artists fight gas plan", "Woodside's Browse, Scott Reef", 122.5, -16.5),
        ("NZ banks unite against scams", "joint anti-fraud effort", 174.8, -41.3),
        ("NZ election on a knife-edge", "126,000 expats could decide", 174.8, -36.8),
        ("Drought emergency: Fiji, Tonga", "El Nino dry spell deepens", 178.4, -17.7),
        ("Niue wins Earthshot prize", "ocean conservation honoured", -169.9, -19.1),
        ("Vanuatu: let ICJ guide COP31", "Regenvanu addresses summit", 167.0, -16.0),
        ("Singapore's $500k for Pacific", "to Resilience Facility", 103.8, 1.35),
        ("Cyclone Xavier nears Cooks", "heavy rain for Samoa possible", -159.8, -21.2),
        ("Jet lands after cabin smoke", "Singapore Airlines at Rocky", 150.5, -23.4),
        ("NZ liable for Penrhyn port", "cost overruns accepted", -157.9, -9.0),
        ("One Nation vows refugee cut", "90% under 'tough stance'", 149.1, -35.2),
        ("96% of reefs at extinction risk", "shallow-water coral study", 160.2, -9.6),
        ("Trump praises 'friend' Albanese", "at Quad summit in Manila", 121.0, 14.6),
        ("Santner out of India Tests", "fractured right hand", 172.6, -43.5),
    ]),
    ("WORLD & SCIENCE", NAVY, [
        ("WHO: resistance could kill 39m", "over 25 years, report warns", 6.1, 46.2),
        ("Deep-sea rocks teem with life", "miners want their metals", -155.0, 10.0),
        ("Leonid meteors peak tonight", "among year's fastest showers", None, None),
        ("Grynspan tipped for UN chief", "could be first woman in post", -73.9, 40.7),
    ]),
]

TOTAL = sum(len(items) for _, _, items in SECTIONS)
assert TOTAL == 150, TOTAL

NUMBERS = [
    ("$115.8bn", "Nvidia revenue +103%"),
    ("25.9bn km", "Voyager 1 light-day"),
    ("11,300", "Ebola cases, DR Congo"),
    ("5,500", "Ebola deaths (WHO)"),
    ("484", "Sudan drone row toll"),
    ("372", "Ukraine Oct civilian toll"),
]

TICKER = ("MORE ON THE WIRE  -  Cruise ship emergency off the Australian coast  -  "
          "Amazon's Black Friday deals 'often deceptive', think tank says  -  "
          "FIFA challenger Diallo claims support beyond Europe")

SOURCES = ("Sources: Reuters - AP - BBC - AFP - Al Jazeera - The Guardian - NASA - WHO - UN News - "
           "RNZ - PINA - Gizmodo - CNBC - Agence Europe - reports of Wednesday 18 November 2026")

# ------------------------------------------------------------- world map
LAND_SPANS = {
    0:  [(36, 41)],
    1:  [(21, 26), (34, 43), (51, 52), (55, 58), (64, 67)],
    2:  [(14, 19), (22, 30), (33, 42), (54, 58), (62, 70), (76, 84), (88, 92)],
    3:  [(2, 9), (13, 32), (34, 41), (52, 60), (63, 72), (75, 84), (86, 93)],
    4:  [(2, 10), (13, 33), (35, 39), (43, 44), (50, 54), (55, 70), (74, 84), (86, 94)],
    5:  [(3, 11), (14, 34), (36, 38), (43, 44), (50, 56), (57, 75), (78, 88), (90, 95)],
    6:  [(4, 11), (15, 25), (31, 35), (47, 48), (50, 56), (57, 76), (80, 88), (90, 95)],
    7:  [(5, 10), (16, 25), (31, 36), (47, 48), (50, 57), (58, 76), (80, 88), (89, 91), (92, 94)],
    8:  [(17, 35), (47, 48), (49, 55), (57, 76), (79, 88), (89, 90)],
    9:  [(18, 34), (47, 48), (49, 56), (57, 74), (76, 84)],
    10: [(19, 33), (47, 48), (48, 51), (52, 56), (59, 66), (67, 82), (85, 86)],
    11: [(16, 31), (46, 49), (50, 52), (54, 60), (61, 72), (73, 83), (84, 86)],
    12: [(15, 30), (46, 49), (50, 52), (54, 58), (59, 68), (72, 82), (84, 85)],
    13: [(15, 30), (46, 49), (50, 52), (53, 55), (54, 58), (59, 64), (70, 81), (82, 83), (84, 85)],
    14: [(15, 29), (54, 59), (60, 64), (65, 68), (71, 80), (84, 85)],
    15: [(15, 29), (46, 52), (55, 57), (57, 61), (61, 65), (67, 72), (72, 79)],
    16: [(16, 27), (45, 56), (57, 62), (65, 70), (73, 79), (80, 80)],
    17: [(14, 24), (44, 57), (58, 62), (66, 71), (73, 76), (77, 79), (79, 81)],
    18: [(14, 23), (43, 56), (58, 62), (66, 70), (74, 78), (79, 81)],
    19: [(14, 22), (42, 58), (59, 61), (66, 70), (76, 78), (80, 81)],
    20: [(20, 25), (42, 61), (66, 69), (74, 77)],
    21: [(21, 26), (42, 57), (58, 61), (67, 68), (74, 77), (81, 82)],
    22: [(27, 34), (43, 56), (59, 61), (73, 74), (74, 75), (80, 81)],
    23: [(26, 35), (43, 57), (73, 75), (77, 79), (80, 81)],
    24: [(26, 36), (44, 56), (74, 76), (77, 80), (80, 81), (83, 87)],
    25: [(26, 37), (44, 53), (54, 56), (75, 76), (76, 77), (77, 79), (83, 87)],
    26: [(27, 38), (44, 52), (53, 55), (76, 78), (77, 79), (83, 87)],
    27: [(27, 38), (44, 52), (53, 55), (76, 78), (83, 87)],
    28: [(27, 38), (44, 54), (77, 78), (81, 82), (83, 86)],
    29: [(27, 37), (44, 53), (59, 60), (81, 82), (82, 84), (86, 86)],
    30: [(27, 36), (44, 52), (59, 61), (80, 89)],
    31: [(27, 35), (44, 52), (59, 60), (80, 89)],
    32: [(27, 34), (44, 51), (59, 60), (80, 89)],
    33: [(27, 34), (44, 51), (59, 59), (81, 89)],
    34: [(28, 34), (44, 50), (81, 89)],
    35: [(28, 33), (44, 50), (81, 88), (94, 94)],
    36: [(28, 32), (44, 50), (82, 88), (94, 95)],
    37: [(28, 31), (45, 49), (82, 87), (94, 95)],
    38: [(28, 30), (45, 48), (83, 87), (94, 95)],
    39: [(28, 29), (45, 47), (87, 87), (93, 94)],
    40: [(28, 29), (93, 94)],
    41: [(28, 28)],
    42: [(28, 28)],
    43: [(28, 28)],
    44: [(28, 28)],
    45: [],
}
GRID_W, GRID_H = 96, 46

def land_cells():
    cells = set()
    for r, spans in LAND_SPANS.items():
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cells.add((c, r))
    return cells

LAND_SET = land_cells()

def marker_cell(lon, lat):
    c = int(round((lon + 178.125) / 3.75))
    r = int(round((82.4 - lat) / 3.2))
    c = max(0, min(GRID_W - 1, c)); r = max(0, min(GRID_H - 1, r))
    if (c, r) in LAND_SET:
        return c, r
    for rad in range(1, 5):
        for dc in range(-rad, rad + 1):
            for dr in range(-rad, rad + 1):
                if (c + dc, r + dr) in LAND_SET:
                    return c + dc, r + dr
    return c, r

# ---------------------------------------------------------------- layout
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

MX = 36

# masthead
name_f = bold(78)
name = "ONE WORLD, ONE DAY"
d.text(((W - tw(name, name_f)) / 2, 10), name, font=name_f, fill=NAVY)
strap_f = reg(24)
strap = "THE WHOLE WORLD'S NEWS ON A SINGLE PAGE - DRAWN FROM THE DAY'S WIRE REPORTS"
d.text(((W - tw(strap, strap_f)) / 2, 100), strap, font=strap_f, fill=GREY)

# date band
d.rectangle([MX, 132, W - MX, 214], fill=RED)
d.text((MX + 24, 146), "WEDNESDAY 18 NOVEMBER 2026", font=bold(52), fill=(255, 255, 255))
cnt = "150 STORIES - 6 CONTINENTS"
cnt_f = bold(34)
d.text((W - MX - 24 - tw(cnt, cnt_f), 156), cnt, font=cnt_f, fill=(255, 255, 255))

# lead
y = 228
chip_f = bold(24)
d.rectangle([MX, y, MX + 320, y + 36], fill=NAVY)
d.text((MX + 14, y + 5), "THE LEAD - STORY 1", font=chip_f, fill=(255, 255, 255))
stats = ["3 tankers ablaze - Hormuz", "0 damage - CENTCOM", "2-month lull broken - AP"]
sx = MX + 356
stat_f = bold(24)
for st in stats:
    w_ = tw(st, stat_f) + 26
    d.rectangle([sx, y, sx + w_, y + 36], outline=RED, width=2)
    d.text((sx + 13, y + 5), st, font=stat_f, fill=RED)
    sx += w_ + 14
y += 48
d.text((MX, y), LEAD[0], font=bold(54), fill=INK)
y += 66
for ln in wrap(LEAD[1], reg(26), W - 2 * MX)[:2]:
    d.text((MX, y), ln, font=reg(26), fill=(52, 56, 64))
    y += 33

# also-leading strip
y += 8
also = [("44", "Ukraine hits Crimea Bridge again"),
        ("79", "Nvidia revenue doubles to $115.8bn"),
        ("93", "Voyager 1 reaches one light-day"),
        ("112", "Ebola cases double in DR Congo")]
box_w = (W - 2 * MX - 3 * 16) // 4
al_n = bold(26); al_f = bold(21)
for i, (num, head) in enumerate(also):
    x = MX + i * (box_w + 16)
    d.rectangle([x, y, x + box_w, y + 62], fill=PANEL)
    d.text((x + 12, y + 8), num + ".", font=al_n, fill=RED)
    hx = x + 12 + tw(num + ".", al_n) + 8
    lines = wrap(head, al_f, x + box_w - hx - 8)
    ly = y + 8
    for ln in lines[:2]:
        d.text((hx, ly), ln, font=al_f, fill=INK)
        ly += 25
y += 74

# map row: numbers box + map + glance box
map_y, map_h = y, 268
boxw = 396
d.rectangle([MX, map_y, MX + boxw, map_y + map_h], fill=NAVY)
d.text((MX + 18, map_y + 12), "THE DAY IN NUMBERS", font=bold(26), fill=(255, 255, 255))
ny = map_y + 52
nv_f, nl_f = bold(23), reg(21)
for val, lab in NUMBERS:
    d.text((MX + 18, ny), val, font=nv_f, fill=(255, 209, 102))
    vx = MX + 18 + tw(val, nv_f) + 10
    d.text((vx, ny + 2), "- " + lab, font=nl_f, fill=(226, 232, 240))
    ny += 36
gx = W - MX - boxw
d.rectangle([gx, map_y, gx + boxw, map_y + map_h], fill=PANEL)
d.text((gx + 18, map_y + 12), "ON THIS PAGE", font=bold(26), fill=NAVY)
gy = map_y + 52
gl_f = reg(23)
glance = ["Lead: the Gulf flare-up (No. 1)",
          "Asia - 43 stories (1-43)",
          "Europe - 35 stories (44-78)",
          "North America - 23 (79-101)",
          "South America - 10 (102-111)",
          "Africa - 20 stories (112-131)",
          "Oceania - 15 stories (132-146)",
          "World & Science - 4 (147-150)"]
for g in glance:
    d.text((gx + 18, gy), g, font=gl_f, fill=INK)
    gy += 27
mx0, mx1 = MX + boxw + 22, gx - 22
mw = mx1 - mx0
d.rectangle([mx0, map_y, mx1, map_y + map_h], fill=(238, 241, 244))
cw, ch = mw / GRID_W, map_h / GRID_H
r_dot = 3.0
for (c, r) in LAND_SET:
    cx, cy = mx0 + (c + 0.5) * cw, map_y + (r + 0.5) * ch
    d.ellipse([cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot], fill=LANDC)
for _, _, items in SECTIONS:
    for (_, _, lon, lat) in items:
        if lon is None:
            continue
        c, r = marker_cell(lon, lat)
        cx, cy = mx0 + (c + 0.5) * cw, map_y + (r + 0.5) * ch
        d.ellipse([cx - 6.5, cy - 6.5, cx + 6.5, cy + 6.5], fill=RED, outline=(255, 255, 255), width=2)
map_bot = map_y + map_h

# digest: numbered flow across 3 columns
zone_top = map_bot + 16
zone_bot = 1964
col_w = (W - 2 * MX - 2 * 28) // 3
col_x = [MX, MX + col_w + 28, MX + 2 * (col_w + 28)]
PITCH = 22
H_FONT = bold(20)
D_FONT = reg(20)
N_FONT = bold(20)
SEC_FONT = bold(22)
HEADER_H = 36

numbered = []
n = 0
for title, colour, items in SECTIONS:
    numbered.append(("H", title, colour, len(items)))
    for it in items:
        n += 1
        numbered.append(("I", n, colour, it))

col = 0
cy = zone_top
placed = 0
truncated = []
for entry in numbered:
    if entry[0] == "H":
        _, title, colour, count = entry
        if cy + HEADER_H + 3 * PITCH > zone_bot and col < 2:
            col += 1; cy = zone_top
        x = col_x[col]
        d.rectangle([x, cy, x + col_w, cy + 28], fill=colour)
        d.text((x + 10, cy + 3), f"{title} - {count} STORIES", font=SEC_FONT, fill=(255, 255, 255))
        cy += HEADER_H
    else:
        _, num, colour, (head, det, _lon, _lat) = entry
        if cy + PITCH > zone_bot and col < 2:
            col += 1; cy = zone_top
        x = col_x[col]
        num_s = f"{num}."
        d.text((x, cy), num_s, font=N_FONT, fill=colour)
        hx = x + tw(num_s, N_FONT) + 7
        d.text((hx, cy), head, font=H_FONT, fill=INK)
        dx = hx + tw(head, H_FONT) + 7
        avail = x + col_w - dx
        det_s = "- " + det
        if tw(det_s, D_FONT) > avail:
            while det_s and tw(det_s + "..", D_FONT) > avail:
                det_s = det_s[:-1]
            det_s = det_s.rstrip() + ".."
            truncated.append(num)
        if avail > 60:
            d.text((dx, cy), det_s, font=D_FONT, fill=DETAIL)
        cy += PITCH
        placed += 1
print("placed:", placed, "| last column:", col, "| truncated:", truncated)

# ticker + sources
ty = 1970
d.rectangle([0, ty, W, ty + 42], fill=INK)
tick_f = reg(22)
twk = tw(TICKER, tick_f)
if twk > W - 32:
    tick_f = reg(20); twk = tw(TICKER, tick_f)
d.text(((W - twk) / 2, ty + 9), TICKER, font=tick_f, fill=(255, 255, 255))
src_f = reg(20)
d.text(((W - tw(SOURCES, src_f)) / 2, ty + 48), SOURCES, font=src_f, fill=GREY)
print("layout bottom:", ty + 48 + 26, "of", H)

img = img.resize((1024, 1024), Image.LANCZOS)
# The rules accept PNG or JPEG (sniffed by first bytes; the file name
# stays entry.png). JPEG 4:4:4 keeps the small type crisp and the file
# well under the 1 MiB cap, where a PNG of this density overflows it.
img.save(OUT, format="JPEG", quality=90, subsampling=0, optimize=True)
print("wrote", OUT)
