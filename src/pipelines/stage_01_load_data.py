from src.ingestion.load_data import DataLoader

def main():

    loader = DataLoader()

    df = loader.load_raw_data()

    loader.save_interim_dataset(df)

if __name__ == "__main__":
    main()