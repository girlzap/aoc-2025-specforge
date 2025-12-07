## **1. Problem Summary**

You are given a horizontally arranged “math worksheet.”
Each column block corresponds to one *problem*.
A problem consists of multiple vertically stacked numbers and one operator (`+` or `*`) in the bottom row.
Your task is to:

* Parse each problem block,
* Extract its numbers and operator,
* Compute the result of each problem,
* Sum all results into a final total.

---

## **2. Domain Entities**

* **Worksheet Grid**: A rectangular text matrix of characters.
* **Problem Block**: A contiguous set of non-space columns representing one math problem.
* **Digits Row**: Any row above the operator row that contains digits.
* **Operator Row**: The final row; contains `+` or `*` inside each problem block.
* **Number**: A vertical slice of digits within one block, combined top→bottom.
* **Problem Result**: Sum or product of all numbers in that block.

---

## **3. Inputs + Constraints**

### Input Format

* One or more rows of characters.
* All rows are the same width after right-padding with spaces.
* Last row contains only operators and spaces.
* Problems are separated by **at least one full column of spaces**.
* Inside a problem block:

  * Columns are contiguous.
  * Numbers may be left- or right-aligned.
  * Digits appear on any rows except last.
  * Operator appears only in the last row.

### Constraints

* Operators are only `+` or `*`.
* There is exactly one operator per problem block.
* There is at least one number per problem block.
* Blocks appear left→right in arbitrary width.
* No upper bound on block size or row count.

---

## **4. Expected Outputs**

Output a **single integer**:
The **sum of all computed problem results**.

---

## **5. Rules + Logic Requirements**

1. Identify problem blocks by scanning columns:

   * A block begins where a column has at least one non-space,
   * It ends before the next all-space column segment.
2. For each block:

   * Read downward through all rows **except the last**.
   * Extract digit sequences inside the block.
   * Combine digits on the same row into a number if multiple digits appear.
3. Operator parsing:

   * The last row of the block must contain exactly one `+` or `*`.
4. Computing each problem:

   * If operator is `+`: sum all numbers.
   * If operator is `*`: multiply all numbers.
5. The final answer is the sum of all problem results.

---

## **6. Edge Cases**

* Blocks of varying width.
* Single-digit or multi-digit numbers.
* Empty rows except operator row (numbers missing on some rows).
* Irregular alignment (left or right justified).
* Numbers stacked without any numeric alignment convention.
* Operators appearing in any column of the block as long as they are in the last row.
* Multiple digits per row inside a block → combine those into a single number.

---

## **7. Sample Tests**

### Test 1 (from prompt)

Worksheet:

```
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
```

Parsed problems:

1. `123 * 45 * 6`
2. `328 + 64 + 98`
3. `51 * 387 * 215`
4. `64 + 23 + 314`

Individual results:

* 1 → 331,200
* 2 → 490
* 3 → 4,253,  etc.
  → Sum = final output.

---

### Test 2

```
12   5
34   7
*    +
```

Problems:

* `12 * 34` = 408
* `5 + 7` = 12
  Total = **420**

---

### Test 3

```
 9   88
77   2
+    *
```

Problems:

* `9 + 77` = 86
* `88 * 2` = 176
  Total = **262**

---

## **8. Solution Outline (High Level)**

1. Read worksheet as a grid; right-pad rows to equal width.
2. Scan column-by-column to detect contiguous non-space column blocks.
3. For each block:

   * Extract operator from bottom row.
   * For every row above:

     * Identify digit sequences in that column slice.
     * Convert each digit sequence into a number.
4. Compute problem result based on the operator.
5. Add all results together.
6. Output the final sum.

---

## **9. Flow Walkthrough**

Using the main example:

* Scan columns → four blocks identified.
* Block 1 columns contain digits for `123`, `45`, `6`, operator `*`.
* Numbers extracted:

  * Row 0: "123"
  * Row 1: "45"
  * Row 2: "6"
* Operator row: "*"
* Compute `123 * 45 * 6`.

Repeat for each block, then sum all results.

---

## **10. Implementation Plan (Language-Agnostic)**

1. Read all lines.
2. Normalize row widths.
3. Identify problem blocks:

   * For each column index:

     * Check if any row has a non-space.
     * Group contiguous such columns.
4. For each block:

   * Extract operator from bottom row.
   * For each row above bottom:

     * Slice block portion.
     * Use digit detection to extract numeric sequences.
5. Convert sequences to integers.
6. Compute block result:

   * Choose addition or multiplication.
7. Accumulate grand total.

---

## **11. Real-World Analogy + Practical Use Case**

This problem simulates:

* Parsing columnar OCR data,
* Extracting tabular fields from monospace logs,
* Segmenting visual spreadsheet regions,
* Columnar text mining where fields are spatially separated.

It trains interval segmentation, grid interpretation, and hierarchical parsing.