import re
import nltk
from typing import List

try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

STOPWORDS = set(stopwords.words("english"))

def preprocess_text(text: str, remove_emails: bool = True) -> str:
    if not text:
        return ""
    s = text.replace("\r"," ").replace("\n"," ").strip()
    s = re.sub(r"\s+"," ",s)

    if remove_emails:
        s = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',' ',s)

    # remove phone
    s = re.sub(r'\b(?:\+?\d{1,3}[\s-]?)?(?:\d{10}|\d{3}[\s-]\d{3}[\s-]\d{4})\b', ' ', s)
    # remove Urls
    s = re.sub(r'http\S+|www\.\S+', ' ', s)
    # Keep + and # and dots for tokens like C++ or C#
    s = re.sub(r'[^a-zA-Z0-9\+\#\.\s\/\-]',' ',s)
    #collapse extra spaces
    s = re.sub(r'\s+',' ',s).strip()
    return s.lower()

def tokenize_and_remove_stopwords(text:str) -> List[str]:
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum() or any(ch in t for ch in ['+','#'])]
    tokens = [t.lower() for t in tokens if t.lower() not in STOPWORDS and len(t) > 1]


def sentence_chunks(text: str, max_len: int = 300) -> List[str]:
    sentences = sent_tokenize(text)
    