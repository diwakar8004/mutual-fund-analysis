import os
import glob
import pandas as pd

RAW_FOLDER = "data/raw"

print("--- Data Profiling Tool ---\n")

# 1. Find all CSV files in our data/raw folder
csv_files = glob.glob(os.path.join(RAW_FOLDER, "*.csv"))

if not csv_files:
    print("No CSV files found yet. Make sure your local 10 CSVs or API CSVs are inside data/raw/")
else:
    # 2. Read and analyze each file one by one
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"==========================================")
        print(f"ANALYZING FILE: {file_name}")
        print(f"==========================================")
        
        try:
            # Load the file into memory using Pandas
            df = pd.read_csv(file_path)
            
            # Print basic structural stats
            print(f"• Total Rows (Rows, Columns): {df.shape}")
            print("\n• Data Columns and Types:")
            print(df.dtypes)
            
            print("\n• First 3 sample rows:")
            print(df.head(3))
            print("\n")
            
        except Exception as e:
            print(f"Could not read {file_name}. Error: {e}\n")