#!/usr/bin/env python3
"""Strip radar chart, language donut and star/fork counts from a
github-profile-3d-contrib SVG, then tighten the viewBox.

Elements are matched by STRUCTURE (a group containing class="radar";
a group containing language labels), never by child index, so an
upstream layout change degrades to "didn't strip" rather than
"deleted the calendar".
"""
import re, sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
S = '{%s}' % SVG
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

LANGS = ('Python', 'TypeScript', 'Java', 'MQL5', 'JavaScript', 'other')
MARGIN = 14   # covers skewX/skewY/scale that a translate-only bbox misses


def text_of(el):
    return ''.join(el.itertext()).strip()


def translate(el):
    m = re.search(r'translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)', el.get('transform') or '')
    return (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)


def bbox(el, ox=0.0, oy=0.0, out=None):
    if out is None:
        out = []
    dx, dy = translate(el)
    ox += dx; oy += dy
    tag = el.tag.replace(S, '')
    if tag == 'rect' and el.get('class') != 'fill-bg':
        x, y = float(el.get('x', 0)), float(el.get('y', 0))
        out.append((ox + x, oy + y))
        out.append((ox + x + float(el.get('width', 0)), oy + y + float(el.get('height', 0))))
    elif tag == 'text':
        m = re.search(r'font-size:\s*([\d.]+)', el.get('style') or '')
        fs = float(m.group(1)) if m else 12.0
        x, y = float(el.get('x', 0)), float(el.get('y', 0))
        w = len(text_of(el)) * fs * 0.6
        a = el.get('text-anchor', 'start')
        x0 = x - w if a == 'end' else (x - w / 2 if a == 'middle' else x)
        out.append((ox + x0, oy + y - fs))
        out.append((ox + x0 + w, oy + y + fs * 0.35))
    for c in el:
        bbox(c, ox, oy, out)
    return out


def strip(path):
    tree = ET.parse(path)
    root = tree.getroot()
    kids = list(root)
    removed = []

    # --- radar: the group that contains the radar polygon ---
    for g in kids:
        if g.tag == S + 'g' and any(c.get('class') == 'radar' for c in g.iter()):
            root.remove(g); removed.append('radar')

    # --- donut: the group that contains language labels ---
    for g in list(root):
        if g.tag == S + 'g' and any(text_of(c) in LANGS for c in g.iter()):
            root.remove(g); removed.append('pie')

    # --- footer: drop star/fork icon+count, keep total and date range ---
    date_text = None
    for g in list(root):
        if g.tag != S + 'g' or not any('contributions' in text_of(c) for c in g):
            continue
        # Document order is: <total> <"contributions"> <star icon> <count>
        # <fork icon> <count> <date range>.  The total PRECEDES its label;
        # the star/fork counts FOLLOW it.  Use that ordering rather than
        # position or value, so the total is never mistaken for a count.
        seen_label = False
        for c in list(g):
            t = text_of(c)
            if c.tag == S + 'text' and t == 'contributions':
                seen_label = True
                continue
            if c.tag == S + 'text' and re.match(r'^\d{4}-\d{2}-\d{2}\s*/', t):
                date_text = c
                continue
            if not seen_label:
                continue                      # the contribution total - keep
            icon = c.tag == S + 'g' and 'scale(' in (c.get('transform') or '')
            count = c.tag == S + 'text' and t.isdigit()
            if icon or count:
                g.remove(c); removed.append('star/fork')

    # --- reflow the date range down to the footer row, freeing the top band ---
    if date_text is not None:
        baseline = max((float(c.get('y', 0)) for g in root for c in g
                        if c.tag == S + 'text' and text_of(c) == 'contributions'), default=None)
        if baseline:
            date_text.set('y', str(baseline))
            removed.append('date->footer')

    # --- tighten viewBox to what is left ---
    pts = bbox(root)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0 = max(0.0, min(xs) - MARGIN); y0 = max(0.0, min(ys) - MARGIN)
    x1 = max(xs) + MARGIN; y1 = max(ys) + MARGIN
    w, h = round(x1 - x0), round(y1 - y0)
    root.set('viewBox', f'{x0:.0f} {y0:.0f} {w} {h}')
    root.set('width', str(w)); root.set('height', str(h))
    for c in root:
        if c.get('class') == 'fill-bg':
            c.set('x', f'{x0:.0f}'); c.set('y', f'{y0:.0f}')
            c.set('width', str(w)); c.set('height', str(h))

    tree.write(path, xml_declaration=True, encoding='UTF-8')
    return removed, (w, h)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        try:
            removed, size = strip(p)
        except Exception as e:                      # never fail the workflow
            print(f'{p}: SKIPPED ({e})'); continue
        if 'radar' not in removed or 'pie' not in removed:
            print(f'{p}: WARNING partial strip -> {removed}')
        print(f'{p}: {sorted(set(removed))} -> {size[0]}x{size[1]}')
