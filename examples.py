"""
Example scripts for using the Zenodo Library Manager
"""

# Example 1: List all records and save to CSV
from zenodo_library_manager import ZenodoLibraryManager

manager = ZenodoLibraryManager(creator_name="Nowlin, Michael K.")
manager.search_records()
manager.list_records(save_to_file=True)

# Example 2: Download a specific record by ID
# Uncomment and modify record_id as needed
# manager.download_record_files(record_id=12345678, output_dir="specific_record")

# Example 3: Download all records (may take a while depending on size)
# Uncomment to enable
# manager.download_all_records(base_dir="all_zenodo_data")

# Example 4: View files in a specific record
# Uncomment and modify record_id as needed
# manager.list_record_files(record_id=12345678)

# Example 5: Export all metadata to JSON
# manager.export_metadata("nowlin_all_metadata.json")

# Example 6: Get detailed info about a single record
# record = manager.get_record_details(record_id=12345678)
# print(record)
