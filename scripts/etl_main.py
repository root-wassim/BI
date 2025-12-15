"""
Main Entry point for the Northwind ETL Pipeline
"""
import sys
import os
import logging

# Ensure special characters don't crash the script on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- IMPORTS ---
try:
    # Changed: Import the function 'run_full_extraction', not the class 'DataExtractor'
    from scripts.extract_data import run_full_extraction
    from scripts.transform_data import DataTransformer
    from scripts.load_dwh import DWLoader
except ImportError:
    from extract_data import run_full_extraction
    from transform_data import DataTransformer
    from load_dwh import DWLoader

# Logging Configuration
log_dir = os.path.join(parent_dir, 'data')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s', # Simplified format to match friend
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'etl_log.log'), mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_etl():
    print("============================================================")
    print(" STARTING ETL PIPELINE (NORTHWIND)")
    print("============================================================")
    
    try:
        # ---------------------------------------------------------
        # Étape 1: Extraction
        # ---------------------------------------------------------
        print("\n--- PHASE 1: EXTRACTION ---")
        # We call the function directly now (Friend's Style)
        success_extract = run_full_extraction()
        
        # ---------------------------------------------------------
        # Étape 2: Transformation
        # ---------------------------------------------------------
        print("\n--- PHASE 2: TRANSFORMATION ---")
        transformer = DataTransformer()
        transformer.transform_all()
        
        # ---------------------------------------------------------
        # Étape 3: Chargement
        # ---------------------------------------------------------
        print("\n--- PHASE 3: LOADING ---")
        loader = DWLoader()
        loader.load_local()
        
        print("\n============================================================")
        print(" ETL PIPELINE FINISHED SUCCESSFULLY")
        print("============================================================")
        return True
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR: {e}", exc_info=True)
        print(f"\n[FAIL] Pipeline failed. Error: {e}")
        return False

if __name__ == "__main__":
    run_etl()