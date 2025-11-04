# photonics_test

# Prerequisites

* **OS** : Windows 10+
* **Software** : Klayout (latest)
* **Misc** : Python3.13, Appropriate environment supplied with this project

# Installation

***pip -r requirements.txt***

All further operations are meant to be performed in the installed environment, so please run .env/Scripts/Activate.ps1 script before.

# Contents

* design/generate_clements.py - a script to generate Clements Mesh based on supplied MZI
***Usage***: python ./generate_clements.py
***Options***: in main script one can set MATRIX_SIZE, HEATER_PADDING (heater keepout area) and MZI_SPACE

* drc:
  * runsets:
    * MIN_WG_WIDTH.lydrc - drc file to check a keepout are violations
