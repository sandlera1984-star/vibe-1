from app.sentiment import SentimentAnalyzer


def test_positive_tone():
    analyzer = SentimentAnalyzer()
    assert analyzer.tone("I feel so happy and excited today") == "positive"


def test_negative_tone():
    analyzer = SentimentAnalyzer()
    assert analyzer.tone("I am sad and worried") == "negative"


def test_neutral_when_no_keywords():
    analyzer = SentimentAnalyzer()
    assert analyzer.tone("Just a regular statement with no markers") == "neutral"
