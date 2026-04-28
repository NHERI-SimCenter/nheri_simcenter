"""Setup script for the nheri_simcenter Python meta-package.

This package installs the Python runtime environment needed by the NHERI
SimCenter backend applications. Dependencies are organized into a small
core plus per-app optional extras — users install the extra that matches
their desktop application:

    pip install nheri_simcenter[pbe]       # PBE
    pip install nheri_simcenter[eeuq]      # EE-UQ
    pip install nheri_simcenter[quofem]    # quoFEM
    pip install nheri_simcenter[weuq]      # WE-UQ
    pip install nheri_simcenter[hydrouq]   # HydroUQ
    pip install nheri_simcenter[r2d]       # R2D

Users who want to run multiple apps can combine extras:

    pip install nheri_simcenter[eeuq,weuq]

"""

import io

from setuptools import find_packages, setup

import nheri_simcenter


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')


# ---------------------------------------------------------------------------
# Core: strictly the packages used by EVERY desktop app.
# ---------------------------------------------------------------------------
CORE = [
    'numpy>=1.26, <3.0',
    'scipy>=1.12',                 # upper bound inherited from pelicun (<1.16) in [pbe]/[r2d]
    'pandas>=2.2.3, <3.0',         # rewet further caps at <=2.2.3 in [r2d]
    'shapely>=2.0',                # imported directly by Workflow/whale/main.py
    'matplotlib>=3.9, <4.0',
    'scikit-learn>=1.0, <2.0',
    'plotly>=5.0',
]

# ---------------------------------------------------------------------------
# quoFEM: FEM + UQ only, no hazard events. Root of the single-asset app
# hierarchy (EE-UQ, PBE, WE-UQ, HydroUQ inherit quoFEM's FEM/UQ stack).
# ---------------------------------------------------------------------------
QUOFEM = [
    'GPy~=1.13.2',                 # hard-pinned: only release compatible with scipy<=1.12 and numpy<2; migration needed
    'emukit',                      # multi-fidelity GP in performFEM/surrogateGP
    'openseespy',                  # OpenSees-Simulation FEA backend
    'paramz',                      # directly imported by performUQ/SimCenterUQ/surrogateBuild.py
    'pydantic>=2.4, <3.0',
    'typing_extensions',
]

# ---------------------------------------------------------------------------
# EE-UQ: quoFEM's stack + earthquake events + EE-UQ Tools menu (ShakerMaker,
# DRM Mesh Generator) + Physics Based Simulation sub-dispatches (M9/Istanbul).
# ---------------------------------------------------------------------------
EEUQ = QUOFEM + [
    # EE-UQ-only SIM option — `Femora` SAM triggers a conditional femora
    # import in performSIMULATION/openSees/OpenSeesSimulation.py
    'femora',

    # Brought in by ShakerMaker + DRM Model tools and by the M9/Istanbul
    # local-dispatch chain (createEVENT/M9/M9Run.py, IstanbulRun.py)
    'geopandas>=1.0',
    'geopy',
    'h5py',                        # DRM event + DRM Model tool
    'pyproj',
    'pyvista',                     # ShakerMaker, DRM Model
    'requests',                    # M9API.py
    'tapipy',                      # ShakerMaker, M9, Istanbul (DesignSafe API)
]

# ---------------------------------------------------------------------------
# PBE: damage/loss (Pelicun) + post-earthquake performance (REDi, ATC-138).
#
# PBE diverges sharply from EE-UQ in what its UI exposes. The following EE-UQ
# entries are gated out for PBE, and their backends are no longer reachable
# from any PBE click path:
#   - Surrogate (GP) SIM widget       → drops `GPy`, `emukit`, `paramz`
#   - "None (only for surrogate)" FEM → drops the SurrogateSimulation backend
#   - Physics Based Simulations EVT   → drops the M9 / Istanbul backends
#   - DRM Event                       → drops the DRM event backend
#   - ShakerMaker Tools-menu item     → drops the ShakerMaker backend
#   - Domain Reduction Method Tools   → drops the DRM Model backend
#   - Femora SIM widget (EE-UQ-only)  → drops `femora`
# That removes (versus EE-UQ): geopandas, geopy, h5py, pyproj, pyvista,
# requests, tapipy, plus the surrogate-stack items already noted.
#
# Train GP Surrogate Model and PLoM/CustomUQ entries inside SimCenterUQ are
# also unreachable from PBE.
# ---------------------------------------------------------------------------
PBE = [
    # Still reachable via Forward-Propagation UQ (Dakota + SimCenterUQ paths
    # through performUQ/common) and via Concrete Building Model.
    'openseespy',                  # Concrete Building Model (createSAM/RCFIAP)
    'pydantic>=2.4, <3.0',         # performUQ/common
    'typing_extensions',           # performUQ/common

    # PBE-specific additions
    'atc138~=1.3',                 # Performance ATC138; forces numpy~=2.0
    'colorlover',                  # performDL/pelicun3/DL_visuals.py
    'pelicun~=3.9',                # damage and loss
    'pyredi',                      # REDi downtime
]

# ---------------------------------------------------------------------------
# WE-UQ: quoFEM's stack + wind events (CFD + experimental + TPU + stochastic)
# + BRAILS-driven CFD workflow.
# ---------------------------------------------------------------------------
WEUQ = QUOFEM + [
    'brails',                      # CFD Workflow With BRAILS event/tool
    'geopandas>=1.0',              # advancedCFDWithBRAILS + wind CFD events
    'mpi4py',                      # top-level import in createEVENT/experimentalWindPressures
    'numpy-stl',                   # IsolatedBuildingCFD, SurroundedBuildingCFD
    'pyproj',                      # advancedCFDWithBRAILS
    'trimesh',                     # advancedCFDWithBRAILS
]

# ---------------------------------------------------------------------------
# HydroUQ: quoFEM's stack + hydrodynamic events (Celeris, MPM, TaichiEvent,
# StochasticWave, GeoClawOpenFOAM) + tsunami/storm-surge EDPs.
# ---------------------------------------------------------------------------
HYDROUQ = QUOFEM + [
    'imageio',                     # Celeris, TaichiEvent
    'meshio',                      # GeoClawOpenFOAM
    'pyevtk',                      # TaichiEvent (VTK export)
    'taichi',                      # Celeris, TaichiEvent (JIT kernels)
    'welib',                       # StochasticWave
]

# ---------------------------------------------------------------------------
# R2D: regional-scale workflow. Uses rWHALE (not sWHALE).
# ---------------------------------------------------------------------------
R2D = [
    'brails',                      # BRAILS-Buildings and BRAILS-Transportation tools
    'colorlover',                  # performDL/pelicun3/DL_visuals.py
    'contextily',                  # systemPerformance/ResidualDemand
    'dask',                        # Workflow/AggregateResults.py
    'geopandas>=1.0',              # createAIM/*, performRegionalMapping/*, systemPerformance/*, tools/
    'geopy',                       # tools/ShakerMaker helpers used by R2D
    'h5py',                        # regionalGroundMotion
    'joblib',                      # regionalGroundMotion
    'JPype1',                      # jpype — regionalGroundMotion (OpenSHA / OpenQuake Java bridge)
    'momepy>=0.7',                 # createAIM/JSON_to_AIM, INP_FILE
    'mpi4py',                      # rWHALE top-level requirement
    'openquake.engine==3.17.1',    # regionalGroundMotion (pinned for compatibility with local workflow integration)
    'pandana',                     # systemPerformance/ResidualDemand, performREC
    'pelicun~=3.9',                # damage/loss via Pelicun3
    'psutil',                      # regionalGroundMotion
    'pyproj',                      # regionalGroundMotion, regionalMapping, tools
    'pyrecodes',                   # RecoveryWidgets/Pyrecodes.cpp invokes run_pyrecodes.py
    'pyvista',                     # tools
    'rasterio',                    # regionalGroundMotion, GISSpecifiedEvents
    'requests',                    # performHUA, BRAILS tools
    'rewet',                       # systemPerformance/REWET (pandas cap <=2.2.3 comes via this)
    'tapipy',                      # tools (DesignSafe API helpers)
    'tqdm',                        # regionalGroundMotion
    'ujson',                       # regionalGroundMotion
]


setup(
    name='nheri_simcenter',
    version=nheri_simcenter.__version__,
    url='http://nheri-simcenter.github.io/nheri_simcenter/',
    license='BSD License',
    author='Adam Zsarnóczay',
    author_email='adamzs@stanford.edu',
    description='NHERI SimCenter Python Dependencies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',

    python_requires='>=3.10, <3.13',

    install_requires=CORE,

    extras_require={
        'quofem': QUOFEM,
        'eeuq': EEUQ,
        'pbe': PBE,
        'weuq': WEUQ,
        'hydrouq': HYDROUQ,
        'r2d': R2D,
        # Dev/test
        'testing': ['pytest'],
    },

    tests_require=['pytest'],

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
    ],
)
