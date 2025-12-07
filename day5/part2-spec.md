# **1. Problem Summary**

You are given a list of numeric ranges (`A-B`), each representing a set of fresh ingredient IDs.
Ignore everything after the blank line.
Your task is to compute the **total number of unique integer IDs** contained in the union of all these ranges.

---

# **2. Domain Entities**

* **Range**: A pair of integers `(start, end)` defining an inclusive interval.
* **Ingredient ID**: Any integer within one of the ranges.
* **Range Union**: The merged set of all IDs covered by overlapping or adjacent intervals.

---

# **3. Inputs + Constraints**

### Input Structure

* One or more lines of ranges (`A-B` format).
* A blank line may follow, but **anything after it is ignored**.

### Constraints / Assumptions

* `A` and `B` are integers, with `A ≤ B`.
* Ranges may overlap, may touch, or may be nested.
* Input order is arbitrary; no guarantee of sorting.
* The total span may be large (merging, not enumeration, is required).

---

# **4. Expected Outputs**

* A **single integer**:
  The total count of *distinct* integer IDs covered by the union of all ranges.

---

# **5. Rules + Logic Requirements**

1. A range `A-B` includes all integers `x` such that `A ≤ x ≤ B`.
2. Overlapping or adjacent ranges contribute only once to the final count.
3. The available ID list from Part 1 must be **ignored entirely**.
4. The final count is the sum over merged non-overlapping ranges:
   `sum(end_i - start_i + 1)` for each merged interval.

---

# **6. Edge Cases**

* Fully nested ranges (e.g., `5-20` and `10-12`) → should not inflate the count.
* Adjacent ranges (e.g., `3-5` and `6-10`) → should be merged.
* Completely disjoint ranges → counted independently.
* Single-element ranges (e.g., `8-8`).
* Large ranges with large gaps.
* Input with only one range.

---

# **7. Sample Tests**

### Test 1 (Given Example)

Ranges:

```
3-5
10-14
16-20
12-18
```

Merged:

```
3-5
10-20
```

Counts:

* `3–5` → 3 IDs
* `10–20` → 11 IDs

Total = **14**.

---

### Test 2

Ranges:

```
1-2
5-8
6-10
```

Merged:

```
1-2
5-10
```

Count = `2 + 6 = 8`.

---

### Test 3

Ranges:

```
100-100
99-101
```

Merged:

```
99-101
```

Count = 3.

---

# **8. Solution Outline (High Level)**

1. Parse each range into `(start, end)`.
2. Ignore everything after the blank line.
3. Sort ranges by starting value.
4. Merge overlapping or adjacent ranges.
5. For each merged range, compute its size: `end - start + 1`.
6. Sum all range sizes.
7. Output the total.

---

# **9. Flow Walkthrough**

Using the example:

Input ranges:
`3-5`, `10-14`, `16-20`, `12-18`

Sorted:
`3-5`, `10-14`, `12-18`, `16-20`

Merge pass:

* `10–14` merges with `12–18` → `10–18`
* `10–18` merges with `16–20` → `10–20`

Final merged ranges:

* `3–5`
* `10–20`

Count:

* `3–5` → 3 IDs
* `10–20` → 11 IDs

Total = **14**.

---

# **10. Implementation Plan (Language-Agnostic)**

1. **Parse Input**

   * Read all lines until the blank line.
   * For each line:

     * Split on `-` to extract `start`, `end`.
     * Convert both to integers.

2. **Sort Ranges**

   * Sort by `start` ascending.

3. **Merge Pass**

   * Initialize merged list with first range.
   * For each next range:

     * If `current.start ≤ last.end + 1`:

       * Overlaps or touches → update last range to
         `last.end = max(last.end, current.end)`
     * Else:

       * Append as a new disjoint range.

4. **Compute Total**

   * For each merged `(s, e)`:

     * Add `(e - s + 1)` to total.

5. **Return Total Count**

---

# **11. Real-World Analogy + Practical Use Case**

This is identical to:

* Finding total coverage in memory allocation maps.
* Computing the union length of IP ranges.
* Summing maintenance windows after interval consolidation.
* Merging booking reservations into consolidated timeslots.

Interval-union problems appear in scheduling, compilers, networking, database optimization, and computational geometry.