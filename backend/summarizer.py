class Summarizer:
    def __init__(self):
        pass

    def summarize(self, text: str, max_len: int = 140):
        if not text:
            return ""
        # Simple extractive summary: first sentence or truncated prefix
        first = text.split(".")[0].strip()
        if len(first) <= max_len:
            return first + ('.' if not first.endswith('.') else '')
        truncated = first[:max_len].rsplit(' ',1)[0]
        return truncated + "..."
