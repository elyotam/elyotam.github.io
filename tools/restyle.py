#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the restrained design system across every page.

The site had grown twelve hues -- teal, orange, violet, pink, magenta, yellow,
green -- one per card. This strips that back to a single neutral scale plus one
cool accent, and replaces the ornamental corner spark with a plain arrow.

Run:  python tools/restyle.py     (from the site root)
"""

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))

ARROW = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
         '<path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

FOOTER = '''<footer>
  <div class="inner">
    <nav>
      <a href="{home}">Home</a><a href="{about}">About</a>
      <a href="{projects}">Projects</a><a href="{contact}">Contact</a>
    </nav>
    <div><span id="yr">2026</span> &copy; Elyotam Cohen</div>
  </div>
</footer>'''


def swap_corner_mark(h):
    """The spark was decoration. An arrow says the card goes somewhere."""
    return re.sub(r'<svg viewBox="0 0 46 42".*?</svg>', ARROW, h, flags=re.S)


def swap_footer(h, absolute):
    p = "/" if absolute else "./"
    new = FOOTER.format(home=p,
                        about=("/about.html" if absolute else "about.html"),
                        projects=("/projects.html" if absolute else "projects.html"),
                        contact=("/contact.html" if absolute else "contact.html"))
    return re.sub(r'<footer>.*?</footer>', new, h, flags=re.S)


def drop_card_colour(h):
    """Every per-card accent, glow and mark colour goes; the cards are uniform
    now and tell themselves apart by what is in them."""
    # the whole colour table on the home page
    h = re.sub(r'\.id\s*\{--accent.*?\.ticker\s*\{--glow:[^}]*\}\n', '', h, flags=re.S)
    # the about page's table
    h = re.sub(r'\.shotcard\{--accent.*?\.stackwrap\{--glow:[^}]*\}\n', '', h, flags=re.S)
    # coloured kickers
    h = re.sub(r'\.(about|showcase|hobby|social) \.kicker\{color:#[0-9a-f]{6}\}\n', '', h)
    # the tint layer itself
    h = re.sub(r'/\* Every card was the same grey.*?\.tint:hover::before\{opacity:\.9\}\n',
               '', h, flags=re.S)
    h = re.sub(r'/\* the same accent system the home page uses \*/\n'
               r'\.tint::before\{.*?\.tint:hover::before\{opacity:\.9\}\n', '', h, flags=re.S)
    h = re.sub(r'/\* a second, brighter pool.*?transparent 60%\)\}\n', '', h, flags=re.S)
    h = h.replace(' tint reveal"', ' reveal"')
    return h


def main():
    for f in PAGES:
        p = os.path.join(ROOT, f)
        h = io.open(p, encoding="utf-8").read()
        before = h
        absolute = f == "404.html"          # served from any depth
        h = swap_corner_mark(h)
        h = swap_footer(h, absolute)
        h = drop_card_colour(h)
        if h != before:
            io.open(p, "w", encoding="utf-8", newline="\n").write(h)
            print("  %-22s updated" % f)
        else:
            print("  %-22s unchanged" % f)


if __name__ == "__main__":
    main()
