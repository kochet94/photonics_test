# photonics_test

# Prerequisites

* **OS** : Windows 10+
* **Software** : Klayout (latest)
* **Misc** : Python3.13, Appropriate environment supplied with this project

# Installation

***pip -r requirements.txt***

All further operations are meant to be performed in the installed environment, so please run .env/Scripts/Activate.ps1 script before.

# Highlights

---

* ***Highly configurable MZI with built-in heater and keepout zone configuration (padding)***

```python
  mzi(
      delta_l: float = 10.0,
      wg_width: float = 0.5, 
      bend_radius: float = 10.0, 
      heater_length: float = 40.0,
      padding: float = 2.0
  )
```

---

* ***Fully functional drc checks including the one for heater keep-out zone based on advanced algorithm using additional shapes generation (in order to exclude heater's waveguides themselves)***

Keepout DRC result with two violations:

<img width="1253" height="731" alt="image" src="https://github.com/user-attachments/assets/6fded9d6-de9b-4a46-a516-895e4559f08b" />

Minimum WG Space violations:

<img width="1600" height="1012" alt="image" src="https://github.com/user-attachments/assets/0cab2fd0-2a35-4641-bb9f-f04167d55935" />

Minumum WG Width violations:

<img width="1296" height="713" alt="image" src="https://github.com/user-attachments/assets/1b9717bf-4e2d-48f4-9f05-2055015aedd3" />

---

* ***Adjustable Clements Mesh generation for 4x4, 8x8, whatever x whatever mesh***

4x4 Clements Mesh:

<img width="744" height="217" alt="4x4 Clements Mesh" src="https://github.com/user-attachments/assets/b2de0ed1-3b32-4653-9e9e-80908ee08f09" />

8x8 Clements Mesh:

<img width="767" height="250" alt="image" src="https://github.com/user-attachments/assets/ee951a8e-3109-4b58-9750-6a3556bda042" />

20x20 Clements Mesh:

<img width="972" height="280" alt="image" src="https://github.com/user-attachments/assets/f9424861-d411-4621-8973-c37ec4537dde" />


# Contents

* design/generate_clements.py - a script to generate Clements Mesh based on supplied MZI

***Usage***: python generate_clements.py

***Options***: in the script one can set MATRIX_SIZE, HEATER_PADDING (heater keepout area) and MZI_SPACE

* drc/
  * runsets/
    * MIN_WG_WIDTH.lydrc - drc file to check minimum width of waveguides (≥ 0.45 μm)
    * MIN_WG_SPACE.lydrc - drc file to check minimum space between waveguides (≥ 0.6 μm)
    * KEEP_OUT_HEATER.lydrc - drc file to check a keepout area violations (no wg shapes allowed in that area)
    * MAIN_DRC.lydrc - drc master file running all checks above at once
  * qa_cells/*: contains testcases for all described drc's and their generation scripts

* lib/
  * mzi.py - pcell of MZI with built-in heater and padding
 
* tests/\*
   * tests for mzi optical ports and drc based on unittest python library

 ***Usage***: python tests.py

# Problems to solve

* Klayout does not run in batch mode on Windows machine, so test_qa_cells_drc check is incomplete but there's a comment with further logic provided
* Minimum space check does not take into account coupler where the space is reduced intentionally (light intensity splitting)... Some workaround needed.
* No grating couplers added to Clements Mesh design since lack of time...

