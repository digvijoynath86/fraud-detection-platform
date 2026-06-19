from src.profiling.data_profiler import DataProfiler
import pandas as pd

def main():

    df = pd.read_parquet(
        "data/interim/merged_dataset.parquet"
    )

    profiler = DataProfiler(df)

    profiler.generate_reports()

if __name__ == "__main__":
    main()