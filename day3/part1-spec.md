# **1. Problem Summary**

You are given multiple input lines.
Each line is a **bank of batteries**, represented as a string of digits (`1–9`).
From each bank, you must choose **exactly two digits**, in their original left-to-right order, to form a **two-digit number**.
For each bank, choose the pair that forms the **largest possible two-digit number**.
Then **sum all those maximum values**.

---

# **2. Domain Entities**

* **Bank** — a string of digits (`'1'` through `'9'`), one bank per line.
* **Battery** — a single digit representing a joltage rating.
* **Chosen pair** — two digits `(i, j)` from a bank with `i < j`.
* **Two-digit joltage** — integer formed by concatenating the two chosen digits.

---

# **3. Inputs + Constraints**

* Input consists of **multiple lines**, each a string of digits.
* Digits are all in the range `'1'`–`'9'`; zero does not appear.
* Each bank:

  * contains at least **two digits** (so a valid pair always exists).
  * may be arbitrarily long.
* No reordering allowed; positions must satisfy `i < j`.

---

# **4. Expected Outputs**

* A **single integer**:
  The **sum** over all banks of their **maximum achievable two-digit number** (formed from two digits in order).

---

# **5. Rules + Logic Requirements**

### Per bank:

1. You must choose exactly **two digits**.
2. Order must follow original positions:

   * If digits are at indices `i` and `j`, then `i < j`.
3. The joltage equals `10 * digit[i] + digit[j]`.
4. Among all valid `(i, j)` pairs, choose the one giving the **maximum** two-digit value.

### After processing all banks:

* Compute the sum of all chosen maximum joltages.
* Return that sum as the final answer.

---

# **6. Edge Cases**

* Banks where the **first digit is already the best tens digit**.
* Banks where the **largest digit appears only at the end**.
* Banks where **multiple equal-best two-digit numbers** exist (just choose any; they are equal).
* Long banks with many digits.
* Banks like `"11"` → only pair is `"11"` → value 11.

---

# **7. Sample Tests**

### Test 1

Input:

```
12345
```

Pairs include 12, 13, 14, 15, 23, 24, 25, 34, 35, 45.
Max = **45**

### Test 2

Input:

```
98
```

Only possible pair → 98.
Sum = **98**

### Test 3

Input:

```
5173
```

All valid pairs:
51, 57, 53, 17, 13, 73
Max = **73**

### Test 4

Input:

```
29
83
741
```

Results:
29 → 29
83 → 83
741 → best pairs: 74, 71, 41 → max 74
Sum = 29 + 83 + 74 = **186**

---

# **8. Solution Outline (High Level)**

For each line:

* Consider every pair `(i, j)` with `i < j`.
* Compute the two-digit number formed by `digit[i]` and `digit[j]`.
* Track the maximum across all pairs.
  Sum these maxima across all lines.

---

# **9. Flow Walkthrough**

Example bank: `"5173"`

* Compare all pairs:
  5→1 → 51
  5→7 → 57
  5→3 → 53
  1→7 → 17
  1→3 → 13
  7→3 → 73
* Maximum is 73.
  Add this to the running total.

---

# **10. Implementation Plan (Language-Agnostic)**

### Per bank:

```
parse the digits
max_value = 0
for i from 0 to len(bank)-2:
    for j from i+1 to len(bank)-1:
        value = 10 * bank[i] + bank[j]
        if value > max_value:
            max_value = value
return max_value
```

### Overall:

```
total = 0
for each bank in input:
    total += max_value_for_bank(bank)
return total
```

---

# **11. Real-World Analogy + Practical Use Case**

This resembles selecting two components in a fixed sequence to maximize combined performance, where the first contributes “tens weight” and the second “units weight.”
It is similar to optimization over ordered pairs in scheduling, ranking, or resource pairing tasks where order matters.