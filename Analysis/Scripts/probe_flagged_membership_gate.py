"""Known-positive probe: is check 2 vacuous after the exemptions?

Three cases, all through the real _scan():
  A  an uncitable PMID inside an emitted HTML f-string   -> MUST be caught
  B  the same PMID inside a repair COMMENT                -> MUST be exempt
  C  the same PMID beside "NOT CORPUS" in an html page    -> MUST be exempt
"""
import os, sys, tempfile
sys.path.insert(0, '.')
import audit_flagged_membership_class as A

d = tempfile.mkdtemp()
TARGET = {'20570966'}

a = os.path.join(d, 'build_probe_a.py')
open(a, 'w', encoding='utf-8').write(
    'def render(x):\n'
    '    return f"<li>Orban et al. abatacept "\\\n'
    '           f"<a href=\'https://pubmed.ncbi.nlm.nih.gov/20570966/\'>PMID:20570966</a></li>"\n')

b = os.path.join(d, 'build_probe_b.py')
open(b, 'w', encoding='utf-8').write(
    '"""Module docstring mentioning PMID 20570966 as a withdrawal record."""\n'
    'def render(x):\n'
    '    # Repaired 2026-08-28. This entry read PMID:20570966, which is a\n'
    '    # Crohn disease paper. Citation withdrawn.\n'
    '    return "<li>ok</li>"\n')

c = os.path.join(d, 'probe_c.html')
open(c, 'w', encoding='utf-8').write(
    '<tr><td>build_immunomod_lada.py</td><td>20570966</td>'
    '<td>NOT CORPUS</td><td>FUT2 non-secretor status</td></tr>\n')

ra = A._scan([a], TARGET, is_python=True)
rb = A._scan([b], TARGET, is_python=True)
rc = A._scan([c], TARGET)

ok = True
def chk(label, got, want_hit):
    global ok
    hit = bool(got)
    good = (hit == want_hit)
    ok &= good
    print('  %-58s %-9s %s' % (label, 'CAUGHT' if hit else 'exempt',
                               'OK' if good else '<<< WRONG'))

chk('A  asserted in emitted HTML string       -> expect CAUGHT', ra, True)
chk('B  named in comment + docstring only     -> expect exempt', rb, False)
chk('C  listed beside "NOT CORPUS" in a page  -> expect exempt', rc, False)
print()
print('known-positive probe:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
