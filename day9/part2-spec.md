## **1. Problem Summary**

You are given a list of red tile coordinates forming a closed loop.
Every consecutive pair in the list lies on the same row or column, and the final red tile is connected back to the first.

Between each pair of red tiles, a straight path of **green tiles** connects them.
Additionally, **every tile strictly inside the loop** is also green.

Your rectangle must:

* Use **two red tiles** as opposite corners.
* Contain **only red or green tiles** inside its boundary.

Goal: **Find the largest such rectangle (inclusive-area) possible**.

---

## **2. Domain Entities**

* **Red Tile (given list order defines edges)**

* **Green Tile**

  * Tiles on any straight border path between consecutive red tiles.
  * Tiles lying strictly inside the polygon formed by the red-tile loop.

* **Valid Rectangle**

  * Opposite corners = two red tiles.
  * All tiles inside that rectangle must be red or green.

---

## **3. Inputs + Constraints**

* Input: list of red tile coordinates `(x, y)` one per line.
* The list forms a **simple orthogonal polygon** (edges horizontal or vertical).
* Coordinates are integers ≥ 0.
* N (red tiles) typically a few thousand.
* Grid itself is large but sparse; only red and green tiles matter.

---

## **4. Expected Outputs**

A single integer:

[
\max\big((|x_1 - x_2|+1)(|y_1 - y_2|+1)\big)
]

over all red-tile pairs `(p1, p2)` such that **every tile inside the rectangle** is red or green.

---

## **5. Rules + Logic Requirements**

### **5.1 Interior region**

* Red tiles define a closed Manhattan-loop polygon.
* Green tiles include:

  1. All border-path tiles between consecutive red points.
  2. All tiles strictly inside the polygon.

This is simply the complete filled polygon (orthogonal).

### **5.2 Rectangle validity**

For rectangle with corners:

```
(x1, y1)  and  (x2, y2)
```

Let bounding box be:

```
xmin = min(x1, x2)
xmax = max(x1, x2)
ymin = min(y1, y2)
ymax = max(y1, y2)
```

The rectangle includes the tile set:

```
{x | xmin ≤ x ≤ xmax} × {y | ymin ≤ y ≤ ymax}
```

**Rectangle is valid if and only if every tile in this range is RED or GREEN.**

Therefore:

* Rectangle must lie entirely inside **or on the boundary** of the red/green polygon.

### **5.3 Computational requirement**

We need to very efficiently determine whether the entire axis-aligned rectangle lies inside/on a polygon.

Equivalent check:

* The rectangle must be fully contained in the polygonal region defined by the red-tile loop.

Since the polygon is orthogonal, this becomes:

A rectangle is valid iff:

For all x between xmin..xmax, the vertical segment [ymin, ymax] lies inside/on the polygon.

OR equivalently:

For all y between ymin..ymax, the horizontal segment [xmin, xmax] lies inside/on the polygon.

We need a fast point-in-orthogonal-polygon query or a fast interior mask.

---

## **6. Edge Cases**

* Rectangle extends outside the polygon → invalid.
* Rectangle touches border → valid.
* Vertical or horizontal rectangle possible.
* Polygon may have concave corners.

---

## **7. Sample Tests**

### Example from prompt:

* Max area = **24**
* Achieved by rectangle between red tiles `(9,5)` and `(2,3)`.

---

## **8. Solution Outline (High Level)**

1. **Parse red tiles**.
2. **Reconstruct polygon edges**:

   * For each consecutive pair: fill all tiles between them.
3. **Rasterize the polygon interior**:

   * Compute bounding box of polygon.
   * Use horizontal scanline fill to mark interior tiles as green.
4. **Build a 2D boolean grid** marking allowed tiles (`True` = red/green).
5. **For every pair of red tiles**:

   * Compute bounding box `(xmin..xmax, ymin..ymax)`.
   * Check sub-rectangle validity using **2D prefix sums**:

     * Precompute `blocked_sum[y][x] = number of non-green tiles inside prefix`.
     * Rectangle valid if block_count == 0.
   * Compute inclusive area.
   * Track maximum.

This yields an **O(N²)** rectangle check using **O(1)** queries.

---

## **9. Flow Walkthrough**

Given two red tiles `(9,5)` and `(2,3)`:

1. Bounding box spans x = 2..9, y = 3..5.
2. Every point in this region is inside the polygon (green).
3. Area = (9–2+1) × (5–3+1) = 8 × 3 = 24.

---

## **10. Implementation Plan (Language-Agnostic)**

Steps:

### A. Read red tiles.

### B. Generate green border tiles:

For each segment:

* If horizontal: fill x-range at fixed y.
* If vertical: fill y-range at fixed x.

Store tiles in a grid dictionary or dynamic boolean grid.

### C. Compute polygon interior via scanline:

* Determine min/max x,y of polygon.
* For each row y:

  * Find all intersections of the polygon edges with that row.
  * Sort intersections.
  * Fill interior spans.

This yields green interior tiles.

### D. Build `allowed[y][x] = True` mask.

### E. Build 2D prefix sum array `bad[y][x]` where:

* `1` = tile is **outside** allowed area.
* Then `bad_prefix` enables O(1) rectangle checks.

### F. For each unordered pair of red tiles:

* Compute xmin, xmax, ymin, ymax.
* Query rectangle sum via prefix.
* If zero → valid; compute area.

### G. Return max area.

---

## **11. Real-World Analogy + Practical Use Case**

This is exactly a **containment check for axis-aligned bounding boxes inside an orthogonal polygon**, used in:

* Image crop validation
* Floorplan layout tools
* CAD system bounding-region constraints
* 2D physical simulation collision envelopes
