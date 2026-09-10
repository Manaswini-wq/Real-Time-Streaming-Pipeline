# Real-Time Reddit Streaming Pipeline

End-to-end streaming data pipeline that ingests Reddit posts in real time,
applies NLP sentiment analysis, and loads enriched data into BigQuery
for analytics.

## Architecture

```
Reddit API ──→ Producer (Python) ──→ Pub/Sub ──→ Dataflow (Beam) ──→ BigQuery
                    │                                  │
               Sentiment NLP                  Windowing + Dedup
                (TextBlob)                   (60s fixed windows)
```

## Tech Stack

| Component       | Technology               |
|-----------------|--------------------------|
| Ingestion       | Python, PRAW (Reddit API)|
| Message Queue   | Google Cloud Pub/Sub     |
| Stream Processing | Apache Beam / Dataflow |
| Data Warehouse  | BigQuery (partitioned)   |
| NLP             | TextBlob                 |
| Infrastructure  | Terraform                |
| Containerization| Docker                   |

## Setup

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env   # fill in your credentials

# 3. Provision GCP resources
cd terraform
terraform init
terraform apply -var="project_id=your-project-id"

# 4. Create BigQuery table
python -m src.bq_schema

# 5. Start producer (Terminal 1)
python -m src.producer

# 6. Start streaming pipeline (Terminal 2)
python -m src.processor --runner DirectRunner

# Deploy to Dataflow (production)
python -m src.processor \
    --runner DataflowRunner \
    --project your-project-id \
    --region us-central1 \
    --temp_location gs://your-bucket/temp \
    --staging_location gs://your-bucket/staging

# 7. Run tests
pytest tests/
```

## Key Features

- **Exactly-once processing**: Pub/Sub + Beam deduplication by post_id
- **Windowed aggregation**: 60-second fixed windows
- **Sentiment enrichment**: Real-time NLP at ingestion
- **Partitioned storage**: BigQuery table partitioned by processing_time
- **Infrastructure as Code**: Full Terraform provisioning
- **Late data handling**: Pub/Sub retry policy with backoff
```
