### 1. Problem Summary

You have a circular dial numbered **0–99** (100 positions).

* It **starts at 50**.
* You apply a sequence of rotation instructions like `R5`, `L13`, etc.
* For each instruction, you rotate step-by-step in that direction, wrapping around the dial.
* You must count **every time the dial’s position is exactly 0 during the motion** of the instructions (including multiple times within a single instruction, e.g., when a large step wraps around more than once).
* At the end, you return the **total count** of these “zero hits”.

---

### 2. Domain Entities

* **Dial**

  * Circular, positions `0` to `99` inclusive.
  * Wrap-around behavior:

    * From `99` and move right→ next is `0`.
    * From `0` and move left → next is `99`.

* **Position**

  * Current integer in `[0, 99]`.
  * Initial value: `50`.

* **Instruction**

  * A pair:

    * **Direction**: `R` (right / increasing) or `L` (left / decreasing).
    * **Steps**: positive integer number of discrete moves.

* **Zero-passing / Zero-landing event**

  * Any discrete step where the dial’s position is exactly `0` while executing an instruction.

---

### 3. Inputs + Constraints

* **Input shape (assumed):**

  * A list/array of instructions, each represented as a string:

    * Format: `<Direction><Steps>`, e.g., `"R5"`, `"L120"`.
    * Direction: a single character `R` or `L`.
    * Steps: one or more digits, parsed as a non-negative integer.

* **Constraints / assumptions:**

  * Steps can be **large**, potentially greater than `100`, so an instruction may wrap around the dial multiple times.
  * There is at least one instruction (but the logic should handle an empty list gracefully).
  * No invalid directions or negative steps (if they appear, they should be treated as invalid input in an implementation).

---

### 4. Expected Outputs

* A **single non-negative integer**:

  * The **total number of times** the dial’s position is exactly `0` during the execution of all instructions in sequence.

---

### 5. Rules + Logic Requirements

1. **Starting position**

   * Before any instructions: position = `50`.

2. **Directional movement**

   * `R` (right): position increases by 1 each step:

     * `pos = (pos + 1) mod 100` repeatedly.
   * `L` (left): position decreases by 1 each step:

     * `pos = (pos - 1 + 100) mod 100` repeatedly.

3. **Step-by-step semantics**

   * Each instruction with `S` steps consists of `S` **discrete moves**.
   * After each single-step move, you have a new position.
   * During these moves, you check whether the position equals `0`.

4. **Zero counting rule**

   * You count **every single time** a step yields `position == 0`.
   * This includes:

     * Crossing from `99 → 0 → 1` (right).
     * Crossing from `1 → 0 → 99` (left).
     * Multiple wraps within one instruction (e.g., `R250` might hit `0` more than once).
   * **Design choice (assumption)**:

     * You **do not** count the initial state *before moving* an instruction, only positions reached *after* making a step.
     * If an instruction starts at `0`, you only count new steps that re-visit `0` (e.g., via full wraps).

5. **Instruction ordering**

   * Instructions are processed in the given order.
   * The ending position of one instruction is the starting position for the next.

---

### 6. Edge Cases

* **No wrap but near zero**

  * Example: starting at `1`, instruction `R2` → `1 → 2 → 3`, no `0` encountered.

* **Single wrap crossing zero once**

  * Example from your statement: starting at `98`, `R5`:
    Sequence of positions: `98 → 99 → 0 → 1 → 2 → 3`.
    Zero hits: `1`.

* **Multiple wraps in one instruction**

  * Example: starting at `10`, `R250`:

    * Total steps: `250`.
    * Every complete 100 steps, you make a full loop and hit `0` once (at the correct offset).
    * Should count **2** zero hits (`250 = 2 × 100 + 50`, position passes 0 twice).

* **Starting at zero**

  * Example: starting at `0`, `R5`:

    * Positions: `0 → 1 → 2 → 3 → 4 → 5`.
    * Zero hits: `0`, because we only count steps *into* 0, not the initial state.
  * Example: starting at `0`, `R100`:

    * You wrap once and hit zero at step `100`.
    * Zero hits: `1`.

* **Very large steps**

  * Instructions like `L1000003` must still correctly compute the number of zero hits using modular arithmetic, not by iterative stepping.

* **Empty instruction list**

  * No movement, so result should be `0`.

---

### 7. Sample Tests

1. **Simple, no zero:**

   * Input: start at 50, instructions: `["R5"]`
   * Path: `50 → 51 → 52 → 53 → 54 → 55`
   * Zero hits: `0`
   * Output: `0`

2. **One wrap hitting zero (right):**

   * Input: `["R60"]`
   * From 50: after 50 steps you reach `0`, then continue to `10`.
   * Zero hits: `1`
   * Output: `1`

3. **One wrap hitting zero (left):**

   * Input: `["L75"]`
   * From 50: moving left:

     * Eventually: `… 2 → 1 → 0 → 99 …`
   * Zero hits: `1`
   * Output: `1`

4. **Given example (R5 from 98):**

   * Start: `50`, instructions: `["R48", "R5"]`

     * First `R48`: `50 → 98` (no zero).
     * Then `R5`: `98 → 99 → 0 → 1 → 2 → 3`.
   * Zero hits: `1` (from the second instruction).
   * Output: `1`

5. **Multiple wraps in a single instruction:**

   * Input: start 10, instructions: `["R250"]`
   * First time hitting 0: after 90 steps (10 + 90 = 100).
   * Next time: 90 + 100 = 190 steps.
   * `250` steps total → hits at steps 90 and 190.
   * Zero hits: `2`
   * Output: `2`

6. **Multiple instructions, accumulating hits:**

   * Input: start 50, instructions: `["R60", "R60"]`

     * First `R60`: 1 zero hit, end at 10.
     * Second `R60`: from 10, 1 zero hit, end at 70.
   * Total zero hits: `1 + 1 = 2`
   * Output: `2`

7. **Starting at zero then wrapping:**

   * Input: start 0, instructions: `["R100", "L200"]`

     * `R100`: one full loop → hit zero once.
     * `L200`: two full loops left → hit zero twice.
   * Total zero hits: `1 + 2 = 3`
   * Output: `3`

---

### 8. Solution Outline (High Level)

1. Maintain a variable for the **current dial position**, initially `50`.
2. Maintain a counter for **zero hits**, initially `0`.
3. For each instruction:

   * Parse direction (`R` or `L`) and steps `S`.
   * Compute how many times this instruction makes the dial land on `0` during its `S` steps.
   * Add that count to the running total.
   * Update the current position to the final position of this instruction.
4. Return the total zero hit count.

Key idea:
Instead of simulating each step (which is too slow for very large steps), use **modular arithmetic** to compute how many multiples of 100 you cross at the right offset where position becomes 0.

---

### 9. Flow Walkthrough

Let’s walk through example: start `50`, instructions `["R48", "R5"]`.

1. **Initial state**

   * `pos = 50`
   * `zero_hits = 0`

2. **Instruction 1: "R48"**

   * Direction: right, steps `S = 48`.
   * From 50, moving right 48 steps goes to position `(50 + 48) mod 100 = 98`.
   * Does it hit zero?

     * From 50, you need 50 steps to reach 0 (since `50 + 50 = 100 ≡ 0 mod 100`).
     * Since `S = 48 < 50`, you **do not** reach 0 during this instruction.
   * Update:

     * `pos = 98`
     * `zero_hits = 0`

3. **Instruction 2: "R5"**

   * Direction: right, `S = 5`, starting at `pos = 98`.
   * Positions: `98, 99, 0, 1, 2, 3`.
   * The dial is at `0` once during these steps.
   * Increment `zero_hits` by `1`.
   * Final position: `(98 + 5) mod 100 = 3`.
   * Final state:

     * `pos = 3`
     * `zero_hits = 1`

4. **Result**

   * Return `zero_hits = 1`.

---

### 10. Implementation Plan (Language-Agnostic)

Use a **mathematical counting formula** per instruction instead of step-by-step simulation.

Let:

* `N = 100` (size of the dial).
* `pos` = current position at the start of an instruction (`0 ≤ pos < 100`).
* `S` = number of steps for this instruction (`S ≥ 0`).
* `direction` ∈ {`R`, `L`}.

**Per-instruction zero-hit counting:**

1. If `direction` is `R` (right):

   * We look for steps `t` (`1 ≤ t ≤ S`) such that:

     * `pos_t = (pos + t) mod N = 0`.
   * This happens when:

     * `pos + t ≡ 0 (mod N)`.
   * Let `t1` be the smallest positive `t` satisfying this:

     * If `pos = 0`, then the first time you *revisit* 0 going forward is at `t1 = N`.
     * If `pos ≠ 0`, then `t1 = N - pos`.
   * If `S < t1`, zero hits this instruction: `0`.
   * Otherwise, additional hits occur every `N` steps after `t1`:

     * Number of hits = `1 + floor((S - t1) / N)`.

2. If `direction` is `L` (left):

   * Positions: `pos_t = (pos - t) mod N`.
   * We want `pos_t = 0`:

     * `pos - t ≡ 0 (mod N)` → `t ≡ pos (mod N)`.
   * Let `t1` be the smallest positive `t` satisfying this:

     * If `pos = 0`, first revisit is again at `t1 = N`.
     * If `pos ≠ 0`, then `t1 = pos`.
   * If `S < t1`, zero hits: `0`.
   * Otherwise:

     * Number of hits = `1 + floor((S - t1) / N)`.

3. **Update the position after the instruction:**

   * If `direction = R`: `pos = (pos + S) mod N`.
   * If `direction = L`: `pos = (pos - S) mod N` (or `(pos + (N - (S mod N))) mod N`).

4. **Main loop:**

   * Initialize `pos = 50`, `zero_hits = 0`.
   * For each instruction in the list:

     * Parse `direction`, `S`.
     * Compute `hits` using the formula above.
     * Add `hits` to `zero_hits`.
     * Update `pos` accordingly.
   * After all instructions, return `zero_hits`.

This approach runs in **O(number of instructions)** time and is independent of step magnitudes.

---

### 11. Real-World Analogy + Practical Use Case

Analogy:
Think of a **clock hand** making full or partial turns around a clock face, and you want to know how many times it points at the 12 o’clock mark while following a sequence of movements. Large moves might spin the hand many times around the clock, and you want to count every time it hits exactly 12.

Practical analogues:

* Tracking how many times a **sensor or encoder** passes a reference position (`0`) on a rotating shaft in robotics or machinery.
* Counting how often a **circular buffer index** returns to the start during bulk operations.
* Analyzing movement loops in games where a player’s position wraps around a map and you care about a specific “checkpoint tile”.