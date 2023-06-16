"""Preprocesses CSV files for the Inventoro app."""

# pylint: disable=too-few-public-methods

import ast
import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CSVPreprocessor:
    """Preprocesses CSV files for the Inventoro app."""

    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

        if not self.output_path.exists():
            self.output_path.mkdir(parents=True)

        if not self.input_path.exists():
            raise ValueError(f"Input path {self.input_path} does not exist")

    def preprocess(self, filename):
        """Preprocess a CSV file."""
        with open(self.input_path / filename, "r", encoding="utf-8") as input_file, open(
            self.output_path / filename, "w", encoding="utf-8"
        ) as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            logger.info("Preprocessing %s", filename)
            for line in reader:
                writer.writerow((self._dict_to_json(value) for value in line))

    def _dict_to_json(self, string):
        """Convert a dictionary to a JSON string."""
        if not isinstance(string, str):
            return string

        try:
            value = ast.literal_eval(string)
        except (ValueError, SyntaxError):
            return string

        if isinstance(value, (dict, list)):
            return json.dumps(value)

        return string
