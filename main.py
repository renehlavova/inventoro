"""Main entrypoint for the inventoro package"""
import json
import logging
import os
import sys

from dotenv import load_dotenv

from inventoro.api_client import APIClient
from inventoro.etl import ETL
from inventoro.preprocessing import CSVPreprocessor

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

load_dotenv()


def main():
    """Main entrypoint"""

    ### preprocess csv files due to python dict format
    preprocessor = CSVPreprocessor(input_path="./input", output_path="./input_preprocessed")

    for file in preprocessor.input_path.glob("*.csv"):
        preprocessor.preprocess(file.name)

    ### transform warehouse products
    etl = ETL()
    with etl:
        etl.transform_warehouse_products().create("warehouse_products")
        logger.info("Uploading warehouse products to json file")
        etl.connection.sql("COPY (SELECT * FROM warehouse_products) TO 'warehouse_products.json' (ARRAY TRUE)")

    ### send data to inventoro api
    api = APIClient(client_id=os.environ["CLIENT_ID"], client_secret=os.environ["SECRET"])

    with open("warehouse_products.json", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    api.post_warehouse_products(json_data)
    logger.info("Data successfully sent")

    ### check if data was sent correctly
    logger.info("Retriving first row for validation purposes")
    print(api.get_warehouse_products()[0])


if __name__ == "__main__":
    main()
