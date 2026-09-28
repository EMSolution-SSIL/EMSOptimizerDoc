---
sidebar_position: 1
---

# Installation Guide
## Software Components
**EMSOptimizer consists of the following three components (collectively, the EMSOptimizer packages).**
- EMSOptFree
    - The publicly available source-code component. It provides EMSOptimizer CLI commands, optimization loops, and implementation examples of optimization algorithms.
- EMSOptEngine
    - The Python package used to run EMSOptFree. This package must be installed to run EMSOptFree.
- EMSOptAnalyzer
    - The Python package for shape definition and analysis in shape optimization. Install it in addition to the two packages above when performing shape optimization.

In addition, **the following related packages are required to use the shape optimization functionality of EMSOptimizer\***.
- pyemsol
    - The Python package for the EMSolution electromagnetic-field simulator engine. It is required to run EMSOptAnalyzer.
:::info
The dedicated pyemsol package is required to run EMSOptAnalyzer. It is provided together with EMSOptAnalyzer.
:::
- (Optional) eMotorSolution API
    - The eMotorSolution Python API. Install it to integrate eMotorSolution with EMSOptimizer. For integration features, see [Advanced Topics > eMotorSolution Integration](./advanced/link_ems.md).
- CodeMeter license key**

*Some functionality excluding shape optimization (such as testing optimization algorithms with benchmark functions) is available even without the related packages for shape optimization.

**Some EMSOptimizer packages and related packages are license-protected by CodeMeter and require license authentication to use.

## Installation Procedure
*A Python 3.11.x environment (where x is any minor version) and the pip package manager are required.

### Installing the Packages
1. Install the EMSOptimizer packages.
- EMSOptFree is provided as a compressed folder (`EMSOptimizer`). Extract it and place the entire folder in any location in your environment.
- EMSOptEngine and EMSOptAnalyzer are provided as wheel files. Install them with the following commands.
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
pip install emsopt_analyzer-(version)-(environment)-(os).whl
```
2. Install the related packages provided by SSIL according to their respective instructions.  

### Installing CodeMeter User Software
1. Open the CodeMeter User Software download page: https://www.wibu.com/support/user/user-software.html
2. Download the CodeMeter User Runtime for your operating system (Windows, macOS, or Linux).
3. Install CodeMeter User Runtime according to the instructions on the website.
4. **Linux only:** Download AxProtector Runtime for Linux from the CodeMeter User Software download page.
5. **Linux only:** Install AxProtector User Runtime according to the instructions on the website.
6. Restart the computer after installation is complete.

### Activating the license
1. Open the activation-page URL provided by SSIL in a browser.
2. Activate the license according to the instructions on the activation page.
3. After activation, open CodeMeter Control Center and confirm that the license is registered correctly.
