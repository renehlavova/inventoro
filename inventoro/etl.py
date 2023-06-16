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

    def __exit__(self, _exc, _exc_type, _traceback):
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

    def list_tables(self):
        """List all tables in DuckDB."""
        logger.info("Listing all tables")

        result = self.connection.sql("SELECT table_name FROM information_schema.tables")
        tables = [row[0] for row in result.fetchall()]

        logger.info("Found %s tables in DuckDB: %s", len(tables), tables)

        return tables

    def table_from_column(self, column, source_table):
        """Create a table from a json column."""
        self.connection.sql(
            f"create or replace table _json_data as select json({column}) as {column} from {source_table}"
        )

        result = self.connection.sql(f"select json_structure({column}) from _json_data").fetchone()

        if not result:
            raise RuntimeError(f"Could not get structure for {column} from {source_table}")

        structure = result[0]

        return self.connection.sql(
            (
                f"select _unnested.* from (select unnest(from_json({column}, '{structure}')) "
                "as _unnested from _json_data) tbl"
            )
        )

    def transform_warehouse_products(self):
        """Transform warehouse products."""
        logger.info("Transforming warehouse products")

        self.connection.sql("SELECT * FROM 'input_preprocessed/products.csv'").create("products")
        self.table_from_column("productOptions", "products").create("product_options")
        self.connection.sql("SELECT * FROM 'input_preprocessed/contact_supplier.csv'").create("contacts_supplier")

        # notes for ETL:
        #   - transforming only mandatory fields
        #   - warehouse product is understood as a product option from productOptions column

        query_1 = """
        SELECT 
            {  
                'id': 'test', 
                'name': 'test', 
                'parentWarehouseId': ''
            } as warehouse,
            {
                'id': TRIM(p.id),
                'name': TRIM(p.name),
                'shortcut': TRIM(p.id),
                'category': {
                    'id': TRIM(p.category),
                    'name': TRIM(p.category),
                },
                'shortDescription': TRIM(p.description), 
                'description': TRIM(p.description),
                'metaDescription': TRIM(p.description),
                'images': [],
                'properties': {
                    'productIdBySupplier': '',
                    'ean': TRIM(po.barcode),
                    'collection': '',
                    'brand': TRIM(p.brand),
                    'weight': po.optionWeight,
                    'volume': 0,
                }
            } as product,
            po.stockAvailable as availableSupply, 
            0 AS stockPrice,
            po.wholesalePrice as salePrice,
            {
                'id': TRIM(p.supplierId),
                'name': CONCAT(TRIM(cs.lastName), ' ', TRIM(cs.firstName)),
                'currency': {
                    'id': '',
                    'default': true
                }
            } as supplier,
            [] as transactions
        FROM product_options po
        LEFT JOIN products p on p.id = po.productId
        LEFT JOIN contacts_supplier cs on cs.id = p.supplierId
        """

        return self.connection.sql(query_1)
