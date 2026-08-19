"""
Test helpers for the Linked List notebook.
Students run these; they don't need to read them.
Instructors: each check_* function returns (passed, total) so it can be autograded.
"""
import random

# Detailed per-case results of the most recent check_* call, for the autograder.
# Each entry: (case_description, status) where status is "pass" | "fail" | "error" | "todo"
last_results = []


def _run(name, cases):
    """cases: list of (description, callable). callable raises AssertionError on failure."""
    global last_results
    last_results = []
    passed = 0
    print(f"=== {name} ===")
    for desc, fn in cases:
        try:
            fn()
            print(f"  ✅ {desc}")
            passed += 1
            last_results.append((desc, "pass"))
        except NotImplementedError:
            print(f"  ⚪ {desc}  (not implemented yet)")
            last_results.append((desc, "todo"))
        except AssertionError as e:
            print(f"  ❌ {desc}  -> {e}" if str(e) else f"  ❌ {desc}")
            last_results.append((desc, "fail"))
        except Exception as e:
            print(f"  💥 {desc}  -> {type(e).__name__}: {e}")
            last_results.append((desc, "error"))
    print(f"  {passed}/{len(cases)} passed\n")
    return passed, len(cases)


def _to_pylist(ll):
    out, cur = [], ll.head
    while cur is not None:
        out.append(cur.data)
        cur = cur.next
    return out


# ---------------------------------------------------------------- SortedLinkedList

def check_sorted_insert(SortedLinkedList):
    def fresh(values=()):
        s = SortedLinkedList()
        for v in values:
            s.insert(v)
        return s

    def t_empty():
        s = fresh(); s.insert(5)
        assert _to_pylist(s) == [5], f"got {_to_pylist(s)}"
        assert len(s) == 1, f"len is {len(s)}, expected 1"

    def t_front():
        s = fresh([10, 20, 30]); s.insert(1)
        assert _to_pylist(s) == [1, 10, 20, 30], f"got {_to_pylist(s)}"

    def t_middle():
        s = fresh([10, 20, 30]); s.insert(25)
        assert _to_pylist(s) == [10, 20, 25, 30], f"got {_to_pylist(s)}"

    def t_end():
        s = fresh([10, 20, 30]); s.insert(99)
        assert _to_pylist(s) == [10, 20, 30, 99], f"got {_to_pylist(s)}"

    def t_duplicates():
        s = fresh([10, 20, 30]); s.insert(20)
        assert _to_pylist(s) == [10, 20, 20, 30], f"got {_to_pylist(s)}"

    def t_size():
        s = fresh([3, 1, 2])
        assert len(s) == 3, f"len is {len(s)}, expected 3 (did you update _size?)"

    def t_random():
        random.seed(0)
        for _ in range(20):
            vals = [random.randint(-50, 50) for _ in range(random.randint(0, 15))]
            s = fresh(vals)
            assert _to_pylist(s) == sorted(vals), f"inserting {vals} gave {_to_pylist(s)}"

    def t_strings():
        s = fresh(["pear", "apple", "fig"])
        assert _to_pylist(s) == ["apple", "fig", "pear"], f"got {_to_pylist(s)}"

    def t_still_a_linked_list():
        s = fresh([2, 1])
        assert s.get(0) == 1 and s.search(2) == 1, "inherited get/search should still work"

    return _run("SortedLinkedList.insert", [
        ("insert into empty list", t_empty),
        ("insert at front", t_front),
        ("insert in middle", t_middle),
        ("insert at end", t_end),
        ("duplicates allowed", t_duplicates),
        ("length tracked correctly", t_size),
        ("random sequences stay sorted", t_random),
        ("works with strings", t_strings),
        ("inherited get/search still work", t_still_a_linked_list),
    ])


def check_sorted_search(SortedLinkedList):
    """Optional stretch: an early-exit search that stops once values exceed the target."""
    def fresh(values):
        s = SortedLinkedList()
        for v in values: s.insert(v)
        return s

    def t_found():
        s = fresh([5, 1, 3])
        assert s.search(3) == 1, f"got {s.search(3)}"

    def t_missing():
        s = fresh([5, 1, 3])
        assert s.search(4) == -1, f"got {s.search(4)}"

    def t_early_exit():
        # Build a list, then attach a poisoned node past where search should stop.
        s = fresh([1, 2, 3, 10])
        class Poison:
            def __eq__(self, other): raise RuntimeError("search walked past where it should have stopped")
            def __lt__(self, other): raise RuntimeError("search walked past where it should have stopped")
            def __gt__(self, other): raise RuntimeError("search walked past where it should have stopped")
        cur = s.head
        while cur.next is not None: cur = cur.next
        cur.next = type(cur)(Poison())   # attach a poison node AFTER 10
        assert s.search(4) == -1

    return _run("SortedLinkedList.search (stretch)", [
        ("finds present value", t_found),
        ("returns -1 for missing", t_missing),
        ("stops early once past target", t_early_exit),
    ])
