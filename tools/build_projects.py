#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the cards on projects.html.

The layout follows the reference projects page: three to a row, the shot on
top with the card's own corner radius, then category / name / one line, and a
spark button that comes up on hover. The filter bar and the corner badges are
ours and stay.

Run:  python tools/build_projects.py     (from the site root)
"""

import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPARK = (
    '<svg viewBox="0 0 46 42" fill="none" aria-hidden="true">'
    '<path d="M30.9224 21.2014C25.1291 21.2014 24.618 24.7796 24.618 27.3354C24.618 21.5421 '
    '21.5509 21.2014 17.9727 21.2014C24.618 21.2014 24.618 17.2824 24.618 14.8969C24.618 '
    '20.3494 27.8554 21.2014 30.9224 21.2014Z" fill="currentColor" stroke="currentColor"/>'
    '<rect y="21.6981" width="1" height="18" transform="rotate(-90 0 21.6981)" fill="currentColor"/>'
    '<path d="M9.93715 16.8555C10.9514 13.0701 13.2829 9.77074 16.5123 7.55063C19.7417 5.33052 '
    '23.6571 4.33531 27.5547 4.74394C31.4522 5.15258 35.0762 6.93825 37.7749 9.77989C40.4736 '
    '12.6215 42.07 16.3327 42.2771 20.2461C42.4842 24.1596 41.2884 28.0185 38.9047 31.1291C36.5211 '
    '34.2398 33.1059 36.398 29.2732 37.2157C25.4406 38.0335 21.4419 37.4571 17.9962 35.5903C14.5505 '
    '33.7234 11.8839 30.6886 10.4757 27.0314" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round"/></svg>'
)

GH = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .3a12 12 0 0 0-3.8 '
    '23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 '
    '1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2 0-.3-.5-1.5.2-3.2 '
    '0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 '
    '4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>'
)

# category, kicker, title, one line, href, artwork, badges, repo
PROJECTS = [
    ("web", "Client work", "Moshe Stern, CPA",
     "Eleven pages, four working tax calculators, no framework.",
     "https://elyotam.github.io/cpa-ms/",
     ("img", "assets/work/cpa-ms.jpg"),
     [("live", "Live")], "elyotam/cpa-ms"),

    ("web", "Marketing site", "CODE92",
     "Dark and motion-led, fully right-to-left.",
     "https://elyotam.github.io/code92-website/",
     ("img", "assets/work/code92-website.jpg"),
     [("live", "Live")], "elyotam/code92-website"),

    ("web", "Client work", "Ahuvit Mor",
     "A boutique cake studio, warm and image-led.",
     "https://elyotam.github.io/ahuvit-website/",
     ("img", "assets/work/ahuvit-website.jpg"),
     [("live", "Live")], "elyotam/ahuvit-website"),

    ("web", "Studio site", "Elyotam",
     "A cinematic opening that reveals itself as you scroll.",
     "https://elyotam.github.io/elyotam-website/",
     ("img", "assets/work/elyotam-website.jpg"),
     [("live", "Live")], "elyotam/elyotam-website"),

    ("infra", "Terraform module", "OpenVPN on AWS",
     "Builds Access Server without putting a secret in state.",
     "openvpn.html",
     ("glyph", "assets/icons/terraform.svg",
      "radial-gradient(120% 120% at 30% 20%,#2a1f3d,#141019 60%,#0d0d0d)"),
     [("doc", "Readme")], "elyotam/aws-openvpn"),

    ("infra", "Flask + Kubernetes", "QuakeWatch",
     "Live USGS earthquake data, shipped all the way to a cluster.",
     "quakewatch.html",
     ("glyph", "assets/icons/kubernetes.svg",
      "radial-gradient(120% 120% at 70% 25%,#123040,#0f2027 55%,#0d0d0d)"),
     [("doc", "Readme")], "elyotam/quakewatch-final-project"),

    ("infra", "Course archive", "DevOps Experts",
     "Fourteen lessons from the course, one script each.",
     "devops-experts.html",
     ("glyph", "assets/icons/docker.svg",
      "radial-gradient(120% 120% at 40% 25%,#2b2410,#1a1608 55%,#0d0d0d)"),
     [("doc", "Readme")], "elyotam/devops-experts"),

    ("shop", "Etsy shop", "ColorCatt",
     "My shop — the artwork, the listings and the storefront.",
     "https://www.etsy.com/shop/ColorCatt",
     ("img", "assets/work/etsy.svg"),
     [("live", "Open")], None),
]

CARD = '''    <article class="box work reveal" data-cat="{cat}">
      <a class="overlay" href="{href}"{rel} aria-label="{title}"></a>
      <div class="{cls}"{style}>
        <div class="badge">{badges}</div>
        {art}
      </div>
      <div class="info">
        <div>
          <p class="cat">{kicker}</p>
          <h2>{title}</h2>
          <p class="line">{line}</p>
        </div>
        <div class="pbtns">{src}<a class="pbtn" href="{href}"{rel} aria-label="Open {title}">{spark}</a></div>
      </div>
    </article>
'''


def card(cat, kicker, title, line, href, art, badges, repo):
    rel = ' rel="noopener"' if href.startswith("http") else ''
    if art[0] == "img":
        markup = '<img src="%s" alt="%s" loading="lazy">' % (art[1], title)
        cls, style = "canvas", ""
    else:
        markup = '<img src="%s" alt="">' % art[1]
        cls, style = "canvas glyph", ' style="background:%s"' % art[2]
    src = ''
    if repo:
        src = ('<a class="pbtn gh" href="https://github.com/%s" rel="noopener" '
               'aria-label="%s on GitHub">%s</a>' % (repo, title, GH))
    return CARD.format(cat=cat, href=href, rel=rel, title=title, cls=cls, style=style,
                       badges="".join('<span class="%s">%s</span>' % b for b in badges),
                       art=markup, kicker=kicker, line=line, src=src, spark=SPARK)


STYLE = '''<style>
.head{padding:6px 0 26px;text-align:center}
.bigtitle{margin:0 0 12px;font-size:clamp(30px,5vw,50px);font-weight:800;letter-spacing:-1px;
  display:flex;align-items:center;justify-content:center;gap:18px}
.bigtitle span{background:linear-gradient(92deg,#e8e8e8,#a9a9a9 45%,#f0c8dd);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.bigtitle i{font-style:normal;color:#cfcfcf;font-size:.55em;opacity:.8}
.head p{margin:0 auto;color:var(--dim);max-width:62ch}

.filters{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;padding:0 0 34px}
.filters button{font:inherit;font-size:13.5px;font-weight:500;letter-spacing:.3px;cursor:pointer;
  padding:9px 18px;border-radius:999px;color:var(--dim);background:#171717;
  border:1px solid #262626;transition:.2s}
.filters button:hover{color:var(--fg);border-color:#3a3a3a}
.filters button[aria-pressed="true"]{background:#f4f4f4;color:#111;border-color:#f4f4f4}

/* Three to a row, the way his projects page is laid out. */
.works{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--gap);padding-bottom:10px}
.work{padding:16px 16px 26px;display:flex;flex-direction:column;height:100%}
.works{align-items:stretch}
/* .work sets display, which outranks the browser's [hidden] rule, so the
   filter had no effect at all until this line existed */
.work[hidden]{display:none}

/* his cards zoom in rather than slide up, and they do it again after a filter */
.works .reveal{transform:scale(.6);
  transition:opacity .5s ease,transform .5s cubic-bezier(.19,.9,.32,1)}
.works .reveal.in{transform:none}

.canvas{position:relative;border-radius:var(--r);overflow:hidden;background:#0d0d0d;
  margin-bottom:13px}
.canvas img{width:100%;aspect-ratio:7/6;object-fit:cover;object-position:top;
  border-radius:var(--r);display:block;transition:transform .6s cubic-bezier(.2,.7,.3,1)}
.work:hover .canvas img{transform:scale(1.05)}
.glyph{display:grid;place-items:center;aspect-ratio:7/6}
.glyph img{width:88px !important;height:88px !important;aspect-ratio:auto !important;
  border-radius:20px;object-fit:contain}
.badge{position:absolute;top:14px;left:14px;display:flex;gap:7px;z-index:3}
.badge span{font-size:10.5px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;
  padding:5px 11px;border-radius:999px;
  background:rgba(10,10,10,.66);border:1px solid rgba(255,255,255,.16);color:#e9e9e9}
.badge .live{background:rgba(18,58,30,.78);border-color:rgba(80,220,120,.4);color:#7ee89a}
.badge .doc{background:rgba(24,44,66,.8);border-color:rgba(75,139,190,.45);color:#9dc6e8}

.info{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;
  padding:0 4px;flex:1}
.cat{margin:5px 0 2px;font-size:13px;letter-spacing:.4px;text-transform:uppercase;
  color:#bcbcbc;opacity:.5}
.work h2{margin:0;font-size:21px;font-weight:500;letter-spacing:-.3px;color:#fff;opacity:.9}
.line{margin:7px 0 0;font-size:13.8px;line-height:1.6;color:var(--dim);text-wrap:balance}
.pbtns{display:flex;align-items:center;gap:4px;position:relative;z-index:10;flex:0 0 auto}
.pbtn{display:block;color:#f4f4f4;opacity:.2;transition:opacity .3s}
.pbtn svg{width:46px;height:42px;display:block}
.pbtn.gh svg{width:19px;height:19px;margin:0 6px}
.work:hover .pbtn{opacity:.5}
.work:hover .pbtn:hover{opacity:1}

@media (max-width:1000px){ .works{grid-template-columns:repeat(2,1fr)} }
@media (max-width:660px){ .works{grid-template-columns:1fr} }
</style>'''


def main():
    p = os.path.join(ROOT, "projects.html")
    h = io.open(p, encoding="utf-8").read()

    a = h.index("<style>")
    b = h.index("</style>") + len("</style>")
    h = h[:a] + STYLE + h[b:]

    a = h.index('<main class="works" id="works">')
    a = h.index("\n", a) + 1
    b = h.index("  </main>")
    h = h[:a] + "\n" + "\n".join(card(*q) for q in PROJECTS) + h[b:]

    io.open(p, "w", encoding="utf-8", newline="\n").write(h)
    print("projects.html rebuilt: %d cards" % len(PROJECTS))


if __name__ == "__main__":
    main()
