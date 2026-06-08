"""
Script to access and download data from Zenodo record 20594501
DOI: 10.5281/zenodo.20594501
"""

import requests
import os
import json

def get_zenodo_record(record_id):
    """
    Fetch metadata and files from a Zenodo record
    
    Args:
        record_id (str): The Zenodo record ID
        
    Returns:
        dict: JSON response containing record metadata and file links
    """
    url = f"https://zenodo.org/api/records/{record_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching record: {e}")
        return None

def list_files(record_id):
    """
    List all files available in a Zenodo record
    
    Args:
        record_id (str): The Zenodo record ID
    """
    data = get_zenodo_record(record_id)
    
    if not data:
        return
    
    print(f"\nRecord Title: {data.get('title', 'N/A')}")
    print(f"Record DOI: {data.get('doi', 'N/A')}")
    print(f"Created: {data.get('created', 'N/A')}")
    print("\n" + "="*60)
    print("Files in this record:")
    print("="*60)
    
    if 'files' in data:
        for idx, file in enumerate(data['files'], 1):
            print(f"\n{idx}. {file['key']}")
            print(f"   Size: {file.get('size', 'N/A')} bytes")
            print(f"   Download URL: {file['links']['self']}")
    else:
        print("No files found in this record")

def download_file(record_id, filename, output_path=None):
    """
    Download a specific file from a Zenodo record
    
    Args:
        record_id (str): The Zenodo record ID
        filename (str): The name of the file to download
        output_path (str): Optional path to save the file (defaults to current directory)
    """
    data = get_zenodo_record(record_id)
    
    if not data or 'files' not in data:
        print("Record not found or has no files")
        return False
    
    # Find the file
    file_data = None
    for file in data['files']:
        if file['key'] == filename:
            file_data = file
            break
    
    if not file_data:
        print(f"File '{filename}' not found in record")
        return False
    
    # Download the file
    file_url = file_data['links']['self']
    save_path = output_path or filename
    
    try:
        print(f"Downloading {filename}...")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Successfully downloaded to {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

def download_all_files(record_id, output_dir="zenodo_data"):
    """
    Download all files from a Zenodo record
    
    Args:
        record_id (str): The Zenodo record ID
        output_dir (str): Directory to save files (creates if doesn't exist)
    """
    data = get_zenodo_record(record_id)
    
    if not data or 'files' not in data:
        print("Record not found or has no files")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Downloading all files to '{output_dir}'...\n")
    
    for file in data['files']:
        filename = file['key']
        save_path = os.path.join(output_dir, filename)
        download_file(record_id, filename, save_path)

if __name__ == "__main__":
    # Zenodo record ID for DOI 10.5281/zenodo.20594501
    RECORD_ID = "20594501"
    
    # List all available files
    list_files(RECORD_ID)
    
    # Uncomment below to download specific file:
    # download_file(RECORD_ID, "filename_here.ext", "path/to/save")
    
    # Uncomment below to download all files:
    # download_all_files(RECORD_ID)
