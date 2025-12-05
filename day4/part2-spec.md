# **1. Problem Summary**

We are given a 2D grid where each `@` represents a roll of paper and `.` represents empty space.
A roll is **accessible** if fewer than four of its eight neighbors are also `@`.

In Part 2, accessibility is dynamic:

* Accessible rolls are **removed** from the grid.
* After removal, adjacency changes for remaining rolls.
* New rolls may become accessible, triggering additional removal waves.
* Removal waves repeat until no rolls remain with fewer than four neighbors.

The required output is the **total number of rolls removed across all waves**.

---

# **2. Domain Entities**

### **Grid**

A 2D array of characters (`@` or `.`).

### **Roll**

A grid cell containing `@`.

### **Adjacency**

Eight directions: N, NE, E, SE, S, SW, W, NW.
Out-of-bounds neighbors are ignored.

### **Accessible Roll**

A roll whose adjacent-`@` count is **< 4**.

### **Removal Wave**

A simultaneous removal of all currently accessible rolls.
After removal, the grid is updated, and the next wave is evaluated.

### **Simulation**

The repeated cycle of:

1. Identify accessible rolls.
2. Remove them.
3. Recompute adjacency.

---

# **3. Inputs + Constraints**

### **Input**

* A rectangular grid of characters (`@` or `.`).
* Provided as multiple lines of text.

### **Constraints**

* Grid is at least 1×1.
* No non-`@`/`.` characters.
* Removal is simultaneous per wave.
* Process halts when no new roll has < 4 adjacent rolls.

---

# **4. Expected Outputs**

* A **single integer**:
  The total number of rolls removed across all removal waves.

---

# **5. Rules + Logic Requirements**

1. For each iteration:

   * Compute adjacency counts for all `@` cells.
   * Mark every roll with < 4 neighbors as *to be removed*.
2. Remove all marked rolls simultaneously.
3. Update the grid.
4. Repeat until no new rolls qualify.
5. Count total rolls removed.

**Important:**
Neighbor counts are **never incremental**; they must be **recomputed after each wave**, because removals change adjacency patterns.

---

# **6. Edge Cases**

### **No rolls (`.` only)**

Output = 0.

### **All rolls isolated**

Every roll has 0 neighbors → all removed in the first wave.

### **Dense block with no removable rolls**

If all rolls have ≥ 4 neighbors, output = 0.

### **Chain reaction removal**

Removing outer rolls reduces adjacency for inner rolls, enabling multiple waves.

### **Single row or single column**

Adjacency reduces naturally; waves often propagate inward.

### **Asymmetric patterns**

Removal may fragment large shapes, causing complex multi-phase removal.

---

# **7. Sample Tests**

### **Test 1 — Single Roll**

Input:

```
@
```

Wave 1: 0 neighbors → removed
Total removed: **1**

---

### **Test 2 — 2×2 Block**

Input:

```
@@
@@
```

Each roll has exactly 3 neighbors → removed in wave 1
Total removed: **4**

---

### **Test 3 — Plus Shape**

Input:

```
.@.
@@@
.@.
```

Neighbor counts:

* Center = 4 → not removed in wave 1
* All four arms = 3 → removed in wave 1
  After wave 1:
* Center roll now has 0 neighbors → removed in wave 2
  Total removed = 4 + 1 = **5**

---

# **8. Solution Outline (High Level)**

1. **Parse the grid** into a mutable structure.
2. **Iteratively evaluate adjacency** for all current rolls.
3. **Collect all rolls with < 4 neighbors**.
4. If none found → stop.
5. **Remove all collected rolls** simultaneously.
6. Accumulate their count.
7. Repeat from step 2 until no more rolls can be removed.

This is effectively a **layer-peeling** process similar to iterative erosion in cellular automata.

---

# **9. Flow Walkthrough**

Using the plus-shape example:

Grid:

```
.@.
@@@
.@.
```

**Wave 1 adjacency:**

* Center: 4 neighbors → NOT removed
* Arms: each has 3 neighbors → removed

**Remove 4 rolls → total = 4**

Updated grid becomes:

```
...
.@.
...
```

**Wave 2 adjacency:**

* Center roll now has 0 neighbors → removed

Total removed = 5.

No rolls remain → stop.

---

# **10. Implementation Plan (Language-Agnostic)**

1. **Represent the grid**

   * Use a 2D list or matrix of booleans or characters.

2. **Define the 8-direction offsets**

3. **Loop until stable**

   * Initialize `to_remove = empty list`.

4. **Compute adjacency**

   * For each `@` cell:

     * Count neighbors using direction offsets.
     * If < 4, add to `to_remove`.

5. **Check termination**

   * If `to_remove` is empty → halt.

6. **Perform wave removal**

   * Convert each location in `to_remove` to `.`.
   * Increase total-removal counter.

7. **Repeat simulation**

8. **Return total removed**

This is straightforward but must recompute adjacency fresh in each wave.

---

# **11. Real-World Analogy + Practical Use Case**

This resembles:

* Gradual mechanical removal of accessible inventory in a warehouse.
* Cellular erosion (e.g., thinning operations in image processing).
* Peeling layers off an onion: each layer's removal exposes new areas.

Such simulations are common in:

* Cellular automata (Conway-like systems),
* Graph pruning algorithms (e.g., k-core decomposition),
* Structural stress modeling (removing weak nodes causes changes in the structure).