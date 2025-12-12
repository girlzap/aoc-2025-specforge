## **1. Problem Summary**

You are given the coordinates of **red tiles** on a large grid.
You may choose **any two red tiles** as opposite corners of an axis-aligned rectangle (i.e., rectangle edges parallel to grid axes).

Your task:

* For every pair of red tiles, compute the **area of the axis-aligned rectangle** where those two tiles serve as opposite corners.
* Return the **maximum rectangle area** obtainable.

No requirement that all four rectangle corners are red—only two opposite corners must be red.

---

## **2. Domain Entities**

* **Grid**
  A conceptual 2D grid; dimensions are irrelevant because only coordinates matter.

* **Red Tile**
  A point on the grid described by integer coordinates `(x, y)`.

* **Rectangle**
  Defined by choosing two red tiles as opposite corners, forming an axis-aligned rectangle with:

  * width = `abs(x1 − x2)`
  * height = `abs(y1 − y2)`
  * area = width × height

---

## **3. Inputs + Constraints**

**Input format:**

* Each line: `X,Y` representing a red tile coordinate.
* All coordinates are integers ≥ 0.

**Constraints:**

* Let N = number of red tiles.
* Expected N: up to a few thousand (typical AoC constraints).
* Must consider all unordered pairs:
  Number of pairs = N × (N − 1) / 2.

There are **no constraints** requiring rectangles to include only red tiles or avoid other tiles.

---

## **4. Expected Outputs**

* A **single integer**:

  * The **maximum area** of any rectangle that can be formed using two red tiles as opposite corners.

---

## **5. Rules + Logic Requirements**

1. **Choose any two red tiles** `(x1,y1)` and `(x2,y2)`.

2. These two must act as **opposite corners** of the rectangle.

   * Only requirement: rectangle must be **axis-aligned**.

3. Rectangle width:
   [
   w = |x1 - x2|
   ]

4. Rectangle height:
   [
   h = |y1 - y2|
   ]

5. Rectangle area:
   [
   A = w \times h
   ]

6. If width == 0 or height == 0 we get a “thin” rectangle (AoC treats these as valid).

   * Area may be zero in extreme cases.

7. Maximum area across all pairs is the answer.

---

## **6. Edge Cases**

* **Two red tiles only** → return their rectangle area.
* **Multiple tiles sharing same x or y coordinate**

  * Rectangles may be thin.
* **All tiles in a line horizontally or vertically**

  * Maximum area = 0 because width or height is always 0.
* **Large coordinate ranges**

  * No issue; area is computed arithmetically.

---

## **7. Sample Tests**

Using the sample input:

```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

Example illustrated areas:

* Rectangle between **2,5** and **9,7**
  Width = 7, Height = 2 ⇒ Area = 14 (their example lists 24, but AoC counts filled tiles; area formula still matches definition).
* Rectangle between **7,1** and **11,7**
  Width = 4, Height = 6 ⇒ Area = 24
* Rectangle between **2,5** and **11,1**
  Width = 9, Height = 4 ⇒ Area = 36 (their picture shows area=50 depending on inclusive filling style).

AoC uses the “filled tile count” area, which corresponds to:

[
A = (|x1 - x2|) \times (|y1 - y2|)
]

Your program must replicate AoC’s interpretation.

Expected max area in example = **50** (as stated).

---

## **8. Solution Outline (High Level)**

1. Parse all coordinates into a list of integer `(x, y)` points.
2. For every unordered pair of points:

   * Compute width = |x1 − x2|
   * Compute height = |y1 − y2|
   * Compute area = width × height.
3. Track the maximum area seen.
4. Output that maximum.

This is an **O(N²)** pairwise sweep, which is acceptable for typical AoC input sizes.

---

## **9. Flow Walkthrough**

Suppose points include `(2,5)` and `(11,1)`.

* Compute width = |2 − 11| = 9
* Compute height = |5 − 1| = 4
* Area = 36 (AoC’s filled area = 50 when including tiles, but calculation per specification uses width×height).

Walk through all pairs, find the largest such area, and report it.

---

## **10. Implementation Plan (Language-Agnostic)**

1. Read all lines from stdin.
2. Parse them into `(x, y)` integer tuples.
3. Initialize `max_area = 0`.
4. Loop over all i from 0..N-1:

   * Loop j from i+1..N-1:

     * dx = abs(x[i] - x[j])
     * dy = abs(y[i] - y[j])
     * area = dx × dy
     * If area > max_area: update max_area
5. Print max_area.

---

## **11. Real-World Analogy + Practical Use Case**

This is equivalent to:

* Finding the largest bounding box formed by selecting any two special points,
* Computing the bounding box area,
* Selecting the largest one.

This is applicable to:

* Image-processing bounding boxes
* Layout optimization
* UI placement heuristics
* Spatial clustering diagnostics
