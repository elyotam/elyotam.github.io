#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite the styles and the stack section of about.html.

The 34 tools used to sit in one undifferentiated grid. They are now grouped,
which is the real upgrade on this page: a visitor can see the shape of the
skillset instead of counting logos. Each group carries its own colour, and the
page picks up the same accent system as the home page.

Run:  python tools/build_about.py     (from the site root)
"""

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# group, accent, tools -- every one of the 34 icons appears exactly once
GROUPS = [
    ("Systems &amp; security", "#6fb3e8", "rgba(75,139,190,.16)", [
        ("linux", "Linux"), ("windows", "Windows"), ("bash", "Bash"),
        ("fortinet", "Fortinet"), ("falcon", "CrowdStrike Falcon"),
        ("openvpn", "OpenVPN"), ("jumpcloud", "JumpCloud"), ("ninite", "Ninite"),
    ]),
    ("Build &amp; ship", "#7fd6de", "rgba(11,132,145,.18)", [
        ("git", "Git"), ("github", "GitHub"), ("githubactions", "GitHub Actions"),
        ("npm", "npm"), ("docker", "Docker"), ("kubernetes", "Kubernetes"),
        ("helm", "Helm"), ("argocd", "Argo CD"),
    ]),
    ("Cloud &amp; infrastructure", "#ffb877", "rgba(255,124,0,.16)", [
        ("aws", "AWS"), ("terraform", "Terraform"), ("ansible", "Ansible"),
        ("postgres", "PostgreSQL"), ("prometheus", "Prometheus"), ("grafana", "Grafana"),
    ]),
    ("Code &amp; design", "#bfa9ff", "rgba(139,104,224,.18)", [
        ("py", "Python"), ("vscode", "VS Code"), ("cursor", "Cursor"),
        ("claudecode", "Claude Code"), ("codex", "Codex"),
        ("antigravity", "Google Antigravity"), ("figma", "Figma"),
    ]),
    ("Business platforms", "#ffe27a", "rgba(255,212,59,.14)", [
        ("microsoft365", "Microsoft 365"), ("googleworkspace", "Google Workspace"),
        ("salesforce", "Salesforce"), ("voicenter", "Voicenter"), ("slack", "Slack"),
    ]),
]

STYLE = '''<style>
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap);padding-bottom:var(--gap)}

/* the same accent system the home page uses */
.tint::before{content:"";position:absolute;inset:0;z-index:0;border-radius:inherit;
  pointer-events:none;opacity:.55;transition:opacity .45s ease;
  background:
    radial-gradient(260px circle at var(--mx,110%) var(--my,-10%),var(--accent),transparent 68%),
    radial-gradient(125% 95% at 100% 0%,var(--accent),transparent 60%)}
.tint:hover::before{opacity:.9}
.shotcard{--accent:rgba(75,139,190,.22); --glow:rgba(122,181,231,.16)}
.card    {--accent:rgba(232,129,166,.18);--glow:rgba(244,166,215,.14)}
.cv.exp  {--accent:rgba(11,132,145,.22); --glow:rgba(64,196,207,.14);  --markhi:#7fd6de}
.cv.edu  {--accent:rgba(255,124,0,.18);  --glow:rgba(255,150,60,.13);  --markhi:#ffb877}
.social  {--accent:rgba(139,104,224,.22);--glow:rgba(160,130,238,.16); --markhi:#bfa9ff; --markglow:rgba(139,104,224,.5)}
.cta     {--accent:rgba(232,129,166,.20);--glow:rgba(244,166,215,.16); --markhi:#1b1b1b}
.stacklink{--accent:rgba(255,212,59,.17);--glow:rgba(255,212,59,.12);  --markhi:#ffe27a; --markglow:rgba(255,212,59,.35)}
.stackwrap{--glow:rgba(255,255,255,.05)}

/* ------------------------------------------------ row 1: portrait + summary */
.shotcard{grid-column:span 4;padding:14px;align-self:start}
/* height:auto is load-bearing. The <img> carries height="480" as an attribute,
   which the browser applies as a style, and it beat aspect-ratio -- the photo
   was being stretched to 480px tall at every column width. */
.shotcard img{width:100%;height:auto;aspect-ratio:380/480;object-fit:cover;
  object-position:center;border-radius:20px;display:block;
  transition:transform .6s cubic-bezier(.2,.7,.3,1)}
.shotcard:hover img{transform:scale(1.04)}
.summary{grid-column:span 8;display:flex;flex-direction:column;gap:18px;
  background:none;border:0;padding:0}
.summary:hover{transform:none}
.summary::after{display:none}
.bigtitle{margin:0;text-align:center;font-size:clamp(30px,5vw,50px);font-weight:800;
  letter-spacing:-1px;display:flex;align-items:center;justify-content:center;gap:18px}
.bigtitle span{background:linear-gradient(92deg,#e8e8e8,#a9a9a9 45%,#f0c8dd);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.bigtitle i{font-style:normal;color:#cfcfcf;font-size:.55em;opacity:.8}
.summary .card{flex:1;padding:60px 34px 32px}
.summary h2{margin:0 0 12px;font-size:27px;font-weight:500;
  background:linear-gradient(92deg,#f472b6,#a78bfa 48%,#60a5fa);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.summary p{margin:0;color:#c0c0c0;font-size:15.2px;line-height:1.78;max-width:66ch}
.spark{position:absolute;left:32px;top:22px;width:34px;height:42px;opacity:.85;z-index:2}
.spark svg{width:100%;height:100%;fill:#e9e9e9}
/* two lines of standing about what the work actually is */
.facts{display:flex;flex-wrap:wrap;gap:9px;margin:22px 0 0}
.facts span{font-size:12px;letter-spacing:.4px;text-transform:uppercase;color:#c9c9c9;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);
  border-radius:999px;padding:7px 14px}

/* ------------------------------------------ row 2: a timeline, not a list */
.cv{grid-column:span 6;padding:30px 32px}
.cv h3{margin:0 0 24px;font-size:13px;letter-spacing:1.1px;text-transform:uppercase;
  font-weight:600;color:var(--railhi,#cfcfcf)}
.cv.exp{--railhi:#7fd6de}
.cv.edu{--railhi:#ffb877}
.rail{position:relative;padding-left:26px}
.rail::before{content:"";position:absolute;left:5px;top:6px;bottom:6px;width:1px;
  background:linear-gradient(var(--railhi),rgba(255,255,255,.06))}
.entry{position:relative;margin-bottom:26px}
.entry:last-child{margin-bottom:0}
.entry::before{content:"";position:absolute;left:-26px;top:5px;width:11px;height:11px;
  border-radius:50%;background:#141414;border:1px solid var(--railhi);
  box-shadow:0 0 0 3px rgba(0,0,0,.5)}
.entry.now::before{background:var(--railhi);box-shadow:0 0 0 3px rgba(0,0,0,.5),
  0 0 12px var(--railhi)}
.entry .when{font-size:12.5px;color:var(--faint);margin:0 0 5px;letter-spacing:.3px}
.entry .what{font-size:16.4px;color:var(--fg);margin:0 0 4px;font-weight:500}
.entry .where{font-size:13.6px;color:#a4a4a4;margin:0}

/* ------------------------------------------------------------------ row 3 */
.social{grid-column:span 3;min-height:200px;display:flex;flex-direction:column;justify-content:flex-end}
.orbwrap{position:absolute;left:24px;right:24px;top:24px;display:flex;gap:14px}
.orb{position:relative;z-index:10;width:58px;height:58px;border-radius:50%;background:#141414;
  border:1px solid #2e2e2e;display:grid;place-items:center;transition:.2s}
.orb:hover{background:#fff;border-color:#fff;transform:translateY(-3px)}
.orb:hover img{filter:invert(1)}
.orb img{width:25px;height:25px}
.cta{grid-column:span 5;min-height:200px;display:flex;flex-direction:column;justify-content:center;padding:32px}
.cta h2{margin:30px 0 0;font-size:clamp(26px,3.6vw,38px);font-weight:400;line-height:1.16;letter-spacing:-.8px}
.grad{background:linear-gradient(90deg,#f472b6,#a78bfa 45%,#60a5fa);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.stacklink{grid-column:span 4;min-height:200px;display:flex;flex-direction:column;justify-content:flex-end}
.stacklink .row{position:absolute;left:26px;right:26px;top:30px;display:flex;flex-wrap:wrap;gap:8px}
.stacklink .row img{width:34px;height:34px;border-radius:9px;
  transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.stacklink:hover .row img{transform:translateY(-3px)}
.stacklink .row img:nth-child(2){transition-delay:.03s}
.stacklink .row img:nth-child(3){transition-delay:.06s}
.stacklink .row img:nth-child(4){transition-delay:.09s}
.stacklink .row img:nth-child(5){transition-delay:.12s}
.stacklink .row img:nth-child(6){transition-delay:.15s}

/* -------------------------------------------------------------- the stack */
.stackwrap{grid-column:span 12;padding:34px 34px 38px}
.stackwrap h3{margin:0 0 6px;font-size:23px;font-weight:500;letter-spacing:-.3px}
.stackwrap > p{margin:0 0 30px;color:var(--dim);font-size:14.6px}
.grp{margin-bottom:30px}
.grp:last-child{margin-bottom:0}
.grp h4{display:flex;align-items:center;gap:12px;margin:0 0 16px;
  font-size:12px;letter-spacing:1.1px;text-transform:uppercase;font-weight:600;
  color:var(--c)}
.grp h4::after{content:"";flex:1;height:1px;
  background:linear-gradient(90deg,var(--line),transparent)}
.grp h4 b{font-weight:500;color:var(--faint);letter-spacing:.4px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(94px,1fr));gap:12px}
.tiles a{display:flex;flex-direction:column;align-items:center;gap:9px;padding:15px 6px;
  border-radius:16px;border:1px solid transparent;position:relative;
  transition:transform .22s cubic-bezier(.2,.7,.3,1),background .22s,border-color .22s}
.tiles a::before{content:"";position:absolute;inset:0;border-radius:inherit;opacity:0;
  transition:opacity .25s;
  background:radial-gradient(70% 60% at 50% 0%,var(--c),transparent 70%)}
.tiles a:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.1);
  background:rgba(255,255,255,.03)}
.tiles a:hover::before{opacity:1}
.tiles img{width:46px;height:46px;border-radius:11px;position:relative;z-index:1;
  transition:filter .25s}
.tiles a:hover img{filter:drop-shadow(0 6px 14px var(--c))}
.tiles span{font-size:11.5px;color:var(--dim);text-align:center;line-height:1.3;
  position:relative;z-index:1;transition:color .2s}
.tiles a:hover span{color:var(--fg)}

@media (max-width:980px){
  .shotcard{grid-column:span 5}.summary{grid-column:span 7}
  .cv{grid-column:span 12}
  .social,.stacklink{grid-column:span 6}.cta{grid-column:span 12}
}
@media (max-width:680px){
  .shotcard,.summary,.social,.cta,.stacklink{grid-column:span 12}
  .stackwrap{padding:26px 20px 30px}
  .tiles{grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:9px}
  .tiles img{width:40px;height:40px}
}
</style>'''


def stack_html():
    out = []
    for name, colour, tint, tools in GROUPS:
        tiles = "".join(
            '<a title="%s"><img src="assets/icons/%s.svg" alt="" loading="lazy">'
            '<span>%s</span></a>' % (label, slug, label)
            for slug, label in tools)
        out.append(
            '        <div class="grp" style="--c:%s">\n'
            '          <h4>%s <b>%d</b></h4>\n'
            '          <div class="tiles" style="--c:%s">%s</div>\n'
            '        </div>' % (colour, name, len(tools), tint, tiles))
    return "\n".join(out)


def main():
    p = os.path.join(ROOT, "about.html")
    h = io.open(p, encoding="utf-8").read()

    a = h.index("<style>")
    b = h.index("</style>") + len("</style>")
    h = h[:a] + STYLE + h[b:]

    # the grid replaces the single flat tile wall
    h = h.replace('      <div class="tiles" id="tiles"></div>',
                  stack_html())

    # The tiles are written into the HTML above, so the page script only has the
    # peek row left to fill. Replace the whole inline block rather than deleting
    # statements out of it -- surgical removals left orphaned `}).join('');`
    # fragments that broke the script and stopped the peek row rendering at all.
    PEEK = ("linux docker kubernetes terraform aws py "
            "github grafana ansible helm argocd postgres").split()
    script = (
        "<script>\n"
        "var PEEK = [%s];\n"
        "document.getElementById('peek').innerHTML = PEEK.map(function (t) {\n"
        "  return '<img src=\"assets/icons/' + t + '.svg\" alt=\"\" loading=\"lazy\">';\n"
        "}).join('');\n"
        "</script>\n" % ",".join("'%s'" % t for t in PEEK))
    h, n = re.subn(r"<script>\nvar STACK = \[.*?</script>\n", script, h, flags=re.S)
    assert n == 1, "expected one inline stack script, replaced %d" % n

    # accent hooks on the cards
    for old, new in [
        ('class="box shotcard reveal"', 'class="box shotcard tint reveal"'),
        ('class="box card reveal"', 'class="box card tint reveal"'),
        ('class="box social reveal"', 'class="box social tint reveal"'),
        ('class="box cta reveal"', 'class="box cta tint reveal"'),
        ('class="box stacklink reveal"', 'class="box stacklink tint reveal"'),
        ('class="box stackwrap reveal"', 'class="box stackwrap reveal"'),
    ]:
        h = h.replace(old, new)

    # the two cv cards need to be told apart
    first = h.index('class="box cv reveal"')
    h = h[:first] + h[first:].replace('class="box cv reveal"',
                                      'class="box cv exp tint reveal"', 1)
    h = h.replace('class="box cv reveal"', 'class="box cv edu tint reveal"', 1)

    # Each run of .entry blocks becomes a rail. Matching the whole run and
    # rewriting it in one go is what keeps the closing </div> from going
    # missing, which is exactly what happened when the open and the close were
    # two separate replaces.
    def rail(m):
        body = m.group(1)
        for live in ("Present", "Ongoing"):
            body = body.replace(
                '<div class="entry">\n        <p class="when">%s<' % live,
                '<div class="entry now">\n        <p class="when">%s<' % live)
        return '      <div class="rail">\n%s      </div>\n' % body

    h, n = re.subn(r'(?<=</h3>\n)((?:      <div class="entry">.*?\n      </div>\n)+)',
                   rail, h, flags=re.S)
    assert n == 2, "expected two rails, wrapped %d" % n

    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(h)
    print("about.html rebuilt: %d groups, %d tools"
          % (len(GROUPS), sum(len(g[3]) for g in GROUPS)))


if __name__ == "__main__":
    main()
