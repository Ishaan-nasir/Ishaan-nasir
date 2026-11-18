"""Check each shipped site and redraw assets/live.svg (green = responding, grey = down)."""
import json, urllib.request
from xml.sax.saxutils import escape

GREEN, GREY, MUTED = "#3fb950", "#555555", "#9c9c9c"
PULSE = '<animate attributeName="opacity" values="1;.35;1" dur="2.4s" begin="-{b}s" repeatCount="indefinite"/>'

def up(url):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (profile status check)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status < 400:
                    return True
        except Exception:
            pass
    return False

sites = json.load(open(".github/live/sites.json"))
svg = open(".github/live/tile.svg.tmpl").read()
live = []
for i, s in enumerate(sites):
    ok = up(s["url"])
    live.append(ok)
    svg = (svg.replace(f"{{{{DOT{i}}}}}", GREEN if ok else GREY)
              .replace(f"{{{{ANIM{i}}}}}", PULSE.format(b=round(i * 0.45, 2)) if ok else "")
              .replace(f"{{{{KIND{i}}}}}", s["kind"] if ok else "down"))
n = sum(live)
alt = "Live sites: " + ", ".join(f'{s["name"]} {"up" if ok else "down"}' for s, ok in zip(sites, live))
svg = (svg.replace("{{COUNT}}", f"{n}/{len(sites)}")
          .replace("{{COUNTFILL}}", GREEN if n == len(sites) else MUTED)
          .replace("{{ALT}}", escape(alt, {'"': "&quot;"})))
open("assets/live.svg", "w").write(svg)
print(alt)
