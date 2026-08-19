# Data Structures unit

## Student notebooks (distribute via Google Classroom → "Make a copy for each student")

| Notebook | Topic | Students implement | Time (approx) |
|---|---|---|---|
| `linked_list_adt.ipynb` | List ADT, `Node`, `LinkedList`, cost vs Python list | `SortedLinkedList.insert` (+ stretch `search`), exercises | 2–3 h |
| `stacks_queues.ipynb` | Stack/Queue ADTs as ABCs, linked vs list implementations, `deque` | `ListStack`, `ListQueue`, exercises, 🏆 `FastListQueue` challenge | 2.5–3.5 h |

Prerequisite: students have seen linked lists and how Python lists work under the hood.

The notebooks fetch their test modules from this repo at run time:

```
https://raw.githubusercontent.com/mdevlin-midpac/ib-cs-2027/main/data_structures/ll_tests.py
https://raw.githubusercontent.com/mdevlin-midpac/ib-cs-2027/main/data_structures/sq_tests.py
```

so the repo must stay **public** and the files must stay at those paths. Updating a test file here updates it for every student on their next run.

## Test modules (students import, don't read)

- `ll_tests.py` — `check_sorted_insert`, `check_sorted_search`
- `sq_tests.py` — `check_stack`, `check_queue`, `check_fast_queue`

Each `check_*` prints a ✅/❌/💥/⚪ report and returns `(passed, total)`.

## Grading

1. In Google Drive, open `Classroom/<class>/<assignment>/`, right-click → Download (zip), unzip.
2. From this folder:
   ```
   python tools/grade.py path/to/unzipped/*.ipynb --report
   ```
3. Open `report.html` (students × test cases, colour-coded) or import `report.csv`.

`grade.py` re-runs each notebook's code and applies the official tests — it never trusts output cells the student may have edited. It works on a mixed folder of both notebooks.

## Adding an assignment

1. Add skeleton cells (with `raise NotImplementedError`) and a form-mode test cell to the notebook.
2. Add a `check_*` function to the matching `*_tests.py`.
3. Add one row to `CHECKS` in `tools/grade.py`.
4. Run a private reference solution through the grader before releasing.

## Notes

- Colab: the `#@title ... { display-mode: "form" }` cells hide the widget/test code. Per-cell read-only metadata is set but Colab doesn't enforce it (JupyterLab/VS Code do).
- The notebooks also run in plain Jupyter/VS Code; the `!wget` line is then harmless if the `.py` files are in the same folder.
