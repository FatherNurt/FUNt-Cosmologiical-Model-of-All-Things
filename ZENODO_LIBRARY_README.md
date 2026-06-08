# Zenodo Library Manager

Comprehensive tool to access and manage ALL records by "Nowlin, Michael K." on Zenodo.

## Features

- **Search all records** by creator name
- **List all records** with metadata (saves to CSV)
- **Download specific records** or all records at once
- **Export metadata** to JSON
- **View file details** (names, sizes)
- **Organize files** by record ID

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### List all records by author

```bash
python zenodo_library_manager.py
```

This will:
1. Search Zenodo for all records by "Nowlin, Michael K."
2. Display a summary of all records
3. Save to `zenodo_records_YYYYMMDD.csv`
4. Export full metadata to JSON

### In your Python code

```python
from zenodo_library_manager import ZenodoLibraryManager

# Initialize manager
manager = ZenodoLibraryManager(creator_name="Nowlin, Michael K.")

# Search for all records
manager.search_records()

# List records with metadata
manager.list_records(save_to_file=True)

# View files in a specific record
manager.list_record_files(record_id=12345678)

# Download a specific record
manager.download_record_files(record_id=12345678, output_dir="my_data")

# Download ALL records (⚠️ may be large!)
manager.download_all_records(base_dir="zenodo_library")

# Export all metadata
manager.export_metadata("all_metadata.json")
```

## Output Structure

When you run the manager, it creates:

```
zenodo_library/
├── record_12345678/
│   ├── file1.txt
│   ├── file2.csv
│   └── file3.pdf
├── record_87654321/
│   ├── data.xlsx
│   └── readme.md
└── ...

zenodo_records_20260608.csv      # Summary of all records
zenodo_metadata_YYYYMMDD.json    # Full metadata export
```

## Search Query

Currently configured to search for records where:
- Creator: "Nowlin, Michael K."
- Sorted by best match
- Returns all pages of results

To modify the search, edit the `search_records()` method in `zenodo_library_manager.py`.

## API Reference

- **Zenodo API Docs:** https://developers.zenodo.org/
- **Search Syntax:** https://help.zenodo.org/docs/discover/search-syntax/
