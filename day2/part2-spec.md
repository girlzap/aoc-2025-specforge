# **1. Problem Summary**

You receive a single line containing comma-separated numeric ranges (`start-end`).
For every integer inside each range, you must detect **invalid IDs**, defined as numbers whose decimal string:

* contains **no leading zeroes**, and
* is composed of some **non-empty digit pattern repeated at least twice** (`k ≥ 2` repeats).

Your task is to **sum all invalid IDs** across all ranges.

---

# **2. Domain Entities**

* **Range** — `(start, end)` inclusive.
* **ID** — integer inside a range.
* **Base pattern** — a non-empty string of digits.
* **Invalid ID** — a number whose string representation = pattern repeated **k times**, where `k ≥ 2`.

---

# **3. Inputs + Constraints**

* A single line string such as:
  `11-22,95-115,998-1012`
* Each token is `"start-end"` using:

  * positive integers
  * no leading zeroes
* Each `start ≤ end`.
* ID sizes can vary (1 digit to many digits).
* Length of ID: up to any reasonable integer size.
* Ranges may be large.

---

# **4. Expected Outputs**

A **single integer** equal to the **sum of all invalid IDs** found across all ranges.

---

# **5. Rules + Logic Requirements**

A decimal integer `N` is **invalid** if:

1. Convert to string `s`.

2. `s` has **no leading zero** (guaranteed by input).

3. There exists an integer `k ≥ 2` and base string `p` such that:

   ```
   s = p repeated k times
   ```

4. Equivalent structural rules:

   * Let `L = len(s)`
   * For some divisor `d` of `L`, where `d < L`:

     * Let `p = s[:d]`
     * If `(p * (L // d)) == s` then `s` is invalid.

Examples:

* `"55"` → `"5"` repeated 2×
* `"6464"` → `"64"` repeated 2×
* `"123123"` → `"123"` repeated 2×
* `"1111111"` → `"1"` repeated 7×
* `"1212121212"` → `"12"` repeated 5×

---

# **6. Edge Cases**

* Single-digit numbers: **never invalid**, because they can’t be ≥ 2 repetitions.
* Numbers with lengths that are **prime** (except multiples of 1) allow only pattern length 1.
* Large ranges that cross digit-length boundaries.
* Very large repeated numbers (e.g., 20-digit patterns).
* Patterns cannot introduce leading zeros (e.g., `"01"` is impossible because the full ID would have a leading zero).

---

# **7. Sample Tests**

### **Test A**

Input:
`11-22`
Invalid:

* 11 → "1"×2
* 22 → "2"×2
  Sum = **33**

### **Test B**

Input:
`95-115`
Invalid:

* 99
  Sum = **99**

### **Test C**

Input:
`111-111`
Invalid:

* 111 = "1" repeated 3×
  Sum = **111**

### **Test D**

Input:
`120120-120120`
Invalid:

* 120120 → "120"×2
  Sum = **120120**

### **Test E**

Input:
`8-9`
Invalid: none
Sum = 0

---

# **8. Solution Outline (High Level)**

1. Parse the input ranges.
2. For each range:

   * Iterate through each ID (or generate matching IDs more efficiently).
3. For each ID:

   * Convert to string.
   * Compute divisors of the string length.
   * For each divisor `d` where `d < L`:

     * Test if the first `d` characters repeated `(L // d)` times equals the full string.
   * If any divisor matches, mark as invalid.
4. Add all invalid IDs into a cumulative sum.
5. Return that sum.

---

# **9. Flow Walkthrough**

Using input:
`111-115`

Check each:

* 111 → length 3
  Divisors of 3: 1
  `"1"*3 = "111"` → invalid → add 111
* 112 → "112" → patterns fail → skip
* 113 → skip
* 114 → skip
* 115 → skip

Final sum = **111**

---

# **10. Implementation Plan (Language-Agnostic)**

### Parsing

* Split on commas.
* For each segment: split on `'-'`.

### Invalid Check (per ID)

```
function isInvalid(s):
    L = length(s)
    for each divisor d of L where d < L:
        p = s[0:d]
        repeats = L // d
        if p repeated repeats == s:
            return true
    return false
```

### Main Loop

```
total = 0
for each (start, end):
    for id from start to end:
        if isInvalid(str(id)):
            total += id
return total
```

### Optional Optimization

* Instead of iterating every number, generate repeated-pattern numbers directly.
* For each digit length L:

  * For each divisor d of L:

    * Generate all patterns of length d (with no leading zeros).
    * Compute `pattern * (L // d)` → candidate ID.
    * Check whether candidate lies in the range.

---

# **11. Real-World Analogy + Practical Use Case**

This matches common data-quality and fraud-detection tasks where numeric sequences must not contain “synthetic repetition patterns.”
Systems often check for identifiers such as 111111, 12121212, 333333, etc., as they are machine-generated or malicious.