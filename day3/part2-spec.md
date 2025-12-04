# **1. Problem Summary**

You receive multiple lines of input.
Each line is a **bank of batteries**, represented as a sequence of digits (`1–9`).
From each bank, you must select **exactly 12 digits**, keeping their **original left-to-right order**, and concatenate them to form a **12-digit number**.
For each bank, choose the 12-digit number that is **lexicographically and numerically maximal**.
Finally, **sum all per-bank maxima**.

---

# **2. Domain Entities**

* **Bank** — a single line of digits.
* **Battery** — a digit (`1`–`9`), each representing a joltage rating.
* **Selection** — a subsequence of exactly 12 digits from a bank, order preserved.
* **Joltage value** — the 12-digit integer formed from the selected subsequence.

---

# **3. Inputs + Constraints**

* Input: multiple lines, each containing a digit string of length **≥ 12**.
* Digits range from `'1'` to `'9'`; zeros do not appear.
* Every bank:

  * has at least 12 digits, otherwise no valid selection exists.
  * may be very long (hundreds or thousands of digits).
* Must select **exactly 12 digits**, not fewer, not more.
* Order must be preserved; only subsequences allowed.

---

# **4. Expected Outputs**

A single integer:

> The **sum** of the **maximum possible 12-digit number** chosen from each bank.

---

# **5. Rules + Logic Requirements**

### For each bank:

1. Treat the line as a sequence of digits.
2. Must select exactly **12 positions** `i₁ < i₂ < … < i₁₂`.
3. Form the output number:
   `digit[i₁] digit[i₂] … digit[i₁₂]`
4. This number must be the **maximum** among all valid 12-digit subsequences.
5. Comparisons are lexicographic = numeric for equal-length digit strings.

### Across all banks:

* Compute each bank's best 12-digit number.
* Convert to integer and sum all such values.
* That sum is the final answer.

---

# **6. Edge Cases**

* Banks where the first 12 digits already produce the maximum.
* Banks where better digits appear later (must skip earlier digits).
* Banks containing long descending or ascending runs.
* Extremely long banks requiring efficient selection (O(n) or O(n log n)) rather than brute-force combinations (which would be impossible).
* Banks with repeated digits (tie-breaking governed by availability of enough remaining digits).

---

# **7. Sample Tests (Constructed)**

These reflect the logic but are not part of the official puzzle.

### Test A

Bank: `"987654321111111"`
Goal: choose the best 12 digits.
Best = first 12 digits: `987654321111`.

### Test B

Bank: `"811111111111119"`
Best = last digit contributes heavily, so:
`811111111111` vs replacing one of the interior 1s by final 9
Best = `811111111119` (take the final 9 as the last position).

### Test C

Bank: `"234234234234278"`
Best 12-digit subsequence begins by choosing the largest possible digits early while ensuring enough digits remain to fill 12 total.

---

# **8. Solution Outline (High Level)**

Use a **greedy lexicographic subsequence selection**:

* You must select exactly 12 digits.
* While scanning the bank left to right, choose the **largest possible next digit** such that:

  * choosing it still leaves enough remaining digits to reach a total of 12 picks.

Equivalent to:

* For each of the 12 positions you must fill:

  * Look ahead for the **best digit** you can legally choose within the window that still leaves enough digits to finish.

This produces the lexicographically maximum subsequence of fixed length.

Repeat per bank, sum all results.

---

# **9. Flow Walkthrough**

Bank: `"811111111111119"`

Need length 12.

1. For the first position:

   * From index 0 onward, you can pick either `8` (index 0) or search for a `9` later.
   * But if you tried to pick the final `9` as the first digit, you wouldn’t have enough digits left to fill 12 positions.
   * So the first digit must be `8`.

2. For digits 2–11, you’ll pick `1`s from early as long as enough remain.

3. For the final digit:

   * You can choose the last `9`.

Result = `811111111119`.

---

# **10. Implementation Plan (Language-Agnostic)**

### Per Bank:

```
target_len = 12
result = []
start_index = 0

for k in 1..12:
    remaining_needed = 12 - len(result)
    max_pick_index = len(bank) - remaining_needed

    # choose the largest digit in bank[start_index : max_pick_index+1]
    best_digit = -1
    best_pos = -1
    for pos from start_index to max_pick_index:
        if bank[pos] > best_digit:
            best_digit = bank[pos]
            best_pos = pos

    append best_digit to result
    start_index = best_pos + 1
```

### After all banks:

* Convert each result list to an integer.
* Add to running total.
* Output total.

---

# **11. Real-World Analogy + Practical Use Case**

This is a classic **best subsequence selection** problem:
Selecting exactly K items from a stream to maximize lexicographic value while preserving order.
Used in data compression, greedy text selection, scheduling with fixed slots, and choosing optimal ordered subsets.