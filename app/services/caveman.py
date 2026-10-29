import re

def count_tokens(text:str) -> int:
    """
    A lightweight token estimator
    Roughly approximates LLm tokenization (approx 4 characters per token on average)
    """

    if not text:
        return 0

    return max(1, len(text)//4)



def caveman_compress(raw_text:str) -> str:
    """
    Applies deterministic 'CaveMan' compression rules
    - Removes common filler words and stop words.
    - Strips all the extra whitespaces an punctuation.
    - keeps core intent keywords intact.

    """

    if not raw_text:
        return ""

    text = raw_text.lower()

    stop_words = [
        \
        "a", "an", "the", "and", "or", "but", "if", "because", "as", "what",
        \
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        \
        "do", "does", "did", "to", "from", "in", "out", "on", "off", "over",
        \
        "under", "again", "further", "then", "once", "here", "there", "when",
        \
        "where", "why", "how", "all", "any", "both", "each", "few", "more",
        \
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        \
        "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
        \
        "should", "now", "please", "kindly", "could", "would"
    ]


    words = re.findall(r'\b\w+\b')

    filtered_words = [word for word in words if word not in stop_words]

    compressed_text = " ".join(filtered_words)

    compressed_text = re.sub(r'\s+', ' ', compressed_text).strip()


    if not compressed_text:
        compressed_text= raw_text.strip()

    return compressed_text