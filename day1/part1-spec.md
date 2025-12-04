### 1. Problem Summary

You have a circular dial with values **0–99** and a starting position of **50**.
You receive a list of rotation instructions like `R12` or `L3`.

For **each** instruction:

* You rotate from the **current** position by the given number of steps in the specified direction.
* You only care about the **final landing position** after that whole instruction.
* If that final position is **0**, you increment a counter.

At the end, you output how many instructions ended with the dial at **0**.

---

### 2. Domain Entities

* **Dial**: Circular range of integers `0` through `99` (100 positions).
* **Current position**: The dial value you’re currently on.
* **Instruction**: A string of form:

  * Direction: `'R'` (right/increase) or `'L'` (left/decrease)
  * Steps: a positive integer (e.g., 1, 2, 10, 123, …)
* **Zero-landing count**: Number of instructions whose **final** position is 0.

---

### 3. Inputs + Constraints

* **Input**: A sequence (list) of instruction strings: e.g. `["R1", "L2", "R50"]`.

  * `instruction[0]` is `'R'` or `'L'`.
  * `instruction[1:]` is a positive integer (no sign).
* Starting position: **50**.
* Dial size: **100** positions: `0–99`.
* Movements are applied **sequentially**:

  * The ending position of one instruction is the starting position for the next.
* Steps can be larger than 100 (multiple wraps).
* No per-step counting; we apply full rotation as a single move.

---

### 4. Expected Outputs

* **Single integer**:

  * The number of instructions whose **final position** (after applying that instruction fully) is exactly **0**.

---

### 5. Rules + Logic Requirements

1. Let `pos` be current position; initial `pos = 50`.
2. For each instruction `instr`:

   * `direction = instr[0]`
   * `amount = int(instr[1:])`
3. Compute final position in **one step**:

   * If `direction == 'R'`:

     * `pos = (pos + amount) mod 100`
   * If `direction == 'L'`:

     * `pos = (pos - amount) mod 100`
4. After updating `pos`, if `pos == 0`, increment `zero_landing_count`.
5. Continue through all instructions.
6. Return `zero_landing_count`.

**Important:** Do **not** simulate each intermediate step; only consider the final `pos` after each instruction.

---

### 6. Edge Cases

* **Large movements**: e.g. `R150` or `L1234`:

  * Must apply modulo 100 properly.
* **Exact multiples of 100**:

  * From any position, `R100` or `L100` returns to the same position.
* **Zero in steps** (if allowed, like `R0` or `L0`):

  * Position doesn’t change; only counts if you were already at 0 when applying it.
* **Already at 0**:

  * If a future instruction has `amount = 0`, that instruction counts as a landing on 0 (because final pos is 0).
  * Otherwise, move away unless steps are multiple-of-100.

---

### 7. Sample Tests

#### Test 1

**Instructions:** `["R1"]`
Start: 50

* After `R1`: `(50 + 1) % 100 = 51` → not 0

**Output:** `0`

---

#### Test 2

**Instructions:** `["R50"]`
Start: 50

* After `R50`: `(50 + 50) % 100 = 100 % 100 = 0` → counts 1

**Output:** `1`

---

#### Test 3

**Instructions:** `["R100"]`
Start: 50

* After `R100`: `(50 + 100) % 100 = 150 % 100 = 50` → not 0

**Output:** `0`

---

#### Test 4

**Instructions:** `["R50", "R50"]`
Start: 50

* After first `R50`: `(50 + 50) % 100 = 0` → count = 1
* After second `R50`: `(0 + 50) % 100 = 50` → no new landing

**Output:** `1`

---

#### Test 5

**Instructions:** `["L50"]`
Start: 50

* After `L50`: `(50 - 50) % 100 = 0` → count = 1

**Output:** `1`

---

#### Test 6

**Instructions:** `["L51"]`
Start: 50

* After `L51`: `(50 - 51) % 100 = (-1) % 100 = 99` → not 0

**Output:** `0`

---

### 8. Solution Outline (High Level)

* Maintain:

  * `pos` (current dial value),
  * `zero_count` (number of final positions that are 0).
* For each instruction:

  * Parse direction and step count.
  * Adjust `pos` using modular arithmetic.
  * If new `pos` is 0, increment `zero_count`.
* Return `zero_count` after all instructions.

---

### 9. Flow Walkthrough

Take instructions: `["R50", "L1", "R51"]`

Start: `pos = 50`, `count = 0`.

1. `R50`:

   * `pos = (50 + 50) % 100 = 0`
   * `pos == 0` → `count = 1`
2. `L1`:

   * `pos = (0 - 1) % 100 = 99`
   * Not 0 → `count = 1`
3. `R51`:

   * `pos = (99 + 51) % 100 = 150 % 100 = 50`
   * Not 0 → `count = 1`

Final result: `1` (only the first instruction landed on 0).

---

### 10. Implementation Plan (Language-Agnostic)

1. Initialize:

   * `pos ← 50`
   * `zero_count ← 0`
2. For each instruction in the list:

   * `direction ← first character of instruction`
   * `amount ← integer value of the remaining characters`
   * If `direction == 'R'`:

     * `pos ← (pos + amount) mod 100`
   * Else if `direction == 'L'`:

     * `pos ← (pos - amount) mod 100`
   * If `pos == 0`:

     * `zero_count ← zero_count + 1`
3. After the loop, output `zero_count`.

---

### 11. Real-World Analogy + Practical Use Case

This is like a **rotary encoder** or a knob with 100 discrete positions:

* The system applies commands: “turn clockwise 13,” “turn counterclockwise 42,” etc.
* You log how many times, at the **end of each command**, the knob is exactly at a reference index (position 0).

This kind of logic appears in:

* Device calibration (checking how often a device returns to a reference mark).
* Circular buffer indexing, where you want to count hits on a particular index after each operation.
