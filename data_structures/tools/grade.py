"""
Instructor autograder.

    python tools/grade.py ~/Downloads/submissions/*.ipynb            # console summary
    python tools/grade.py ~/Downloads/submissions/*.ipynb --report   # also writes report.html + report.csv
(run from the data_structures/ folder; reports are written to the current directory)

Runs every code cell of each notebook (skipping the students' own test cells), then
applies the official tests from ll_tests.py to the SortedLinkedList they defined.
Never trusts output the student may have edited.
"""
import sys, json, io, contextlib, os, csv, html
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # ../ holds ll_tests.py, sq_tests.py
import ll_tests, sq_tests

# (label, class name the student must define, test function, test module)
# A check is skipped if the notebook doesn't define that class -- so one grader
# works for every notebook in the course.
CHECKS = [
    # linked_list_adt.ipynb
    ("insert",     "SortedLinkedList", ll_tests.check_sorted_insert, ll_tests),
    ("search",     "SortedLinkedList", ll_tests.check_sorted_search, ll_tests),
    # stacks_queues.ipynb
    ("ListStack",  "ListStack",        sq_tests.check_stack,         sq_tests),
    ("ListQueue",  "ListQueue",        sq_tests.check_queue,         sq_tests),
    ("FastQueue",  "FastListQueue",    sq_tests.check_fast_queue,    sq_tests),
]

SYMBOL = {"pass": "✅", "fail": "❌", "error": "💥", "todo": "⚪", "missing": "—"}
COLOR  = {"pass": "#c8f7c5", "fail": "#f7c5c5", "error": "#f7dcc5", "todo": "#e6e6e6", "missing": "#e6e6e6"}


def run_notebook(path):
    nb = json.load(open(path))
    g = {}
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if "_tests" in src or src.lstrip().startswith(("!", "%")):
            continue  # skip their test cell and any shell/magic lines (e.g. !wget)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(src, g)
        except Exception:
            pass
    return g


def grade(path):
    """Return (student_name, {(check, case): status}, {check: (passed,total)})."""
    name = os.path.splitext(os.path.basename(path))[0]
    g = run_notebook(path)
    cells, totals = {}, {}
    # Only run checks whose target class this notebook is supposed to contain.
    relevant = [c for c in CHECKS if c[1] in g or any(c[1] in "".join(cell["source"])
                for cell in json.load(open(path))["cells"] if cell["cell_type"] == "code")]
    for check_name, cls_name, fn, module in relevant:
        cls = g.get(cls_name)
        if cls is None:
            totals[check_name] = (0, 0)          # class missing / didn't compile
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            p, t = fn(cls)
        totals[check_name] = (p, t)
        for desc, status in module.last_results:
            cells[(check_name, desc)] = status
    return name, cells, totals


def write_reports(rows, columns):
    # CSV
    with open("report.csv", "w", newline="") as f:
        w = csv.writer(f)
        score_cols = []
        for _, _, totals in rows:
            for k in totals:
                if k not in score_cols: score_cols.append(k)
        w.writerow(["student"] + [f"{c}: {d}" for c, d in columns] + [f"{c} score" for c in score_cols])
        for name, cells, totals in rows:
            w.writerow([name] + [cells.get(col, "missing") for col in columns]
                       + [("%d/%d" % totals[k]) if k in totals else "" for k in score_cols])
    # HTML
    head = "".join(f'<th class="rot"><div><span>{html.escape(c)}: {html.escape(d)}</span></div></th>' for c, d in columns)
    head += "".join(f"<th>{c}</th>" for c in score_cols)
    body = ""
    for name, cells, totals in rows:
        tds = "".join(f'<td style="background:{COLOR[cells.get(col, "missing")]}" title="{html.escape(col[1])}">'
                      f'{SYMBOL[cells.get(col, "missing")]}</td>' for col in columns)
        tds += "".join(f"<td><b>{'%d/%d' % totals[k] if k in totals else ''}</b></td>" for k in score_cols)
        body += f"<tr><td class='name'>{html.escape(name)}</td>{tds}</tr>"
    doc = f"""<!doctype html><meta charset="utf-8"><title>Grade report</title>
<style>
 body{{font-family:system-ui,sans-serif;padding:1em}}
 table{{border-collapse:collapse}} td,th{{border:1px solid #ccc;padding:4px 8px;text-align:center}}
 td.name{{text-align:left;font-weight:600}}
 th.rot{{height:170px;white-space:nowrap;vertical-align:bottom}}
 th.rot>div{{transform:translate(0,0) rotate(-60deg);width:28px}}
 th.rot span{{padding:4px}}
 tr:hover td{{filter:brightness(0.95)}}
</style>
<h2>Grade report — {len(rows)} submissions</h2>
<p>✅ pass &nbsp; ❌ fail &nbsp; 💥 crashed &nbsp; ⚪ not implemented &nbsp; — class not defined</p>
<table><tr><th>student</th>{head}</tr>{body}</table>"""
    open("report.html", "w").write(doc)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    want_report = "--report" in sys.argv
    rows = [grade(p) for p in args]

    # column order = order the tests are defined in
    columns = []
    for _, cells, _ in rows:
        for col in cells:
            if col not in columns:
                columns.append(col)

    for name, cells, totals in rows:
        line = "  ".join(f"{c} {p}/{t}" for c, (p, t) in totals.items())
        print(f"{name:40s} {line}")

    if want_report:
        write_reports(rows, columns)
        print("\nwrote report.html and report.csv")
