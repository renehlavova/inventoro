"""Transformation of the data for API"""

import logging

import duckdb

logger = logging.getLogger(__name__)


class ETL:
    """ETL class for Inventoro."""

    def __init__(self):
        self._connection = None

    def __enter__(self):
        """Create a DuckDB database."""
        logger.info("Creating a DuckDB database")
        self._connection = duckdb.connect()

        return self

    def __exit__(self, exc, exc_type, traceback):
        """Close the DuckDB database."""
        logger.info("Closing the DuckDB database")

        if self._connection:
            self._connection.close()

    @property
    def connection(self):
        """Get DuckDB connection."""
        if not self._connection:
            raise ValueError("Connection is not open")

        return self._connection

    def load_csv(self, filepath):
        """Load CSV file into DuckDB."""
        table_path = filepath.split(".csv")[0]
        table_name = table_path.split("/")[-1]

        logger.info(f"Loading CSV file {filepath}")

        return self.connection.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{filepath}')")

    def list_tables(self):
        """List all tables in DuckDB."""
        logger.info("Listing all tables")

        result = self.connection.execute("SELECT table_name FROM information_schema.tables")
        tables = [row[0] for row in result.fetchall()]

        logger.info(f"Found {len(tables)} tables in DuckDB: {tables}")

        return tables

    def transform_warehouse_products(self):
        """Transform warehouse products."""
        # q1 = ...
        # q2 = ...

        # queries = [q1, q2]

        # for query in queries:
        #    self.connection.exequte(query)

    def get_warehouse_products(self, table):
        """Select all warehouse products from DuckDB."""
        logger.info(f"Selecting {table}")

        return self.connection.execute(f"SELECT * FROM {table}")

    def transform_transactions(self):
        """Transform transactions."""

    def get_transactions(self):
        """Select all transactions from DuckDB."""
