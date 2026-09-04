#!/usr/bin/env python3
"""Does every link the published site advertises actually resolve?

WHY THIS EXISTS
---------------
On 2026-09-04 an end-to-end check of docs/index.html found two cards marked
`status live` / "Available" whose links cannot be served:

    <a href="Analysis/Results/literature_gap_report.md">View report -></a>
    <a href="Analysis/Results/pubmed_recent_summary.md">View report -></a>

docs/ is the GitHub Pages publish root. Those hrefs are page-relative, so they
resolve to docs/Analysis/Results/... - a directory that has never existed. The
other 38 relative links on the same page (Dashboards/*.html) all resolve. Two
of forty were broken, and both were advertised as available.

This is the 2026-08-16 lesson repeating in a third form. That audit found
docs/Dashboards/ stale because rebuild_website.py wrote docs/index.html and
nothing published the artifacts it pointed at; sync_docs_dashboards.py was
written to close it. The same shape reappeared here for the two MARKDOWN
reports, which sync_docs_dashboards.py does not cover because it copies *.html
only. A gate aimed at the builder is not a gate aimed at the site.

WHAT THIS GATE DOES
-------------------
For every .html file under docs/, resolve every relative href/src against the
file's own directory and confirm the target exists on disk, and confirm the
resolved path stays inside docs/ (a target outside the publish root cannot be
served even if it exists in the repo - which is exactly how the two defects
above hid: the files exist, just not where Pages can reach them).

  BROKEN_LINK     target does not exist on disk
  ESCAPES_ROOT    target resolves outside docs/, so Pages cannot serve it

Absolute URLs (http, https, mailto, //) and in-page anchors (#...) are out of
scope: this gate speaks only about files this repo is responsible for placing.

Exit codes: 0 clean, 1 findings.
"""
import json
import os
import re
import sys
from datetime import date
from urllib.parse import unquote, urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
ROOT = os.path.dirname(BASE)
DOCS = os.path.join(ROOT, 'docs')
REPORT = os.path.join(BASE, 'Results', 'published_links_audit.json')

LINK_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.IGNORECASE)
EXTERNAL = ('http://', 'https://', '//', 'mailto:', 'tel:', 'data:', 'javascript:')


def is_external(target):
    return target.startswith(EXTERNAL)


def collect():
    findings, ok = [], 0
    pages = []
    for dirpath, dirnames, filenames in os.walk(DOCS):
        dirnames[:] = [d for d in dirnames if d not in {'.git', 'node_modules'}]
        for name in sorted(filenames):
            if name.endswith('.html'):
                pages.append(os.path.join(dirpath, name))

    for page in sorted(pages):
        rel_page = os.path.relpath(page, ROOT).replace(os.sep, '/')
        with open(page, encoding='utf-8', errors='replace') as fh:
            html = fh.read()
        for raw in LINK_RE.findall(html):
            target = raw.strip()
            if not target or target.startswith('#') or is_external(target):
                continue
            # Strip query/fragment before touching the filesystem.
            path_part = unquote(urlparse(target).path)
            if not path_part:
                continue
            resolved = os.path.normpath(
                os.path.join(os.path.dirname(page), path_part))
            inside = os.path.commonpath([os.path.abspath(resolved),
                                         os.path.abspath(DOCS)]) == os.path.abspath(DOCS)
            exists = os.path.exists(resolved)
            if not inside:
                findings.append({
                    'kind': 'ESCAPES_ROOT', 'page': rel_page, 'href': target,
                    'resolves_to': os.path.relpath(resolved, ROOT).replace(os.sep, '/'),
                    'exists_in_repo': exists,
                })
            elif not exists:
                findings.append({
                    'kind': 'BROKEN_LINK', 'page': rel_page, 'href': target,
                    'resolves_to': os.path.relpath(resolved, ROOT).replace(os.sep, '/'),
                    'exists_in_repo': False,
                })
            else:
                ok += 1
    return findings, ok, len(pages)


def main():
    if not os.path.isdir(DOCS):
        print('[SKIP] no docs/ directory; nothing is published.')
        return 0

    findings, ok, n_pages = collect()

    print('=' * 74)
    print('PUBLISHED LINK AUDIT - does every advertised link resolve under docs/?')
    print('=' * 74)
    print('%d page(s) scanned, %d relative link(s) resolve, %d finding(s).'
          % (n_pages, ok, len(findings)))

    for f in findings:
        print('  [%s] %s' % (f['kind'], f['page']))
        print('        href        %s' % f['href'])
        print('        resolves to %s (exists=%s)'
              % (f['resolves_to'], f['exists_in_repo']))
        if f['kind'] == 'ESCAPES_ROOT' and f['exists_in_repo']:
            print('        the file exists in the repo but NOT under the publish')
            print('        root, so a reader clicking this link gets a 404.')

    payload = {
        'generated': date.today().isoformat(),
        'pages_scanned': n_pages,
        'links_ok': ok,
        'findings': findings,
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2)
    print('  -> %s' % os.path.relpath(REPORT, ROOT).replace(os.sep, '/'))

    if findings:
        print('\n[FAIL] %d advertised link(s) cannot be served.' % len(findings))
        return 1
    print('\n[OK] every advertised relative link resolves under the publish root.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
