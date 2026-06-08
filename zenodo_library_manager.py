"""
Script to access and download data from multiple Zenodo records
Searches for all records by creator: Nowlin, Michael K.
"""

import requests
import os
import json
import csv
from typing import List, Dict
from datetime import datetime

class ZenodoLibraryManager:
    """Manages access to multiple Zenodo records by a specific creator"""
    
    def __init__(self, creator_name="Nowlin, Michael K."):
        self.base_url = "https://zenodo.org/api"
        self.creator_name = creator_name
        self.records = []
        
    def search_records(self, page_size=50):
        """
        Search for all records by the specified creator
        
        Args:
            page_size (int): Number of results per page
            
        Returns:
            list: List of record dictionaries
        """
        all_records = []
        page = 1
        
        print(f"Searching for records by: {self.creator_name}")
        print("=" * 70)
        
        while True:
            # Query Zenodo API
            params = {
                'q': f'metadata.creators.person_or_org.name:"{self.creator_name}"',
                'size': page_size,
                'page': page,
                'sort': 'bestmatch'
            }
            
            try:
                response = requests.get(f"{self.base_url}/records", params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'hits' not in data or len(data['hits']['hits']) == 0:
                    break
                
                all_records.extend(data['hits']['hits'])
                print(f"✓ Retrieved page {page} ({len(data['hits']['hits'])} records)")
                
                # Check if there are more pages
                if len(data['hits']['hits']) < page_size:
                    break
                    
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Error fetching records: {e}")
                break
        
        self.records = all_records
        print(f"\n✓ Total records found: {len(all_records)}\n")
        return all_records
    
    def list_records(self, save_to_file=True):
        """
        List all retrieved records with metadata
        
        Args:
            save_to_file (bool): Save listing to CSV file
        """
        if not self.records:
            print("No records found. Run search_records() first.")
            return
        
        print(f"{'ID':<12} {'Title':<50} {'Year':<6} {'Type':<15}")
        print("-" * 85)
        
        for record in self.records:
            rec_id = record.get('id', 'N/A')
            title = record.get('metadata', {}).get('title', 'N/A')[:47] + "..." if len(record.get('metadata', {}).get('title', 'N/A')) > 50 else record.get('metadata', {}).get('title', 'N/A')
            created = record.get('created', 'N/A')[:4]
            rec_type = record.get('metadata', {}).get('resource_type', {}).get('type', 'N/A')[:14]
            
            print(f"{rec_id:<12} {title:<50} {created:<6} {rec_type:<15}")
        
        # Save to CSV
        if save_to_file:
            self._save_records_csv()
    
    def _save_records_csv(self):
        """Save record listing to CSV file"""
        filename = f"zenodo_records_{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['record_id', 'title', 'doi', 'created', 'type', 'url', 'num_files']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    'record_id': record.get('id', 'N/A'),
                    'title': record.get('metadata', {}).get('title', 'N/A'),
                    'doi': record.get('metadata', {}).get('doi', 'N/A'),
                    'created': record.get('created', 'N/A'),
                    'type': record.get('metadata', {}).get('resource_type', {}).get('type', 'N/A'),
                    'url': record.get('links', {}).get('html', 'N/A'),
                    'num_files': len(record.get('files', []))
                })
        
        print(f"✓ Records saved to: {filename}\n")
    
    def get_record_details(self, record_id):
        """
        Get detailed information about a specific record
        
        Args:
            record_id (int): The Zenodo record ID
            
        Returns:
            dict: Detailed record information
        """
        try:
            response = requests.get(f"{self.base_url}/records/{record_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching record {record_id}: {e}")
            return None
    
    def list_record_files(self, record_id):
        """
        List all files in a specific record
        
        Args:
            record_id (int): The Zenodo record ID
        """
        record = self.get_record_details(record_id)
        
        if not record:
            return
        
        print(f"\nRecord: {record['metadata']['title']}")
        print(f"DOI: {record['metadata'].get('doi', 'N/A')}")
        print("=" * 70)
        print(f"{'File Name':<40} {'Size (MB)':<15}")
        print("-" * 70)
        
        if 'files' in record:
            for file in record['files']:
                filename = file['key']
                size_mb = file.get('size', 0) / (1024 * 1024)
                print(f"{filename:<40} {size_mb:>10.2f} MB")
        else:
            print("No files in this record")
    
    def download_record_files(self, record_id, output_dir=None):
        """
        Download all files from a specific record
        
        Args:
            record_id (int): The Zenodo record ID
            output_dir (str): Directory to save files (defaults to record_id folder)
        """
        record = self.get_record_details(record_id)
        
        if not record:
            return
        
        if output_dir is None:
            output_dir = f"zenodo_record_{record_id}"
        
        os.makedirs(output_dir, exist_ok=True)
        
        title = record['metadata']['title']
        print(f"\nDownloading files from: {title}")
        print(f"Output directory: {output_dir}\n")
        
        if 'files' not in record or len(record['files']) == 0:
            print("No files to download")
            return
        
        for file in record['files']:
            filename = file['key']
            file_url = file['links']['self']
            save_path = os.path.join(output_dir, filename)
            
            try:
                print(f"Downloading: {filename}...", end=" ")
                response = requests.get(file_url, stream=True)
                response.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print("✓")
            except requests.exceptions.RequestException as e:
                print(f"✗ Error: {e}")
    
    def download_all_records(self, base_dir="zenodo_library"):
        """
        Download all files from all retrieved records
        
        Args:
            base_dir (str): Base directory to organize all records
        """
        if not self.records:
            print("No records found. Run search_records() first.")
            return
        
        os.makedirs(base_dir, exist_ok=True)
        
        print(f"\nDownloading all {len(self.records)} records")
        print(f"Base directory: {base_dir}\n")
        
        for idx, record in enumerate(self.records, 1):
            record_id = record['id']
            record_dir = os.path.join(base_dir, f"record_{record_id}")
            print(f"[{idx}/{len(self.records)}] ", end="")
            self.download_record_files(record_id, record_dir)
    
    def export_metadata(self, output_file=None):
        """
        Export all record metadata to JSON
        
        Args:
            output_file (str): Output filename
        """
        if not self.records:
            print("No records found. Run search_records() first.")
            return
        
        if output_file is None:
            output_file = f"zenodo_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, indent=2)
        
        print(f"✓ Metadata exported to: {output_file}\n")

def main():
    """Main execution"""
    
    # Initialize manager
    manager = ZenodoLibraryManager(creator_name="Nowlin, Michael K.")
    
    # Search for all records
    manager.search_records()
    
    # List records
    manager.list_records(save_to_file=True)
    
    # Export metadata
    manager.export_metadata()
    
    # Uncomment to download all files (large operation):
    # manager.download_all_records()
    
    # Or download specific record:
    # if manager.records:
    #     first_record_id = manager.records[0]['id']
    #     manager.list_record_files(first_record_id)
    #     manager.download_record_files(first_record_id)

if __name__ == "__main__":
    main()
