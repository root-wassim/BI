import time
import extract_data
import transform_data
import load_dwh





#root_waaim
def main():
    start_time = time.time()
    print(" STARTING NORTHWIND ETL PIPELINE")

    #  Extraction
    try:
        extract_data.extract_from_sql_server()
        extract_data.extract_from_access()
    except Exception as e:
        print(f" CRITICAL ERROR in Extraction: {e}")
        return

    #  Transformation
    try:
        transform_data.run_transformation()
    except Exception as e:
        print(f" CRITICAL ERROR in Transformation: {e}")
        return

    #  Loading
    try:
        load_dwh.load_to_warehouse()
    except Exception as e:
        print(f" CRITICAL ERROR in Loading: {e}")
        return

    

    end_time = time.time()
    duration = end_time - start_time
    print(f" ETL PIPELINE FINISHED in {duration:.2f} seconds")
if __name__ == "__main__":
    main()