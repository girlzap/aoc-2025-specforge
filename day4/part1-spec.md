# **1. Problem Summary**

You are given a 2D grid composed of `@` symbols (paper rolls) and `.` symbols (empty space).
For each roll `@`, you must count how many of its **8 adjacent cells** (including diagonals) also contain `@`.
A roll is **accessible** if it has **fewer than 4** adjacent rolls.
The required output is the **total number of accessible rolls** in the grid.

---

# **2. Domain Entities**

**Grid**

* A 2D arrangement of characters.

**Cell**

* Contains either `@` (roll) or `.` (empty).

**Adjacent positions**

* The eight surrounding cells: N, NE, E, SE, S, SW, W, NW.

**Accessible Roll**

* A roll that has fewer than 4 adjacent `@` cells.

---

# **3. Inputs + Constraints**

**Input:**

* A multiline grid of characters, each row of equal length (rectangular grid).
* Characters allowed: `@` and `.`.

**Constraints:**

* The grid may be any size ≥ 1×1.
* Treat out-of-bounds adjacency checks as nonexistent (ignored).
* Whitespace or blank lines outside the grid should be ignored.

---

# **4. Expected Outputs**

* A single integer: the count of rolls (`@`) that have **< 4** adjacent rolls.

---

# **5. Rules + Logic Requirements**

1. For each cell containing `@`, examine its 8 neighbors.
2. Count how many of those neighbors also contain `@`.
3. If this count is **fewer than 4**, mark the roll as **accessible**.
4. Sum all accessible rolls.
5. Edge boundaries must not cause errors; off-grid neighbors are skipped.

---

# **6. Edge Cases**

* **Single-cell grid** (`@` or `.`).

  * A solitary `@` has 0 neighbors → accessible.
* **All dots**: result = 0.
* **All @’s in a dense block**: center rolls likely exceed adjacency threshold, but edges and corners may be accessible.
* **Non-rectangular input lines**: treat as invalid unless guaranteed rectangular (assume valid per problem statement).
* **Rows or columns of length 1**: adjacency reduces accordingly.

---

# **7. Sample Tests**

### **Test 1**

**Input:**

```
@
```

**Expected Output:**
`1`
**Reasoning:** Single roll, 0 neighbors < 4 → accessible.

---

### **Test 2**

**Input:**

```
@@
@@
```

**Expected Output:**
`4`
**Reasoning:**
Each roll has 3 neighbors → all accessible (3 < 4).

---

### **Test 3**

**Input:**

```
.@.
@@@
.@.
```

**Expected Output:**
`4`
**Reasoning:**
The center `@` has 4 adjacent `@` → NOT accessible.
All others have fewer than 4 → accessible.

---

### **Test 4**

**Input:**

```
...
.@.
...
```

**Expected Output:**
`1`
**Reasoning:** The single `@` has 0 neighbors.

---

# **8. Solution Outline (High Level)**

1. Read the grid into a 2D structure.
2. Iterate through every cell.
3. When encountering a `@`, inspect all 8 neighbor positions.
4. Count neighbors containing `@`.
5. If the count is < 4, increment an accessible counter.
6. Output the counter.

---

# **9. Flow Walkthrough**

Using sample test 3:

Grid:

```
.@.
@@@
.@.
```

Evaluate the center roll at (1,1):

* Its neighbors include all 8 directions.
* Adjacent `@` count = 4.
* Since 4 is not < 4, it is *not accessible*.

Evaluate roll at (0,1):

* Neighbors include 3 adjacent `@` cells.
* 3 < 4 → accessible.

Repeating this logic for each roll yields 4 accessible rolls.

---

# **10. Implementation Plan (Language-Agnostic)**

1. **Parse input**

   * Split input into lines.
   * Store as a 2D array of characters.

2. **Define adjacency directions**

   * List of 8 (dx, dy) offset pairs for neighbors.

3. **Initialize counter**

   * `accessible_count = 0`.

4. **Iterate grid cells**

   * For each (r, c):

     * If cell is not `@`, continue.

5. **Count neighbors**

   * For each direction offset:

     * Compute neighbor position.
     * If in bounds and equals `@`, increment neighbor counter.

6. **Check accessibility**

   * If neighbor count < 4 → increment `accessible_count`.

7. **Return the result**.

---

# **11. Real-World Analogy + Practical Use Case**

This mimics evaluating whether a forklift can access a pallet in a warehouse based on how many surrounding positions are blocked.
In computer science, this is similar to grid-based simulations such as cellular automata, pathfinding occlusion analysis, and adjacency-based rule systems.