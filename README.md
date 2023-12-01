<div align="center">
  <h1 align="center">
    Badger: The Missing Optimizer in ACR
    <br />
    <a href="https://slac-ml.github.io/Badger">
      <img src="pics/badger.png" alt="Badger" height=128>
    </a>
  </h1>
</div>

![Badger main GUI](pics/main.png)

| Documentation | Package | Downloads | Version | Platforms |
| --- | --- | --- | --- | --- |
| [![Documentation](https://img.shields.io/badge/Badger-documentation-blue.svg)](https://slac-ml.github.io/Badger/) | [![Conda Recipe](https://img.shields.io/badge/recipe-badger-opt.svg)](https://anaconda.org/conda-forge/badger-opt) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/badger-opt.svg)](https://anaconda.org/conda-forge/badger-opt) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/badger-opt.svg)](https://anaconda.org/conda-forge/badger-opt) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/badger-opt.svg)](https://anaconda.org/conda-forge/badger-opt) |


## Installation

Using `conda`

```shell
conda install -c conda-forge badger-opt
```

or `pip`

```shell
pip install badger-opt
```

### Run an optimization

Once Badger is installed, launch the GUI by running the following command in the terminal:

```bash
badger -g
```

Then following [this simple GUI tutorial](https://slac-ml.github.io/Badger/docs/next/getting-started/tutorial_0) to run your first optimizaion in Badger within a couple of minutes!

### Citation

If you use Badger for your research, please consider adding the following citation to your publications.

```
Zhang, Z., et al. "Badger: The missing optimizer in ACR",
in Proc. IPAC'22, Bangkok. doi:10.18429/JACoW-IPAC2022-TUPOST058
```

BibTex entry:
```bibtex
@inproceedings{Badger,
    author       = {Z. Zhang and M. Böse and A.L. Edelen and J.R. Garrahan and Y. Hidaka and C.E. Mayes and S.A. Miskovich and D.F. Ratner and R.J. Roussel and J. Shtalenkova and S. Tomin and G.M. Wang},
    title        = {{Badger: The Missing Optimizer in ACR}},
    booktitle    = {Proc. IPAC'22},
    pages        = {999--1002},
    eid          = {TUPOST058},
    language     = {english},
    keywords     = {interface, controls, GUI, operation, framework},
    venue        = {Bangkok, Thailand},
    series       = {International Particle Accelerator Conference},
    number       = {13},
    publisher    = {JACoW Publishing, Geneva, Switzerland},
    month        = {07},
    year         = {2022},
    issn         = {2673-5490},
    isbn         = {978-3-95450-227-1},
    doi          = {10.18429/JACoW-IPAC2022-TUPOST058},
    url          = {https://jacow.org/ipac2022/papers/tupost058.pdf},
}
```
