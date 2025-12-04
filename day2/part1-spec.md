Below is your **SpecForge structured specification** for the described problem.

---

# **1. Problem Summary**

You receive one long input line containing multiple **inclusive numeric ranges** in the form `start-end`, separated by commas.
For every integer within every range, you must detect **invalid IDs**, where an invalid ID is any number whose decimal representation consists of **a non-empty substring repeated exactly twice** (e.g., `"x" + "x"` or `"abc" + "abc"`).
Your final task is to compute the **sum of all such invalid IDs**.

---

# **2. Domain Entities**

* **Range** – a pair `(start, end)` of positive integers.
* **ID** – an integer value within one of the ranges.
* **Invalid ID** – an integer whose decimal string has:

  * even length, and
  * first half equals second half.
* **Input line** – a single string containing comma-separated ranges.

---

# **3. Inputs + Constraints**

* Input is a **single line string** such as:
  `11-22,95-115,998-1012`

* Each component is:

  * A positive integer with no leading zeroes.
  * A hyphen-separated range `"start-end"`.

* Range constraints:

  * `start <= end`
  * Values may be large (no explicit upper bound given).
  * Potentially many ranges (performance considerations apply).

* Implied constraints:

  * IDs do **not** contain leading zeroes.
  * Only **exactly-two repetitions** count (not 3×, 4×, etc).

---

# **4. Expected Outputs**

A **single integer** equal to:

> The sum of all invalid IDs found across all inclusive ranges.

---

# **5. Rules + Logic Requirements**

### A. Invalid ID Rules

A number `N` is invalid **iff**:

1. Let `s = decimal string of N`.
2. `len(s)` is **even**.
3. Let `half = len(s) / 2`.
4. `s[0:half] == s[half:]`.

Examples:

* `55` → `"5"` + `"5"` → invalid
* `6464` → `"64"` + `"64"` → invalid
* `123123` → `"123"` + `"123"` → invalid

### B. Processing Rules

* For each `start-end`:

  * Enumerate integers `n` from `start` to `end`, inclusive.
  * Test each using the invalid-ID rule.
  * Accumulate the sum of those that qualify.

### C. No leading zero handling needed:

* IDs like `0101` will never appear.

---

# **6. Edge Cases**

* **Very large ranges** (e.g., millions of values). Need efficient detection logic; avoid brute force if necessary.
* **Single-value ranges** like `"7-7"`.
* **No invalid IDs at all** → output `0`.
* **Large invalid IDs** (e.g., repeating large substrings).
* **Ranges containing numbers of mixed digit lengths**:

  * E.g., `95-115` crosses from 2-digit to 3-digit; invalid patterns depend on digit length.

---

# **7. Sample Tests**

### **Test 1**

Input:
`11-22`
IDs: 11,12,13,…22
Invalid IDs:

* `11` ( "1" + "1" )
* `22` ( "2" + "2" )
  Sum = 11 + 22 = **33**

### **Test 2**

Input:
`95-115`
Two-digit invalids: `99` → 99
Three-digit invalids: none (digit length odd)
Sum = **99**

### **Test 3**

Input:
`6464-6464`
Only one number: 6464
Invalid: "64" + "64"
Sum = **6464**

### **Test 4**

Input:
`123120-123140`
Invalid IDs (pattern “XYZXYZ”):

* `123123` → invalid
  Others unlikely
  Sum = **123123**

---

# **8. Solution Outline (High Level)**

1. **Parse input** into ranges.
2. For each range:

   * Iterate integers from start to end.
   * Convert to string or use arithmetic method.
   * Check if length is even; if not, skip.
   * Split into halves.
   * Validate equality of halves.
3. Maintain a cumulative sum of all invalid numbers.
4. Return the final sum.

For performance, you may:

* Avoid string creation by using digit arithmetic—but strings are simplest.
* Optionally detect entire subranges with fixed digit length and generate only candidates of form `XY` → `XYXY`.

---

# **9. Flow Walkthrough**

**Example input:** `"95-115"`

1. Parse → ranges = [(95, 115)]
2. Loop `n = 95 .. 115`.
3. Convert to strings:

   * 95 → `"95"` → halves: `"9"` vs `"5"` → not equal.
   * …
   * 99 → `"99"` → `"9"` vs `"9"` → invalid → add 99.
   * 100 → `"100"` length odd → skip.
   * …
   * 115 → `"115"` length odd → skip.
4. Sum accumulated = 99.
5. Output = **99**.

---

# **10. Implementation Plan (Language-Agnostic)**

### A. Parsing

* Split input on commas.
* For each token:

  * Split on `-` → `(start, end)` as integers.

### B. Invalid-ID Check

Define a function:

```
function isInvalid(id):
    s ← decimal string of id
    L ← length of s
    if L is odd: return false
    H ← L / 2
    if s[0:H] == s[H:L]:
        return true
    else:
        return false
```

### C. Main Iteration

```
sum ← 0
for each (start, end) in ranges:
    for id from start to end:
        if isInvalid(id):
            sum ← sum + id
return sum
```

### D. (Optional Optimization)

* Precompute all repeated-half numbers for each digit length range.
* Check if they fall within the numeric range.

---

# **11. Real-World Analogy + Practical Use Case**

This task resembles **pattern detection in ID sequences**, commonly used in:

* Fraud detection (e.g., suspicious repeated-pattern identifiers).
* Compression analysis (identifying duplicative numeric substrings).
* Data validation pipelines (spotting non-random or malformed IDs).
* Log analysis for synthetically generated values.

Your solution enforces a structural integrity rule across a large integer domain.
