"""
Test helpers for the Stacks & Queues notebook.
Students run these; they don't need to read them.
Instructors: each check_* function returns (passed, total); per-case detail is in `last_results`.
"""
import random, time

last_results = []


def _run(name, cases):
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


# ------------------------------------------------------------------ Stack

def check_stack(StackClass, name="Stack"):
    def t_empty():
        s = StackClass()
        assert s.is_empty() is True, "is_empty() should be True on a new stack"
        assert len(s) == 0, f"len should be 0, got {len(s)}"

    def t_push_len():
        s = StackClass(); s.push(1); s.push(2); s.push(3)
        assert len(s) == 3, f"len should be 3, got {len(s)}"
        assert s.is_empty() is False, "is_empty() should be False after pushes"

    def t_lifo():
        s = StackClass()
        for x in [1, 2, 3]: s.push(x)
        assert s.pop() == 3, "pop should return the LAST pushed item"
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.is_empty(), "stack should be empty after popping everything"

    def t_peek():
        s = StackClass(); s.push("a"); s.push("b")
        assert s.peek() == "b", f"peek should return 'b', got {s.peek()!r}"
        assert len(s) == 2, "peek must not remove the item"
        assert s.peek() == "b", "peek should be repeatable"

    def t_pop_empty():
        s = StackClass()
        try:
            s.pop()
        except IndexError:
            return
        raise AssertionError("pop() on an empty stack should raise IndexError")

    def t_peek_empty():
        s = StackClass()
        try:
            s.peek()
        except IndexError:
            return
        raise AssertionError("peek() on an empty stack should raise IndexError")

    def t_interleaved():
        s = StackClass()
        s.push(1); s.push(2)
        assert s.pop() == 2
        s.push(3)
        assert s.pop() == 3
        assert s.pop() == 1
        assert s.is_empty()

    def t_random():
        random.seed(1)
        s = StackClass(); ref = []
        for _ in range(500):
            if ref and random.random() < 0.4:
                assert s.pop() == ref.pop(), "pop disagreed with reference"
            else:
                v = random.randint(0, 99); s.push(v); ref.append(v)
            assert len(s) == len(ref), "len disagreed with reference"

    return _run(name, [
        ("new stack is empty", t_empty),
        ("push increases length", t_push_len),
        ("pop returns items last-in-first-out", t_lifo),
        ("peek returns top without removing", t_peek),
        ("pop on empty raises IndexError", t_pop_empty),
        ("peek on empty raises IndexError", t_peek_empty),
        ("interleaved push/pop", t_interleaved),
        ("500 random operations match reference", t_random),
    ])


# ------------------------------------------------------------------ Queue

def check_queue(QueueClass, name="Queue"):
    def t_empty():
        q = QueueClass()
        assert q.is_empty() is True, "is_empty() should be True on a new queue"
        assert len(q) == 0, f"len should be 0, got {len(q)}"

    def t_enqueue_len():
        q = QueueClass(); q.enqueue(1); q.enqueue(2); q.enqueue(3)
        assert len(q) == 3, f"len should be 3, got {len(q)}"
        assert q.is_empty() is False

    def t_fifo():
        q = QueueClass()
        for x in [1, 2, 3]: q.enqueue(x)
        assert q.dequeue() == 1, "dequeue should return the FIRST enqueued item"
        assert q.dequeue() == 2
        assert q.dequeue() == 3
        assert q.is_empty()

    def t_peek():
        q = QueueClass(); q.enqueue("a"); q.enqueue("b")
        assert q.peek() == "a", f"peek should return 'a' (the front), got {q.peek()!r}"
        assert len(q) == 2, "peek must not remove the item"

    def t_dequeue_empty():
        q = QueueClass()
        try:
            q.dequeue()
        except IndexError:
            return
        raise AssertionError("dequeue() on an empty queue should raise IndexError")

    def t_peek_empty():
        q = QueueClass()
        try:
            q.peek()
        except IndexError:
            return
        raise AssertionError("peek() on an empty queue should raise IndexError")

    def t_refill():
        # Empty the queue completely, then use it again (catches stale head/tail bugs).
        q = QueueClass()
        q.enqueue(1); q.dequeue()
        assert q.is_empty()
        q.enqueue(2); q.enqueue(3)
        assert q.dequeue() == 2 and q.dequeue() == 3

    def t_random():
        random.seed(2)
        from collections import deque
        q = QueueClass(); ref = deque()
        for _ in range(500):
            if ref and random.random() < 0.4:
                assert q.dequeue() == ref.popleft(), "dequeue disagreed with reference"
            else:
                v = random.randint(0, 99); q.enqueue(v); ref.append(v)
            assert len(q) == len(ref), "len disagreed with reference"

    return _run(name, [
        ("new queue is empty", t_empty),
        ("enqueue increases length", t_enqueue_len),
        ("dequeue returns items first-in-first-out", t_fifo),
        ("peek returns front without removing", t_peek),
        ("dequeue on empty raises IndexError", t_dequeue_empty),
        ("peek on empty raises IndexError", t_peek_empty),
        ("works again after being emptied", t_refill),
        ("500 random operations match reference", t_random),
    ])


def check_fast_queue(QueueClass):
    """CHALLENGE: correctness + a scaling check that catches O(n) dequeue."""
    def t_correct():
        p, t = check_queue(QueueClass, name="FastListQueue (correctness)")
        assert p == t, f"only {p}/{t} correctness cases passed"

    def _time_drain(n):
        q = QueueClass()
        for i in range(n): q.enqueue(i)
        t0 = time.perf_counter()
        for _ in range(n): q.dequeue()
        return time.perf_counter() - t0

    def t_scaling():
        # O(1) dequeue: 10x more items ~ 10x more time. O(n): ~100x.
        small = max(_time_drain(3_000), 1e-4)
        large = _time_drain(30_000)
        ratio = large / small
        assert ratio < 35, (f"dequeue time grew {ratio:.0f}x for 10x more items "
                            f"— looks like O(n) per dequeue (pop(0)?)")

    def t_memory_reclaimed():
        # After draining, the internal list shouldn't still hold 30k dead slots.
        q = QueueClass()
        for i in range(30_000): q.enqueue(i)
        for _ in range(30_000): q.dequeue()
        for i in range(10): q.enqueue(i)
        # Look for any list attribute; it should be small now.
        lists = [v for v in vars(q).values() if isinstance(v, list)]
        assert lists, "expected the queue to store items in a Python list"
        assert all(len(L) < 1000 for L in lists), \
            f"internal list still holds {max(len(L) for L in lists)} slots after draining — compact it occasionally"

    return _run("FastListQueue (CHALLENGE)", [
        ("passes all queue correctness tests", t_correct),
        ("dequeue is O(1) amortized (scaling check)", t_scaling),
        ("dead slots are reclaimed", t_memory_reclaimed),
    ])
