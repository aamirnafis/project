import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

# Configuration class to store file paths
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")

# Main class to handle data ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion process")
        try:
            # Load the raw dataset
            df = pd.read_csv(r'C:\Users\aamir\OneDrive\Desktop\me\project\notebook\data\stud.csv')
            logging.info("Dataset loaded successfully with shape: %s", df.shape)

            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save raw data for reproducibility
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved at: %s", self.ingestion_config.raw_data_path)

            # Split the data into training and testing sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("Train-test split completed: train=%d, test=%d", len(train_set), len(test_set))

            # Save the train and test datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train data saved at: %s", self.ingestion_config.train_data_path)
            logging.info("Test data saved at: %s", self.ingestion_config.test_data_path)

            # Return paths for downstream use
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.error("Error during data ingestion: %s", str(e))
            raise CustomException(e, sys)

# ✅ Correct entry point for standalone execution
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()