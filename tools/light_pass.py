#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the contact page, the 404 and the README pages onto the light theme."""

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTACT = '''<style>
.grid{display:grid;grid-template-columns:1fr 1.35fr;gap:70px;
  padding:56px 0 20px;align-items:start}
.grid > *{min-width:0}

.rail h3{margin:0 0 14px;font-size:11px;letter-spacing:1.6px;text-transform:uppercase;
  color:var(--faint);font-weight:600}
.rail p{margin:0 0 38px;color:var(--dim);font-size:15.5px;line-height:1.75;max-width:34ch}
.orbs{display:flex;gap:14px}
.orb{display:grid;place-items:center;width:38px;height:38px;border:1px solid var(--line);
  border-radius:3px;background:var(--surface);transition:border-color .2s,transform .2s}
.orb:hover{border-color:var(--fg);transform:translateY(-2px)}
.orb img{width:19px;height:19px;border-radius:4px}

.formcard{padding:0;background:none;border:0}
.formcard:hover{box-shadow:none;border:0}
.formcard h1{margin:0 0 30px;font-family:var(--serif);font-weight:400;
  font-size:clamp(38px,5.6vw,64px);letter-spacing:-.015em;line-height:1.05}
.formcard h1 .accent{color:var(--accent);font-style:italic}
.f{display:flex;flex-direction:column;gap:0}
.f input,.f textarea{
  width:100%;background:none;border:0;border-bottom:1px solid var(--line);
  padding:16px 2px;color:var(--fg);font:inherit;font-size:16px;transition:border-color .2s;
}
.f textarea{min-height:110px;resize:vertical}
.f input::placeholder,.f textarea::placeholder{color:var(--faint)}
.f input:focus,.f textarea:focus{outline:none;border-bottom-color:var(--fg)}
.f button{
  margin-top:30px;align-self:flex-start;padding:13px 30px;border-radius:3px;
  border:1px solid var(--fg);background:var(--fg);color:var(--bg);font:inherit;
  font-size:14.5px;font-weight:500;cursor:pointer;transition:background .2s}
.f button:hover{background:#000}
.f button:disabled{opacity:.5;cursor:default}
.notice{margin:0 0 26px;padding:14px 16px;border-radius:3px;font-size:14px;
  background:var(--accent-soft);border:1px solid #cddbe4;color:var(--accent)}
.notice a{text-decoration:underline}
.hint{margin:16px 0 0;font-size:13.5px;color:var(--faint)}
.hint a{color:var(--accent)}

@media (max-width:900px){ .grid{grid-template-columns:1fr;gap:44px;padding-top:38px} }
</style>'''

FOUR = '''<style>
.lost{padding:110px 0 130px}
.code{font-family:var(--serif);font-size:clamp(80px,16vw,168px);font-weight:400;
  line-height:.9;letter-spacing:-.03em;color:var(--fg)}
.lost h1{margin:26px 0 12px;font-family:var(--serif);font-size:clamp(24px,3.4vw,34px);
  font-weight:400;letter-spacing:-.01em}
.lost p{margin:0 0 34px;color:var(--dim);font-size:16px;max-width:46ch;line-height:1.7}
.ways{display:flex;gap:12px;flex-wrap:wrap}
.way{display:inline-flex;align-items:center;padding:12px 22px;border-radius:3px;
  border:1px solid var(--fg);font-size:14.5px;font-weight:500;
  transition:background .2s,color .2s}
.way:hover{background:var(--fg);color:var(--bg)}
.way.key{background:var(--fg);color:var(--bg)}
.way.key:hover{background:#000;border-color:#000}
@media (max-width:680px){ .lost{padding:70px 0 90px} }
</style>'''

# readme.css: every dark surface swapped for its light counterpart
README = [
    ('.readme{padding:0;overflow:hidden}',
     '.readme{padding:0;overflow:hidden;background:var(--surface);'
     'border:1px solid var(--line);border-radius:3px}'),
    ('padding:14px 22px;background:#161616;border-bottom:1px solid var(--line);',
     'padding:14px 22px;background:var(--sunk);border-bottom:1px solid var(--line);'),
    ('font-weight:500;color:#d6d6d6}', 'font-weight:500;color:var(--fg)}'),
    ('font-size:15.4px;line-height:1.72;color:#c2c2c2;word-wrap:break-word;',
     'font-size:15.6px;line-height:1.75;color:var(--dim);word-wrap:break-word;'),
    ('padding-bottom:12px;border-bottom:1px solid #262626}',
     'padding-bottom:12px;border-bottom:1px solid var(--line)}'),
    ('padding-bottom:10px;border-bottom:1px solid #232323;margin-top:38px}',
     'padding-bottom:10px;border-bottom:1px solid var(--line);margin-top:38px}'),
    ('background:#17171b;border:1px solid var(--line);border-radius:5px;',
     'background:var(--sunk);border:1px solid var(--line);border-radius:3px;'),
    ('padding:.14em .42em;color:#cfd4da;white-space:break-spaces}',
     'padding:.14em .42em;color:#1d4b3a;white-space:break-spaces}'),
    ('.markdown-body pre{background:#101013;border:1px solid var(--line);border-radius:12px;',
     '.markdown-body pre{background:var(--sunk);border:1px solid var(--line);border-radius:3px;'),
    ('line-height:1.75;color:#cfd4da;white-space:pre}',
     'line-height:1.72;color:#2a2a24;white-space:pre}'),
    ('border:1px solid #262626;padding:10px 15px;text-align:inherit;vertical-align:top}',
     'border:1px solid var(--line);padding:10px 15px;text-align:inherit;vertical-align:top}'),
    ('.markdown-body th{background:#191919;', '.markdown-body th{background:var(--sunk);'),
    ('.markdown-body tbody tr:nth-child(even) td{background:#151515}',
     '.markdown-body tbody tr:nth-child(even) td{background:#fcfbf9}'),
    ('border-left:3px solid #2f3d4a;background:#151a20;',
     'border-left:2px solid var(--accent);background:var(--sunk);'),
    ('border-radius:0 12px 12px 0;padding:12px 20px;color:#a5a5a5}',
     'border-radius:0 3px 3px 0;padding:12px 20px;color:var(--dim)}'),
    ('.markdown-body hr{border:0;border-top:1px solid #242424;margin:30px 0}',
     '.markdown-body hr{border:0;border-top:1px solid var(--line);margin:30px 0}'),
    ('border-radius:12px;\n  background:#171717;', 'border-radius:4px;\n  background:var(--sunk);'),
    ('.markdown-body details{background:#161616;border:1px solid #242424;\n  border-radius:14px;',
     '.markdown-body details{background:var(--sunk);border:1px solid var(--line);\n  border-radius:3px;'),
    ('.markdown-body kbd{background:#1d1d1d;border:1px solid #333;',
     '.markdown-body kbd{background:var(--surface);border:1px solid var(--line);'),
    ('border-radius:11px;border:1px solid #2a2a2a;background:#151515;\n  font-size:13.5px;color:var(--dim);transition:.2s}',
     'border-bottom:1px solid var(--line);font-size:13.5px;color:var(--dim);transition:.2s}'),
    ('.back:hover{color:var(--fg);border-color:#3f3f3f;background:#1b1b1b}',
     '.back:hover{color:var(--fg);border-color:var(--fg)}'),
    ('white-space:nowrap;color:#c9c9c9;\n  background:#1f1f1f;border:1px solid #303030;border-radius:999px;',
     'white-space:nowrap;color:var(--dim);\n  background:var(--surface);border:1px solid var(--line);border-radius:2px;'),
    ('.rm-lang:hover{background:#2a2a2a;border-color:#474747;color:#fff}',
     '.rm-lang:hover{border-color:var(--fg);color:var(--fg)}'),
    # the GitHub alert callouts
    ('.markdown-body .markdown-alert{border-left:3px solid #2f3d4a;background:#151a20;\n  border-radius:0 12px 12px 0;',
     '.markdown-body .markdown-alert{border-left:2px solid var(--accent);background:var(--sunk);\n  border-radius:0 3px 3px 0;'),
    ('.markdown-body .markdown-alert-warning{border-color:#6d5a2a;background:#1b1710}',
     '.markdown-body .markdown-alert-warning{border-color:#b08a2e;background:#fbf7ec}'),
    ('.markdown-body .markdown-alert-caution{border-color:#6b3030;background:#1b1414}',
     '.markdown-body .markdown-alert-caution{border-color:#a84a4a;background:#fcf1f1}'),
    ('.markdown-body .markdown-alert-tip{border-color:#2c5c3f;background:#131a16}',
     '.markdown-body .markdown-alert-tip{border-color:#3d7a55;background:#f0f7f2}'),
]


def main():
    for f, css in (("contact.html", CONTACT), ("404.html", FOUR)):
        p = os.path.join(ROOT, f)
        h = io.open(p, encoding="utf-8").read()
        h2, n = re.subn(r"<style>.*?</style>", css, h, count=1, flags=re.S)
        assert n == 1, f
        io.open(p, "w", encoding="utf-8").write(h2)
        print("  %-14s restyled" % f)

    p = os.path.join(ROOT, "assets", "readme.css")
    c = io.open(p, encoding="utf-8").read()
    hit = 0
    for a, b in README:
        if a in c:
            c = c.replace(a, b)
            hit += 1
    io.open(p, "w", encoding="utf-8", newline="\n").write(c)
    print("  readme.css     %d/%d rules moved to light" % (hit, len(README)))


if __name__ == "__main__":
    main()
