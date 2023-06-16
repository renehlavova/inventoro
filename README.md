# inventoro

* **autor:** Renata Hlavova hlavova.renata@gmail.com
* **created:** 2023-06-15

## Description

### What it is used for

This package was prepared as part of the interview task. It sends data about warehouse products to Inventoro API.

### What the code does

The `inventoro` package:

1. preprocesses csv files to Duckdb-friendly format due to incompatible python dictionaries in the source files (seems that transforming python dict to DuckDB struct is very painful)
2. transforms warehouse products for API
3. sends warehouse products to Inventoro API
4. validates that the data were sent by retriving the first row

## Requirements

See [`pyproject.toml`](./pyproject.toml)

## How to use it

### Installation

Install this project using `poetry`.

```console
poetry install
```

### Commands

* `poe isort`
  * sort imports using `isort`
* `poe isort-check`
  * check imports are sorted using `isort`
* `poe black`
  * format Python files using `black`
* `poe black-check`
  * check Python formatting using `black`
* `poe pylint`
  * use `pylint` to lint your Python files
* `poe format`
  * run `isort` and `black` in succession
* `poe lint`
  * run `isort-check`, `black-check`, `pylint` in succession
* `poe run`
  * run the project

## My notes regarding DuckDB

1. this was my first time working with DuckDB, so the main aim was to learn the tool
2. working with DuckDB wasn't clean from my point of view, I had to make a lot of compromises while retriving and loading data from and to different formats (it may be due to my low experience though)
3.  chaining queries is one of the main advantages of DuckDB but it was very hard to stay true to SOLID principles while also taking advantage of this. the implementation suffered due to this
4.  lack of in-depth DuckDB documentation 
5.  however, the performance was good (although tried it only on small data, cannot judge performance on bigger data)
6.  the ETL process could be more detailed as I skipped non-mandatory fields
