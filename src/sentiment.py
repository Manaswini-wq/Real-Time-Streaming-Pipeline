from textblob import TextBlob


def analyze(text):
    """Returns sentiment polarity (-1 to 1) and subjectivity (0 to 1)."""
    if not text:
        return {"polarity": 0.0, "subjectivity": 0.0, "label": "neutral"}

    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 4)
    subjectivity = round(blob.sentiment.subjectivity, 4)

    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return {"polarity": polarity, "subjectivity": subjectivity, "label": label}
