#!/usr/bin/env python3
"""Remove the star and fork counters from a github-profile-3d-contrib SVG.

Everything else the action draws is left alone: the 3D calendar, the
language donut, the contribution radar, the contribution total and the
date range all stay exactly where the action put them.

The action offers no way to switch individual parts off -- BaseSettings
(src/type.ts) has no visibility flags, and create-svg.ts draws every part
unconditionally for the full render types -- so the counters are removed
from the generated SVG afterwards instead.

Elements are matched by STRUCTURE, never by child index or by value:

  * the footer is the group that contains the "contributions" label;
  * inside it, document order is
        <total> <"contributions"> <star icon> <count> <fork icon> <count>
    so the total PRECEDES the label and the two counters FOLLOW it.

That ordering is what distinguishes the total from a counter, so the
total is never removed no matter what number it happens to be. If the
upstream layout changes and the expected shape is not found, the file is
left untouched and a warning is printed -- a no-op, never a partial or
destructive edit.
"""
import re
import sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
S = '{%s}' % SVG
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')


def text_of(el):
    return ''.join(el.itertext()).strip()


def strip(path):
    tree = ET.parse(path)
    root = tree.getroot()

    footers = [g for g in root
               if g.tag == S + 'g'
               and any(c.tag == S + 'text' and text_of(c) == 'contributions'
                       for c in g)]
    if len(footers) != 1:
        return None, f'expected 1 footer group, found {len(footers)}'

    footer = footers[0]
    removed = 0
    seen_label = False
    for child in list(footer):
        if child.tag == S + 'text' and text_of(child) == 'contributions':
            seen_label = True
            continue
        if not seen_label:
            continue                      # the contribution total -- keep
        is_icon = (child.tag == S + 'g'
                   and 'scale(' in (child.get('transform') or ''))
        is_count = child.tag == S + 'text' and text_of(child).isdigit()
        if is_icon or is_count:
            footer.remove(child)
            removed += 1

    if removed == 0:
        return 0, 'no star/fork counters found'

    tree.write(path, xml_declaration=True, encoding='UTF-8')
    return removed, None


if __name__ == '__main__':
    failures = 0
    for path in sys.argv[1:]:
        try:
            removed, note = strip(path)
        except Exception as exc:                  # never fail the workflow
            print(f'{path}: SKIPPED ({exc})')
            failures += 1
            continue
        if removed is None:
            print(f'{path}: SKIPPED ({note})')
            failures += 1
        elif removed == 0:
            print(f'{path}: unchanged ({note})')
        else:
            print(f'{path}: removed {removed} star/fork elements')
    if failures:
        print(f'note: {failures} file(s) left untouched', file=sys.stderr)
