from google.cloud import bigquery
import pandas as pd

from fishing.config import Environment


def insert_rows_to_bq(table_id: str, rows: list):
    """Stream a list of Python dictionaries into a BigQuery table.
    Each dictionary key should match a column name in the table schema.
    """
    env = Environment()
    DATASET_ID = env.bq_dataset
    full_table_id = f"{DATASET_ID}.{table_id}"

    client = bigquery.Client()
    errors = client.insert_rows_json(full_table_id, rows)

    if not errors:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows:", errors)


if __name__ == "__main__":
    df = pd.DataFrame({
        "full_name": ["John Smith", "Jane Doe"],
        "age": [50, 60]
    })
    # write_dataframe_to_bq("fishing", "your_table", df)
    insert_rows_to_bq("test_table", df.to_dict('records'))
