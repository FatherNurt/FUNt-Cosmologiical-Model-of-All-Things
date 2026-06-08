# FUNt-Cosmological-Model-of-All-Things

## Accessing Zenodo Data

This project accesses research data from Zenodo record [10.5281/zenodo.20594501](https://doi.org/10.5281/zenodo.20594501).

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the access script to list available files:
```bash
python zenodo_access.py
```

### Usage

**List all files in the Zenodo record:**
```python
from zenodo_access import list_files
list_files("20594501")
```

**Download a specific file:**
```python
from zenodo_access import download_file
download_file("20594501", "filename.ext")
```

**Download all files:**
```python
from zenodo_access import download_all_files
download_all_files("20594501", output_dir="data")
```

### Zenodo Record Details

- **DOI:** 10.5281/zenodo.20594501
- **Record ID:** 20594501
- **Access:** [View on Zenodo](https://zenodo.org/records/20594501)
