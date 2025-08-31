"""
Dataset Manager Service
Handles downloading and managing datasets for PhishGuard
"""

import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
import structlog
from typing import Optional, Dict, Any
import json
import zipfile

logger = structlog.get_logger()

class DatasetManager:
    """Manages datasets for PhishGuard training and testing"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.datasets = {}
        self.api = None
        
    def _authenticate_kaggle(self):
        """Authenticate with Kaggle API"""
        try:
            if self.api is None:
                self.api = KaggleApi()
                self.api.authenticate()
                logger.info("✅ Kaggle API authenticated successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Kaggle authentication failed: {e}")
            logger.info("💡 Please ensure you have kaggle.json in ~/.kaggle/ directory")
            return False
    
    async def download_spam_dataset(self) -> Optional[str]:
        """Download the spam email dataset from Kaggle"""
        try:
            logger.info("📥 Downloading spam email dataset from Kaggle...")
            
            # Authenticate with Kaggle
            if not self._authenticate_kaggle():
                return None
            
            # Download the dataset
            dataset_name = "jackksoncsie/spam-email-dataset"
            target_dir = self.data_dir / "spam_dataset"
            target_dir.mkdir(exist_ok=True)
            
            logger.info(f"📁 Downloading to: {target_dir}")
            self.api.dataset_download_files(dataset_name, path=str(target_dir), unzip=True)
            
            # Find the downloaded files
            csv_files = list(target_dir.glob("*.csv"))
            if csv_files:
                dataset_path = str(csv_files[0])
                logger.info(f"✅ Dataset downloaded successfully: {dataset_path}")
                
                # Store dataset info
                self.datasets['spam_emails'] = {
                    'path': dataset_path,
                    'type': 'spam_classification',
                    'source': 'kaggle',
                    'status': 'downloaded',
                    'file_size': Path(dataset_path).stat().st_size
                }
                
                return dataset_path
            else:
                logger.warning("No CSV files found after download")
                return None
            
        except Exception as e:
            logger.error(f"❌ Failed to download dataset: {e}")
            return None
    
    async def load_spam_dataset(self) -> Optional[pd.DataFrame]:
        """Load the spam email dataset into a pandas DataFrame"""
        try:
            if 'spam_emails' not in self.datasets:
                await self.download_spam_dataset()
            
            if 'spam_emails' not in self.datasets:
                return None
            
            dataset_path = self.datasets['spam_emails']['path']
            
            # Load the CSV file
            df = pd.read_csv(dataset_path)
            
            logger.info(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
            logger.info(f"📊 Dataset columns: {list(df.columns)}")
            
            # Store dataset info
            self.datasets['spam_emails']['dataframe'] = df
            self.datasets['spam_emails']['rows'] = len(df)
            self.datasets['spam_emails']['columns'] = list(df.columns)
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Failed to load dataset: {e}")
            return None
    
    async def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about available datasets"""
        return {
            'datasets': self.datasets,
            'data_directory': str(self.data_dir),
            'total_datasets': len(self.datasets)
        }
    
    async def save_dataset_info(self):
        """Save dataset information to a JSON file"""
        try:
            info_file = self.data_dir / "datasets_info.json"
            
            # Convert DataFrame info to serializable format
            serializable_datasets = {}
            for name, info in self.datasets.items():
                serializable_info = info.copy()
                if 'dataframe' in serializable_info:
                    del serializable_info['dataframe']  # Remove DataFrame reference
                serializable_datasets[name] = serializable_info
            
            with open(info_file, 'w') as f:
                json.dump(serializable_datasets, f, indent=2)
            
            logger.info(f"✅ Dataset info saved to {info_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save dataset info: {e}")
    
    async def cleanup_datasets(self):
        """Clean up downloaded datasets"""
        try:
            for name, info in self.datasets.items():
                if 'path' in info and Path(info['path']).exists():
                    # Remove the dataset file
                    Path(info['path']).unlink()
                    logger.info(f"🗑️ Cleaned up dataset file: {name}")
                
                # Remove the dataset directory
                dataset_dir = self.data_dir / "spam_dataset"
                if dataset_dir.exists():
                    import shutil
                    shutil.rmtree(dataset_dir)
                    logger.info(f"🗑️ Cleaned up dataset directory: {dataset_dir}")
            
            # Clear the datasets dictionary
            self.datasets.clear()
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup datasets: {e}")

# Global dataset manager instance
dataset_manager = DatasetManager()
