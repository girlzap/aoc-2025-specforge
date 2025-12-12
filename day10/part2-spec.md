

## **1. Problem Summary**

For each machine:

* You have counters, all starting at **0**.
* You have a required target joltage vector `{t₀, t₁, ..., t_{m-1}}`.
* Each button increases certain counters by **+1** (no XOR).
* You may press buttons any number of times (non-negative integers).
* You want the **fewest total presses** such that the resulting joltage vector equals the target.

We must compute:

[
\sum_{\text{machines}} \text{minimum button presses to reach target}
]

---

## 2. Domain Entities

* **Counters (`m` counters)**

  * Initially all zero.
  * Target is vector `T ∈ ℕ^m`.

* **Buttons**

  * A button is a vector `b ∈ ℕ^m` where:

    * `b[i] = 1` if button increments counter `i`
    * `b[i] = 0` otherwise
  * Pressing a button adds its vector to the current counter vector:
    [
    state := state + b
    ]

* **Solution vector**

  * For each button `j` we choose a number of presses `x_j ≥ 0` (integer).
  * Requirement:
    [
    \sum_j x_j b_j = T
    ]

* **Cost**

  * Number of button presses:
    [
    \text{cost}(x) = \sum_j x_j
    ]

---

## 3. Inputs + Constraints

Format per machine line:

```
[ignore_me] (button1) (button2) ... {t0,t1,...,tm-1}
```

* Indicator diagram `[...]` is ignored.
* Parentheses contain button definitions.
* Curly braces contain target joltage values.
* Number of counters `m` is number of integers inside `{ }`.

**Constraints (AoC typical)**:

* Number of buttons B ~ up to 20–30
* Number of counters m ~ up to 20
* Target magnitudes small-ish (≤ 100ish)
* Guarantee (implicitly) that system is solvable.

---

## 4. Expected Outputs

A single integer = the **sum of minimum button presses** over all machines.

Example answer (from text):
`10 + 12 + 11 = 33`

---

## 5. Rules + Logic Requirements

### 5.1 Core equation

Given button vectors (b_j) and target (T), we need:

[
B x = T
]

where:

* (B) is m×B matrix of 0/1 entries.
* (x) is B-vector of **non-negative integers** (not mod 2).

### 5.2 Cost minimization

We minimize:

[
|x|_1 = \sum_j x_j
]

### 5.3 Observations

* This is a **non-negative integer linear combination** problem.
* All button vectors are 0/1; all counter increments are +1 per press.
* There is **no cancellation** (no subtraction).

### 5.4 Algorithm requirement

Because:

* Target dimensions are small.
* Target magnitudes are small.
* Button increments are small and uniform (+1),
* Buttons add *only* (monotone system),

The system forms a **bounded multi-dimensional BFS shortest path** in ℕ^m:

* Each BFS node is a counter vector.
* Edges correspond to pressing one button.
* We stop when we reach target.

This finds the **minimum total presses**, guaranteed optimal.

But mD BFS state space may be large, so a more efficient form is needed.

### 5.5 Optimized formulation

We instead use:

* **Dijkstra / BFS** over counter vectors because all edge costs = 1.
* Represent counter vectors as small tuples.
* Use pruning:

  * Never explore a state whose any coordinate > target[i].
* State space size is at most:
  [
  \prod_{i=0}^{m-1} (t_i + 1)
  ]
  which is manageable for typical AoC ranges.

Alternative method:

* A* search (heuristic: remaining sum of deficits).
* Or integer DP with memoization.

The BFS approach is cleanest and always correct.

---

## 6. Edge Cases

* **Target = all zeros** → cost = 0.
* **Some counter unreachable** → problem likely avoids this.
* **Buttons that don't affect any counter** → useless, can be ignored.
* **Buttons that affect the same counter multiple times** → impossible (format ensures unique integer indices inside each button).

---

## 7. Sample Tests

#### Machine 1 example:

Target = `{3,5,4,7}`
Buttons include:

* (3) → +1 to counter 3
* (1,3) → +1 to counters 1,3
* (2) → +1 to counter 2
* (2,3) → +1 to counters 2,3
* (0,2) → +1 to counters 0,2
* (0,1) → +1 to counters 0,1

Minimum presses = **10**, example sequence provided.

#### Machine 2:

Minimum presses = **12**

#### Machine 3:

Minimum presses = **11**

---

## 8. Solution Outline (High Level)

For each machine:

1. Parse target vector T.
2. Convert each button into a vector of length m:

   * button j → vector b_j where b_j[i] = 1 if toggles counter i.
3. Run a **multi-dimensional BFS**:

   * State: tuple `(c0, c1, ..., cm-1)` = current counters.
   * Start at `(0,0,...,0)`.
   * Moves: For each button j:

     * New state = state + b_j
   * Prune: do not enqueue states exceeding T in any component.
4. When state == T:

   * BFS depth = minimum presses.
5. Add result to total.

Return total sum.

---

## 9. Flow Walkthrough

Example:

Machine 1 target = (3,5,4,7)
Start = (0,0,0,0)

BFS expands:

Level 1:

* All button vectors once.

Level 2:

* All sums of two button vectors.

…

Eventually reaches target after exactly 10 presses.

---

## 10. Implementation Plan (Language-Agnostic)

* Parse input lines.
* For each line:

  * Extract `{T}` vector.
  * Extract `(button)` vectors.
* BFS:

  * Use `deque`.
  * Use `visited=set` of tuples.
  * Each move cost = 1.
  * Use pruning.
* Sum answers.
* Print result.

---

## 11. Real-World Analogy + Practical Use Case

This is analogous to:

* A manufacturing process where pressing a button increments several counters.
* The goal is to reach an exact recipe with minimal operations.
* It is a bounded, monotonic integer programming / scheduling problem with non-negative constraints.
