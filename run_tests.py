"""Minimal Extent-style HTML report for unittest."""

import os, sys, time, html, json, datetime as dt, unittest
from dataclasses import dataclass, asdict


@dataclass
class TestRecord:
    name: str
    class_name: str
    status: str
    start: float
    stop: float
    duration_ms: int
    message: str | None = None
    traceback: str | None = None


class ExtentResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.records: list[TestRecord] = []

    def startTest(self, test):
        setattr(test, '_started_at', time.time())
        super().startTest(test)

    def addSuccess(self, test):
        self._store(test, 'PASS')
        super().addSuccess(test)

    def addFailure(self, test, err):
        self._store(test, 'FAIL', err)
        super().addFailure(test, err)

    def addError(self, test, err):
        self._store(test, 'ERROR', err)
        super().addError(test, err)

    def addSkip(self, test, reason):
        self._store(test, 'SKIP', (None, None, reason))
        super().addSkip(test, reason)

    def _store(self, test, status, err=None):
        stop = time.time()
        start = getattr(test, '_started_at', stop)
        duration_ms = int((stop - start) * 1000)
        tb = msg = None
        if err and status in ('FAIL', 'ERROR'):
            etype, evalue, etb = err
            import traceback
            tb = ''.join(traceback.format_exception(etype, evalue, etb))
            msg = str(evalue)
        elif err and status == 'SKIP':
            msg = err[2]
        test_id = test.id()
        class_name, name = test_id.rsplit('.', 1)
        self.records.append(TestRecord(name, class_name, status, start, stop, duration_ms, msg, tb))


class ExtentRunner(unittest.TextTestRunner):
    def _makeResult(self):  # override to return our ExtentResult
        return ExtentResult(self.stream, self.descriptions, self.verbosity)


def discover():
    return unittest.defaultTestLoader.discover('tests', pattern='test_*.py')


def render_html(records: list[TestRecord], started: float, finished: float) -> str:
    total = len(records)
    counts = {k: sum(1 for r in records if r.status == k) for k in ['PASS', 'FAIL', 'ERROR', 'SKIP']}
    passed = counts['PASS']
    duration = finished - started
    started_human = dt.datetime.fromtimestamp(started).strftime('%Y-%m-%d %H:%M:%S')
    pass_pct = (passed / total * 100) if total else 0
    fail_pct = (counts['FAIL'] / total * 100) if total else 0
    error_pct = (counts['ERROR'] / total * 100) if total else 0
    skip_pct = (counts['SKIP'] / total * 100) if total else 0
    bar_parts = []
    if pass_pct: bar_parts.append(f"#2e7d32 {pass_pct:.2f}%")
    if fail_pct: bar_parts.append(f"#c62828 {fail_pct:.2f}%")
    if error_pct: bar_parts.append(f"#ad1457 {error_pct:.2f}%")
    if skip_pct: bar_parts.append(f"#f9a825 {skip_pct:.2f}%")
    bar_gradient = ','.join(bar_parts) or '#555 100%'

    rows = []
    for r in records:
        rows.append(f"<tr class='row {r.status}'><td><span class='status {r.status}'>{r.status}</span></td><td>{html.escape(r.class_name)}</td><td>{html.escape(r.name)}</td><td>{r.duration_ms} ms</td><td>{html.escape(r.message or '')}</td><td>{('<details><summary>Trace</summary><pre>'+html.escape(r.traceback)+'</pre></details>') if r.traceback else ''}</td></tr>")

    data_json = html.escape(json.dumps([asdict(r) for r in records]))

    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Extent Style Report</title>
<style>body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#121212;color:#e0e0e0}}header{{padding:1rem 2rem;background:#1e1e1e;display:flex;justify-content:space-between;align-items:center}}h1{{margin:0;font-size:1.2rem}}.badges span{{display:inline-block;margin-right:.5rem;padding:.35rem .6rem;border-radius:.6rem;font-size:.7rem;font-weight:600}}.PASS{{background:#2e7d32;color:#fff}}.FAIL{{background:#c62828;color:#fff}}.ERROR{{background:#ad1457;color:#fff}}.SKIP{{background:#f9a825;color:#222}}main{{padding:1.25rem}}table{{width:100%;border-collapse:collapse;margin-top:1rem;font-size:.75rem}}th,td{{border:1px solid #2d2d2d;padding:.45rem;vertical-align:top}}th{{background:#222}}tr.row:hover{{background:#1d1d1d}}details summary{{cursor:pointer;color:#64b5f6}}.summary-grid{{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1rem}}.card{{flex:1 1 160px;background:#1e1e1e;padding:1rem;border:1px solid #2a2a2a;border-radius:8px}}.bar{{height:10px;border-radius:5px;background:linear-gradient(90deg,{bar_gradient});margin-top:.5rem}}.status{{padding:.2rem .45rem;border-radius:.5rem;font-size:.6rem;font-weight:600}}</style>
</head><body>
<header><h1>Extent Style Selenium Report</h1><div class='badges'><span class='PASS'>PASS {counts['PASS']}</span><span class='FAIL'>FAIL {counts['FAIL']}</span><span class='ERROR'>ERROR {counts['ERROR']}</span><span class='SKIP'>SKIP {counts['SKIP']}</span><span>Total {total}</span></div></header>
<main>
<section class='summary-grid'>
  <div class='card'>Start<br><strong>{started_human}</strong></div>
  <div class='card'>Duration<br><strong>{duration:.2f}s</strong></div>
  <div class='card'>Pass Rate<br><strong>{pass_pct:.1f}%</strong><div class='bar'></div></div>
</section>
<h2>Tests</h2>
<table><thead><tr><th>Status</th><th>Class</th><th>Name</th><th>Duration</th><th>Message</th><th>Traceback</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>Raw Data (JSON)</h2><pre>{data_json}</pre>
</main>
<footer style='padding:1rem 2rem;font-size:.65rem;color:#777'>Generated {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</footer>
</body></html>"""


def write_report(content: str, directory: str = 'reports') -> str:
    os.makedirs(directory, exist_ok=True)
    name = dt.datetime.utcnow().strftime('extent_report_%Y%m%d_%H%M%S.html')
    path = os.path.join(directory, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def main():
    suite = discover()
    start = time.time()
    runner = ExtentRunner(verbosity=1)
    result = runner.run(suite)  # type: ignore
    stop = time.time()
    html_report = render_html(result.records, start, stop)  # type: ignore
    path = write_report(html_report)
    print(f"Extent-style report written to: {path}")
    if result.failures or result.errors:  # type: ignore
        sys.exit(1)


if __name__ == '__main__':
    main()
