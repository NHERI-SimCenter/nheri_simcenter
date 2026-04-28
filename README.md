<p align="center">
	<b>NHERI SimCenter Python Dependencies</b>
</p>

<p align="center">
	<a href="https://pypi.org/project/nheri-simcenter/"><img src="https://img.shields.io/pypi/v/nheri-simcenter.svg" alt="PyPI"></a>
	<a href="https://pypi.org/project/nheri-simcenter/"><img src="https://img.shields.io/pypi/pyversions/nheri-simcenter.svg" alt="Python versions"></a>
	<a href="LICENSE"><img src="https://img.shields.io/pypi/l/nheri-simcenter.svg" alt="License"></a>
</p>

`nheri_simcenter` is a Python meta-package that installs the third-party
Python libraries needed by the [NHERI SimCenter](https://simcenter.designsafe-ci.org/)
desktop applications. It contains no application code itself — its sole
purpose is to declare the dependency stack for each desktop app and let
pip resolve it.


## Installation

When installing this package, choose the extra that matches the desktop app 
you use:

```bash
pip install nheri_simcenter[quofem]      # quoFEM   — UQ on a user-supplied numerical model
pip install nheri_simcenter[eeuq]        # EE-UQ    — earthquake response analysis
pip install nheri_simcenter[pbe]         # PBE      — performance-based engineering
pip install nheri_simcenter[weuq]        # WE-UQ    — wind response analysis
pip install nheri_simcenter[hydrouq]     # HydroUQ  — hydrodynamic events
pip install nheri_simcenter[r2d]         # R2DTool  — regional resilience workflows
```

A bare `pip install nheri_simcenter` installs only a small core
(`numpy`, `scipy`, `pandas`, `shapely`, `matplotlib`, `scikit-learn`,
`plotly`) — every SimCenter app needs more than this, so always pass
the matching extra.

If you use multiple SimCenter apps in the same environment, combine
extras:

```bash
pip install nheri_simcenter[eeuq,weuq]
```

### Why no `[all]` extra?

A single environment that covers every SimCenter app is currently
unresolvable. The `[all]` extra will be introduced in a future update.

## Python version

`nheri_simcenter` supports Python **3.10, 3.11, and 3.12**. Use a
clean virtual environment to avoid resolver conflicts with other packages.


## What this package does NOT install

- **C++ libraries** (Qt, OpenSees, HDF5 native libs, etc.) — managed
  by each desktop app's own installer / Conan configuration.


## License

`nheri_simcenter` is distributed under the BSD 3-Clause license. See
[LICENSE](LICENSE) for the full text.

## Acknowledgement

This material is based upon work supported by the National Science
Foundation under Grants No. 1612843 and 2131111. Any opinions, findings, and
conclusions or recommendations expressed in this material are those of
the authors and do not necessarily reflect the views of the National
Science Foundation.

## Contact

Adam Zsarnóczay, NHERI SimCenter, Stanford University —
[adamzs@stanford.edu](mailto:adamzs@stanford.edu)
</content>
</invoke>