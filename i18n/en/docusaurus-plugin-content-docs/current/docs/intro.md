---
sidebar_position: 1
---

# Installation Guide
## Software Components
**EMSOptimizer consists of the following three plus one components (collectively, the EMSOptimizer packages).**
- EMSOptFree
    - The publicly available source-code component. It provides EMSOptimizer CLI commands, optimization loops, and implementation examples of optimization algorithms. It is available on the [GitHub page](https://github.com/EMSolution-SSIL/EMSOptimizer).
- EMSOptEngine
    - The Python package used to run EMSOptFree. This package must be installed to run EMSOptFree. It can be downloaded from Releases on the [GitHub page](https://github.com/EMSolution-SSIL/EMSOptimizer).
- EMSOptAnalyzer
    - The Python package for shape definition and analysis in shape optimization. Install it in addition to the two packages above when performing shape optimization.
- pylevelset_reinit
    - The Python package used to reinitialize level set functions. It is provided together with EMSOptAnalyzer.

In addition, **the following related packages are required to use the shape optimization functionality of EMSOptimizer\***.
- pyemsol
    - The Python package for the EMSolution electromagnetic-field simulator engine. It is required to run EMSOptAnalyzer.
:::info
The dedicated pyemsol package is required to run EMSOptAnalyzer. It is provided together with EMSOptAnalyzer.
:::
- (Optional) eMachineSim
    - The eMachineSim tool for peripheral analysis of electrical equipment. It is required together with pyemsol when performing peripheral analyses such as stress analysis during optimization.
- (Optional) eMotorSolution API
    - The Python API for eMotorSolution (SSIL's motor simulation tool). Install it to integrate eMotorSolution with EMSOptimizer. See [Advanced Topics > Integration with eMotorSolution](./advanced/link_ems.md) for details.
- CodeMeter license key**

*Some functionality excluding shape optimization (such as testing optimization algorithms with benchmark functions) is available even without the related packages for shape optimization.

**Some EMSOptimizer and related packages are license-protected by CodeMeter and require license activation.**

## Installation Procedure
*A Python 3.11.x environment (where x is any minor version) and the pip package manager are required.

### Installing the Packages
1. Install the EMSOptimizer packages.
- EMSOptFree is provided as a compressed folder (`EMSOptimizer`). Extract it and place the entire folder in any location in your environment.
- EMSOptEngine and EMSOptAnalyzer are provided as wheel files. Install them with the following commands.
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
pip install emsopt_analyzer-(version)-(environment)-(os).whl
pip install pylevelset_reinit-(version)-(environment)-(os).whl
```
:::info
Starting with v0.7.0, EMSOptFree can also be installed from a wheel file. It can also be downloaded from Releases on the [GitHub page](https://github.com/EMSolution-SSIL/EMSOptimizer).  
Installing the wheel allows CLI commands to be run from anywhere within the Python environment.  
However, if you frequently customize optimization methods, installing it as a compressed folder as before is recommended.
:::
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
