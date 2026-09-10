from google.cloud import bigquery
from src.utils import load_config, get_env


SCHEMA = [
    bigquery.SchemaField("post_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("subreddit", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("author", "STRING"),
    bigquery.SchemaField("score", "INTEGER"),
    bigquery.SchemaField("num_comments", "INTEGER"),
    bigquery.SchemaField("url", "STRING"),
    bigquery.SchemaField("created_utc", "TIMESTAMP"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
    bigquery.SchemaField("polarity", "FLOAT"),
    bigquery.SchemaField("subjectivity", "FLOAT"),
    bigquery.SchemaField("sentiment_label", "STRING"),
    bigquery.SchemaField("processing_time", "TIMESTAMP"),
    bigquery.SchemaField("window_start", "TIMESTAMP"),
    bigquery.SchemaField("window_end", "TIMESTAMP"),
]


def create_dataset_and_table():
    config = load_config()
    project = get_env("GCP_PROJECT_ID")
    dataset_id = config["bigquery"]["dataset"]
    table_id = config["bigquery"]["table"]

    client = bigquery.Client(project=project)

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = config["gcp"]["region"]
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset {dataset_id} ready.")

    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="processing_time",
    )
    client.create_table(table, exists_ok=True)
    print(f"Table {dataset_id}.{table_id} ready.")


if __name__ == "__main__":
    create_dataset_and_table()
