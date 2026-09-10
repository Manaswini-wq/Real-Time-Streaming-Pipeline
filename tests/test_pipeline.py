import json
import pytest
from src.sentiment import analyze
from src.producer import post_to_message
from unittest.mock import MagicMock


def test_positive_sentiment():
    result = analyze("This is an amazing and wonderful project!")
    assert result["label"] == "positive"
    assert result["polarity"] > 0


def test_negative_sentiment():
    result = analyze("This is terrible and broken.")
    assert result["label"] == "negative"
    assert result["polarity"] < 0


def test_neutral_sentiment():
    result = analyze("The meeting is at 3pm.")
    assert result["label"] == "neutral"


def test_empty_text():
    result = analyze("")
    assert result["label"] == "neutral"
    assert result["polarity"] == 0.0


def test_post_to_message():
    mock_post = MagicMock()
    mock_post.id = "abc123"
    mock_post.subreddit = "technology"
    mock_post.title = "Python is great for data engineering"
    mock_post.author = "testuser"
    mock_post.score = 42
    mock_post.num_comments = 10
    mock_post.url = "https://example.com"
    mock_post.created_utc = 1700000000.0

    msg = post_to_message(mock_post)

    assert msg["post_id"] == "abc123"
    assert msg["subreddit"] == "technology"
    assert msg["score"] == 42
    assert msg["sentiment_label"] in ("positive", "negative", "neutral")
    assert "ingested_at" in msg
    assert "polarity" in msg
