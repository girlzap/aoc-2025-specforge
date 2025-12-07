# ✅ **SpecForge Specification — Day 6 Part 2**

---

## **1. Problem Summary**

You are given a rectangular text grid representing horizontally arranged “cephalopod math” problems.
Unlike Part 1, **numbers are written in vertical columns and problems are read right-to-left.**

Each problem consists of:

* One or more **column-groups**, each group representing a number.
* Columns in a group contain digits from **top (most significant)** to **bottom (least significant)**.
* Problems are separated by at least **one full column of spaces**.
* The **operator (`+` or `*`) appears on the bottom row** in the **rightmost column of that problem**.

Your task is:

1. Parse problems **right-to-left**.
2. Extract numbers (one per column-group).
3. Apply the problem’s operator to all its numbers.
4. Sum all problem results to produce the final output.

---

## **2. Domain Entities**

* **Grid** — The full rectangular character matrix.
* **Column** — A vertical slice of characters from top to bottom.
* **Number Column-Group** — A contiguous block of digit-filled columns forming one integer.
* **Problem Block** — One or more number column-groups ending with a column containing the operator at its bottom cell.
* **Operator** — A `+` or `*` located at the bottom of the last column in a problem.
* **Problem Result** — The computed value after applying the operator to all extracted numbers.

---

## **3. Inputs + Constraints**

### Input Format

* A rectangular grid (rows can be padded with spaces).
* Digits may appear in any row except the last-column operator row.
* Operators appear **only** in the last row.
* Problems may vary in width.
* Problems are separated by at least one **fully blank column**.
* Columns of a number contain only digits (top to bottom).

### Constraints

* Entire worksheet must be parsed from **rightmost column to leftmost**.
* A problem terminates when:

  * Reaching a blank column (space in every row), **or**
  * Reaching the left edge of the worksheet.
* A number terminates when encountering:

  * A blank column, or
  * The start of a new problem (operator column).
* A problem may contain **one or more numbers**.

---

## **4. Expected Outputs**

Output a **single integer**:
The **sum of all problem results** after applying each problem’s operator to its numbers.

---

## **5. Rules + Logic Requirements**

1. **Scanning Direction**

   * Move from **rightmost column** to **leftmost**.
   * Identify problems in decreasing column index order.

2. **Problem Detection**

   * A problem **begins** at a column where the **bottom cell contains an operator**.
   * The problem **extends leftward** until reaching:

     * A fully blank vertical column, indicating separation, or
     * The start of the grid.

3. **Number Extraction**

   * Each number is formed by one **group of contiguous digit columns**.
   * Within a number group:

     * Read columns right-to-left.
     * Within each column, concatenate digits top→bottom.
   * The resulting integer is formed by concatenating the column-values (each column’s top→bottom digits) in right-to-left order.

4. **Operator Application**

   * Apply the operator (`+` or `*`) to all numbers in the problem *in the order extracted*.
   * A problem must contain at least one number.

5. **Final Result**

   * The global answer is the **sum** of all problem results.

---

## **6. Edge Cases**

* Problems with only one number.
* Numbers consisting of a single-digit column.
* Multi-column numbers (digits in multiple vertical slices).
* Rows containing spaces above digits (digit columns may not be aligned).
* Operators touching grid edges.
* Leading blank columns at left or right.
* Problems directly adjacent except for exactly one blank column.
* Very tall grids containing many empty rows between digits.

---

## **7. Sample Tests**

### Example (conceptual)

Suppose rightmost column contains `+`.
Columns to its left contain:

* `3`, `5`, `7` (three number columns)
* Then a blank column
* Then another problem starting at column with `*`.

Parsed as:

Problem A (rightmost):

* Numbers: 7, 5, 3
* Operator: `+`
* Result: `7 + 5 + 3`

Problem B:

* Numbers extracted similarly
* Operator: `*`
* Result: product of numbers

Final output = `result(A) + result(B)`.

### Edge Case Example

Grid:

```
4 3
2 1
* +
```

Interpretation (right to left):

* Right problem: number = 3→1 = 31, operator = `+`
* Left problem: number = 4→2 = 42, operator = `*`

Grand total = 31 + 42.

---

## **8. Solution Outline (High Level)**

1. Normalize lines to equal width.
2. Iterate columns from rightmost to leftmost:

   * If bottom cell is an operator → begin new problem.
3. While in a problem:

   * Move leftward, grouping digit-only columns into numbers.
   * Stop when encountering a blank column (problem boundary).
4. For each problem:

   * Apply operator to extracted numbers.
5. Sum all problem results and output.

---

## **9. Flow Walkthrough**

For a problem ending at column `C_op`:

1. Read operator at `(last_row, C_op)`.
2. Initialize empty list of numbers.
3. Move leftward:

   * If column contains digits → begin building number:

     * Collect contiguous digit columns.
     * For each column, read digits top→bottom.
     * Concatenate column-digits right→left to form integer.
   * If blank column encountered → end problem.
4. Reverse number list if necessary to maintain extraction order.
5. Compute the problem result.
6. Add to running total.
7. Continue scanning left for the next operator.

---

## **10. Implementation Plan (Language-Agnostic)**

1. **Read and normalize input**

   * Pad all rows to the same width.

2. **Column Analysis**

   * For each column index:

     * Determine if it is blank.
     * Determine if bottom row contains operator.
     * Determine if a column contains digits.

3. **Problem Parsing Loop**

   * For column `c` from rightmost down to 0:

     * If operator column → begin problem.
     * Move left to accumulate number groups.
     * Each number group:

       * Collect consecutive digit-columns.
       * For each column, build string from digits top→bottom.
       * Combine these into a number.
     * Stop at blank column.

4. **Compute Problem Result**

   * If operator is `+`: sum numbers.
   * If operator is `*`: multiply numbers.

5. **Accumulate and Output Total**

   * Keep running total.
   * Print final sum.

---

## **11. Real-World Analogy + Practical Use Case**

This models:

* Parsing right-justified columnar data (common in legacy mainframe output),
* Reverse-reading digit streams (similar to Arabic vs. RTL numeric parsing),
* Constructing tokens from vertical slices (OCR / document layout analysis),
* Extracting structured information from monospaced grid encodings.

It is an interval/segmentation problem combined with digit reconstruction.