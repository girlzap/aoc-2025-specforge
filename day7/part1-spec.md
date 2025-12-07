# ✅ **SpecForge Specification — Day 7 Part 1**

---

## **1. Problem Summary**

You are given a 2D grid representing a tachyon manifold.
A single downward-moving tachyon beam enters the grid at the column containing `S`.
As the beam moves downward, it may encounter splitter cells `^`, which stop the current beam and create two new beams that start below the splitter but shifted left and right.

The task is to simulate all beams until none remain and count **how many times a beam enters a splitter**, i.e., total number of splits.

---

## **2. Domain Entities**

* **Grid** — A 2D array of characters.
* **Empty cell (`.`)** — Beam passes through.
* **Splitter (`^`)** — Stops the incoming beam and spawns two new beams.
* **Entry point (`S`)** — Defines the column where the initial beam enters the grid.
* **Beam** — An active object defined by:

  * Current row
  * Current column
  * Direction: always **downward**
* **Split event** — When a beam moves into a splitter cell.

---

## **3. Inputs + Constraints**

### Input

* A rectangular grid of characters consisting only of `.`, `^`, and exactly one `S`.

### Grid Rules & Constraints

* The grid may be any reasonable size (≥ 1×1).
* `S` appears exactly once and is never the bottom row.
* All beams always move **down** (increasing row index).
* Beams spawn new beams when hitting a splitter.
* Beams may go off the grid; then they disappear.
* No cycles exist because all beams always move strictly downward.

---

## **4. Expected Outputs**

* A single integer:
  **The total number of splits** (i.e., number of times any beam enters a splitter).

---

## **5. Rules + Logic Requirements**

1. **Initial Beam Spawn**

   * Identify the column of `S`.
   * The first beam starts in the cell immediately **below** `S`, moving downward.

2. **Beam Movement**

   * Beams advance **one row downward per step**.
   * If they move into:

     * `.` → continue downward.
     * Off-grid → the beam disappears.
     * `^` → trigger a split event.

3. **Splitter Behavior**

   * When a beam enters a `^`:

     * Increment split counter by **1**.
     * The beam **stops** and is removed.
     * Two new beams spawn:

       * One in the cell left of the splitter (`row, col-1`)
       * One in the cell right of the splitter (`row, col+1`)
     * Both new beams begin moving downward next step.

4. **Beam Termination**

   * A beam disappears if:

     * It moves past the bottom of the grid.
     * It moves out of horizontal bounds.
     * It hits a splitter and stops (replaced by spawned beams).

5. **Simulation Ends When**

   * No beams remain in the grid.

6. **Count All Splits**

   * If multiple beams hit the same splitter at different times, each hit counts individually.

---

## **6. Edge Cases**

* Splitter located directly below `S`.
* Multiple beams spawning off-sides (left or right beam off-grid immediately).
* Splitter near edges causing only one new beam to spawn.
* A tall grid with no splitters → result is `0`.
* Multiple beams reaching different splitters in the same step.
* Narrow grid (width 1).

---

## **7. Sample Tests**

### Test 1: No splitters

Grid:

```
.S.
...
...
```

Result: **0**

---

### Test 2: Single splitter directly below S

```
.S.
.^.
...
```

Events:

* Beam enters `^` → split count = 1
* Left beam off-grid; right beam continues down.
  Total = **1**

---

### Test 3: Example cascade

```
..^..
.S.^.
..^..
.....
```

A beam may hit multiple splitters sequentially, spawning chains.
Expected: count all split events individually.

---

## **8. Solution Outline (High Level)**

1. Load the grid and locate `S`.
2. Create an initial beam at `(row_of_S+1, col_S)`.
3. Use a queue or list of active beams.
4. While beams exist:

   * For each beam:

     * Move down one row.
     * If off-grid → remove.
     * If empty → keep moving.
     * If splitter:

       * Increment split counter.
       * Remove the beam.
       * Spawn left and right child beams if inside grid.
5. Continue until no beams remain.
6. Return split counter.

---

## **9. Flow Walkthrough**

Example:

```
Row 0: ..S..
Row 1: ..^..
Row 2: .....
Row 3: .....
```

* Initial beam starts at (1,2)
* Step 1: beam enters `^` →

  * split_count = 1
  * Left beam at (1,1), Right beam at (1,3)
* Step 2:

  * Both beams move to row 2
* Step 3:

  * Both continue to row 3
* Step 4:

  * Both exit grid → simulation ends.

Final output = **1**

---

## **10. Implementation Plan (Language-Agnostic)**

1. Parse grid into 2D array.
2. Find coordinates of `S`.
3. Initialize beam list with one beam directly below `S`.
4. Loop while beams list is not empty:

   * Create new list for next-step beams.
   * For each beam:

     * Compute next row, same column.
     * If out of bounds → skip.
     * If cell is `.` → append updated beam to next-step list.
     * If cell is `^`:

       * Increment split counter.
       * If left cell exists, add beam (row, col-1).
       * If right cell exists, add beam (row, col+1).
5. Replace beams list with next-step beams.
6. Output the split counter.

---

## **11. Real-World Analogy + Practical Use Case**

This models:

* Light-beam propagation through optical splitters
* Event-driven particle propagation in physics simulations
* Branching logic flows
* Downward-only DAG traversal with splitting nodes

It is a deterministic breadth-first simulation of downward-moving particles.


---

Our first implementation failed, and here is a SpecForge generated summary of what was missed in the original requirements that caused this issue:

# ✅ **1. Missing Rule: Beams Must Not Revisit the Same Cell**

The puzzle text **did not say** what happens if a beam returns to a location that *another beam* (or the same beam’s earlier clone) has already visited.

### Why this matters:

Without this rule:

* Beams split into more beams
* Those beams split into more beams
* And some of those beams can **re-enter the same cell from above again**
* The process repeats forever

This creates **exponential beam growth** and **infinite loops**, because nothing prevents beams from triggering the same splitter repeatedly.

### What was needed:

A beam state must be pruned if its `(row, col)` has already been processed.

This transforms the simulation from infinite → finite.

---

# ✅ **2. Incorrect Interpretation of Where Child Beams Spawn**

The requirements say:

> The splitter creates two new beams, one starting in the cell immediately to the left and one immediately to the right.

The original implementation placed child beams **one row below the splitter**, but the correct interpretation is:

### Correct:

```
Parent beam enters (r, c)
New beams spawn at:
   (r, c-1)
   (r, c+1)
```

### Incorrect (what we originally did):

```
Spawn at (r+1, c-1) and (r+1, c+1)
```

This mistake allowed:

* Child beams to propagate downward *before* interacting horizontally
* Some cross-beam interactions to be impossible
* Some infinite horizontal loops to appear
* Split cascades not matching puzzle expectations

---

# ✅ **3. Missing “State-Based Simulation” Concept**

AoC puzzles like this almost always depend on:

* **State deduplication**
* **Finite visit sets**
* **Beam caching**

The puzzle didn’t explicitly state this, but **you must simulate a DAG**, not an infinite branching graph.

---

# ✅ **4. Assumption That All Beams Must Always Be Simulated Raw**

Early attempts assumed:

> Every beam must continue moving until it individually leaves the grid.

This is technically true *if beams never re-enter the same square*, but in this puzzle **they can re-enter**, and that breaks assumptions unless we enforce a visited-state rule.

The missing mental model:

### Beams do NOT represent unique physical particles

They represent **logical simulation states**, and once a state repeats, nothing new can happen.

---

# ✅ **5. Why the Original Code Ran Forever**

Because beams:

* Moved down
* Hit splitters
* Spawned left/right beams
* Those beams moved down
* Hit *other* splitters
* Spawned more beams
* Some eventually moved back under the original splitter column
* Re-hit the same splitter
* Spawned *again*
* Repeat forever

No termination occurs because **splitters continue firing infinitely**, which was not intended by the puzzle.

Once we added:

```
if (r, c) in visited:
    continue
```

the infinite chain is cut.

---

# 🎯 **Final Summary — What You Missed in the Requirements**

Here are the exact requirement gaps that caused issues:

### **❌ Missing requirement:**

“No beam should be processed more than once at the same grid position.”

### **❌ Missing detail:**

Child beams spawn **in the same row as the splitter**, not below.

### **❌ Unspoken assumption:**

Beam simulation must be **state-based**, not particle-based.

### **❌ Hidden expectation:**

The grid defines a downward DAG; cycles must not be allowed.

---

# ✅ Corrected mental model

A beam simulation step represents:

* **State transitions**, not new physical particles
* **Finite unique beam positions**
* **Single processing per coordinate**

Once understood this way, the puzzle behaves as intended and finishes instantly.
