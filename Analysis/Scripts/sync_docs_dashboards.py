#!/usr/bin/env python3
"""
Publish Dashboards/ -> docs/Dashboards/ (GitHub Pages).

WHY THIS EXISTS
---------------
On 2026-08-16 an audit found that docs/Dashboards/ - the copy GitHub Pages
actually serves - had not been updated since 2026-03-29 / 2026-04-20. All 33
published dashboards were stale and 2 were missing entirely. Zero were in sync.

Meanwhile run_quality_improvements.py reported "All 42 improvements completed
successfully" on every daily run, because rebuild_website.py only ever wrote
docs/index.html. Nothing copied the rebuilt dashboards into docs/.

The practical consequence: seven miscited PMIDs corrected in the build scripts
that day were still live on the public site, including two that resolved to
plant-biology papers, plus a DIAGNODE-3 description that had been superseded by
the trial's futility closure.

This is the same failure mode as the citation MISMATCH gap: a step that reports
success while the artifact a reader actually sees goes untouched. A green
pipeline must mean the published output changed.

BEHAVIOUR
---------
Copies every Dashboards/*.html to docs/Dashboards/, then re-verifies byte
equality. Exits non-zero if any file fails to sync.

Usage:
    python sync_docs_dashboards.py           # sync + verify
    python sync_docs_dashboards.py --check    # report drift only, no writes
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SRC_DIR = os.path.join(BASE_DIR, 'Dashboards')
DST_DIR = os.path.join(BASE_DIR, 'docs', 'Dashboards')

# PUBLISH REWRITE - added 2026-09-04, forced by measurement.
#
# A dashboard at Dashboards/X.html and its published copy at
# docs/Dashboards/X.html sit at DIFFERENT depths relative to the hub page, so
# the same relative href cannot be correct in both. postprocess_dashboards.py
# writes `../docs/index.html`, which is right where it runs and wrong once the
# file is published - docs/Dashboards/../docs/index.html is docs/docs/index.html,
# which has never existed.
#
# audit_published_links.py measured the damage on 2026-09-04: 34 of 34 published
# dashboards had a dead "<- Hub" back-link, plus three hand-written nav links
# ("Home", "<- Back to Index", "<- Dashboard Home") and one `href="/"` pointing
# at the Pages domain root rather than this project. 41 dead links, 1359 live.
#
# THE VERIFICATION IS WHY IT SURVIVED SIX MONTHS. This script's success
# condition was byte equality between source and published copy - and byte
# equality is precisely what guarantees this defect, because the published copy
# MUST differ from the source for its links to work. A copy step that verifies
# sameness cannot detect a defect whose fix is difference.
#
# So the transform is declared here, applied on publish, and verified on the
# transformed text. Keep this table small and exact: every entry is a path that
# is correct at repo root and wrong under docs/.
PUBLISH_REWRITES = [
    ('href="../docs/index.html"', 'href="../index.html"'),
]


def published_form(text):
    """The bytes that SHOULD be at docs/Dashboards/<name> for this source."""
    for old, new in PUBLISH_REWRITES:
        text = text.replace(old, new)
    return text


def read(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def classify(src_dir, dst_dir):
    stale, missing, ok = [], [], []
    if not os.path.isdir(src_dir):
        return stale, missing, ok
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith('.html'):
            continue
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        if not os.path.exists(dst):
            missing.append(name)
        elif read(dst) != published_form(read(src)):
            stale.append(name)
        else:
            ok.append(name)
    return stale, missing, ok


def main():
    check_only = '--check' in sys.argv

    if not os.path.isdir(SRC_DIR):
        print('[FAIL] Source dashboards directory not found: %s' % SRC_DIR)
        return 1

    stale, missing, ok = classify(SRC_DIR, DST_DIR)

    print('Publish dashboards -> docs/')
    print('  source   : %s' % SRC_DIR)
    print('  published: %s' % DST_DIR)
    print('  stale=%d  missing=%d  in-sync=%d' % (len(stale), len(missing), len(ok)))

    if check_only:
        for name in stale:
            print('    STALE   %s' % name)
        for name in missing:
            print('    MISSING %s' % name)
        if stale or missing:
            print('\n[FAIL] Published site is behind the built dashboards.')
            return 1
        print('\n[OK] Published site matches built dashboards.')
        return 0

    if not (stale or missing):
        print('\n[OK] Already in sync; nothing to publish.')
        return 0

    os.makedirs(DST_DIR, exist_ok=True)
    copied, rewritten = 0, 0
    for name in stale + missing:
        source = read(os.path.join(SRC_DIR, name))
        publish = published_form(source)
        if publish != source:
            rewritten += 1
        with open(os.path.join(DST_DIR, name), 'w', encoding='utf-8') as fh:
            fh.write(publish)
        copied += 1
    if rewritten:
        print('  %d file(s) had publish-relative links rewritten (see '
              'PUBLISH_REWRITES).' % rewritten)

    # Re-verify: a copy that silently failed is worse than no copy at all.
    stale2, missing2, ok2 = classify(SRC_DIR, DST_DIR)
    if stale2 or missing2:
        print('\n[FAIL] %d file(s) still out of sync after copy.' % (len(stale2) + len(missing2)))
        for name in stale2 + missing2:
            print('    %s' % name)
        return 1

    print('\n[OK] Published %d dashboard(s); %d verified in sync.' % (copied, len(ok2)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
