#!/usr/bin/env python3
"""Render each non-website project's README into a page of its own.

The Markdown is not parsed here. It is posted to GitHub's own /markdown
endpoint in GFM mode, so what the page shows is byte-for-byte what GitHub
would show -- task lists, tables, footnotes, alerts and all. Relative links
and images are then rewritten to absolute GitHub URLs, because a README is
written to be read from inside the repository.

Run:  python tools/render_readme.py          (from the site root)
Needs the `gh` CLI, authenticated.
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# page slug -> what to render
PROJECTS = [
    {
        "slug": "openvpn",
        "repo": "elyotam/aws-openvpn",
        "branch": "main",
        "readme": "README.md",
        "title": "OpenVPN Access Server on AWS",
        "tagline": "A reusable, clean-room Terraform module that keeps every secret out "
                   "of Terraform state.",
        "chips": ["Terraform module", "HCL", "AWS", "EC2", "Secrets hygiene"],
        "tint": "rgba(124,92,224,.20)",
        "extra": [("מדריך בעברית",
                   "https://github.com/elyotam/aws-openvpn/blob/main/README.he.md")],
        "rtl": False,
    },
    {
        "slug": "quakewatch",
        "repo": "elyotam/quakewatch-final-project",
        "branch": "main",
        "readme": "README.md",
        "title": "QuakeWatch",
        "tagline": "Live USGS earthquake data in Flask, shipped the whole way down: "
                   "Docker, Helm, Kubernetes and Argo CD.",
        "chips": ["Flask + Kubernetes", "Python", "Docker", "Helm", "Argo CD"],
        "tint": "rgba(50,108,229,.22)",
        "extra": [("Docker Hub image",
                   "https://hub.docker.com/r/cohenelyotam/quakewatch")],
        "rtl": False,
    },
    {
        "slug": "devops-experts",
        "repo": "elyotam/devops-experts",
        "branch": "main",
        "readme": "README.md",
        "title": "DevOps course archive",
        "tagline": "Fourteen lessons from the DevOps Experts programme — one runnable "
                   "script per lesson, plus six deliberately broken builds.",
        "chips": ["14 lessons", "Bash", "Kubernetes", "Terraform", "Ansible"],
        "tint": "rgba(255,212,59,.14)",
        "extra": [("The final project →", "quakewatch.html")],
        "rtl": True,
    },
]


def gh(*args, stdin=None):
    """Run gh and return stdout, raising with gh's own message on failure."""
    p = subprocess.run(["gh", *args], input=stdin, capture_output=True,
                       text=True, encoding="utf-8")
    if p.returncode != 0:
        raise RuntimeError("gh %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def fetch_markdown(repo, branch, path):
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch, path)
    return gh("api", "--method", "GET", url) if False else _raw(url)


def _raw(url):
    import urllib.request
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


def to_html(markdown, repo):
    """GitHub renders it, so it matches GitHub exactly."""
    payload = json.dumps({"text": markdown, "mode": "gfm", "context": repo})
    # no leading slash: Git Bash rewrites /markdown into a filesystem path
    return gh("api", "--method", "POST", "markdown", "--input", "-", stdin=payload)


def absolutise(html, repo, branch):
    """A README links to files next to it. From our domain those must be absolute."""
    blob = "https://github.com/%s/blob/%s/" % (repo, branch)
    raw = "https://raw.githubusercontent.com/%s/%s/" % (repo, branch)

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|#|//|data:)', url):
            return m.group(0)
        # href points at the file's page, src/srcset at the bytes themselves
        base = blob if attr == "href" else raw
        return '%s="%s%s"' % (attr, base, url.lstrip("./"))

    return re.sub(r'\b(href|src|srcset)="([^"]*)"', fix, html)


def harden(html):
    """Anything leaving GitHub's renderer is trusted markup, but links out of the
    site still need the usual hygiene, and headings need to survive our CSS."""
    # GitHub already puts rel="nofollow" on some outbound links; adding a second
    # rel attribute would be invalid and would silently drop the first
    def rel(m):
        tag = m.group(0)
        return tag if ' rel=' in tag else '<a rel="noopener"' + tag[2:]
    html = re.sub(r'<a (?=[^>]*href="https?:)[^>]*>', rel, html)
    # GitHub emits <h1>-<h6> with an anchor child; keep them, drop the SVG icon
    html = re.sub(r'<svg class="octicon octicon-link".*?</svg>', '', html, flags=re.S)
    return html


PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Elyotam Cohen</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#111111">
<link rel="canonical" href="https://elyotam.github.io/{slug}.html">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Elyotam Cohen">
<meta property="og:title" content="{title} — Elyotam Cohen">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://elyotam.github.io/{slug}.html">
<meta property="og:image" content="https://elyotam.github.io/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} — Elyotam Cohen">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://elyotam.github.io/assets/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/case.css">
<link rel="stylesheet" href="assets/readme.css">
<style>.hero{{--tint:{tint}}}</style>
</head>
<body>

<div class="wrap">
  <div class="top">
    <a class="ghost" href="./">HELLO WORLD!</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav">
      <a href="./">Home</a><a href="about.html">About</a>
      <a class="on" href="projects.html">My Projects</a><a href="contact.html">Contact</a>
    </nav>
    <a class="pill" href="contact.html">
      <svg viewBox="0 0 24 24"><path d="M6.94 5a2 2 0 1 1-4-.002 2 2 0 0 1 4 .002M7 8.48H3V21h4zm6.32 0H9.34V21h3.92v-6.57c0-3.66 4.77-4 4.77 0V21H22v-7.93c0-6.17-7.06-5.94-8.72-2.91z"/></svg>
      Let&rsquo;s Connect!
    </a>
  </div>

  <main class="case">

    <header class="box hero reveal">
      <p class="crumbs"><a href="projects.html">My Projects</a><span>/</span>{crumb}</p>
      <h1>{title}</h1>
      <p class="lede">{tagline}</p>
      <div class="chips">{chips}</div>
      <div class="acts">
        <a class="btn key" href="https://github.com/{repo}" rel="noopener">
          <svg viewBox="0 0 24 24"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2 0-.3-.5-1.5.2-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>
          View on GitHub
        </a>
        {extra}
        <a class="btn" href="projects.html">All projects</a>
      </div>
    </header>

    <dl class="facts reveal">{facts}</dl>

    <article class="box readme reveal">
      <div class="rm-bar">
        <span class="rm-file">
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 13.25 16h-9.5A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011Z"/></svg>
          {readme_name}
        </span>
        <a class="rm-src" href="https://github.com/{repo}/blob/{branch}/{readme_name}" rel="noopener">Read it on GitHub &nearr;</a>
      </div>
      <div class="markdown-body"{dir}>
{body}
      </div>
    </article>

    <section class="box next reveal">
      <div>
        <h2>Questions about this one?</h2>
        <p>Happy to walk through any of it.</p>
      </div>
      <div class="acts">
        <a class="btn key" href="contact.html">Get in touch</a>
        <a class="btn" href="projects.html">Back to projects</a>
      </div>
    </section>

  </main>
</div>

<footer>
  <nav>
    <a href="./">Home</a><a href="about.html">About</a>
    <a href="projects.html">My Projects</a><a href="contact.html">Contact</a>
  </nav>
  <div><span id="yr">2026</span> &copy; Created with love by
    <a class="by" href="https://github.com/elyotam" rel="noopener">Elyotam Cohen</a></div>
</footer>

<script src="assets/site.js"></script>
<script src="assets/cursor.js"></script>
</body>
</html>
'''


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def build(p):
    repo, branch = p["repo"], p["branch"]
    md = _raw("https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch, p["readme"]))
    # never re-indent this: inside <pre>, leading spaces are content, and
    # indenting the block silently pushes every code sample and ASCII diagram
    html = harden(absolutise(to_html(md, repo), repo, branch))

    meta = json.loads(gh("api", "repos/" + repo,
                         "--jq", '{lang:.language,size:.size,updated:.pushed_at,stars:.stargazers_count}'))
    files = gh("api", "repos/%s/git/trees/%s?recursive=1" % (repo, branch),
               "--jq", '[.tree[] | select(.type=="blob")] | length').strip()
    updated = meta["updated"][:10]

    facts = "".join(
        '<div class="box fact"><dt>%s</dt><dd>%s</dd></div>' % (dt, dd)
        for dt, dd in [
            ("Language", meta["lang"] or "Mixed"),
            ("Files", "%s tracked" % files),
            ("Last push", updated),
            ("Licence", "Public repository"),
        ])

    extra = "".join('<a class="btn" href="%s"%s>%s</a>'
                    % (u, ' rel="noopener"' if u.startswith("http") else "", esc(t))
                    for t, u in p["extra"])

    page = PAGE.format(
        slug=p["slug"], title=esc(p["title"]), desc=esc(p["tagline"]),
        tagline=esc(p["tagline"]), tint=p["tint"], repo=repo, branch=branch,
        crumb="Infrastructure", readme_name=p["readme"],
        chips="".join('<span class="chip%s">%s</span>'
                      % (" hot" if i == 0 else "", esc(c))
                      for i, c in enumerate(p["chips"])),
        acts="", extra=extra, facts=facts,
        dir=' dir="rtl" lang="he"' if p["rtl"] else "",
        body=html)

    out = os.path.join(ROOT, p["slug"] + ".html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    return out, len(page), len(md)


if __name__ == "__main__":
    for p in PROJECTS:
        try:
            out, n, m = build(p)
            print("  %-22s %6d bytes  (from %d bytes of Markdown)"
                  % (os.path.basename(out), n, m))
        except Exception as e:
            print("  %-22s FAILED: %s" % (p["slug"], e))
            sys.exit(1)
