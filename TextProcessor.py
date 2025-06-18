import fitz

class TextProcessor:
    def __init__(self):
        pass

    def detect_encoding(self, content: bytes):
        """Detect the encoding of text content"""
        # Try common encodings in order of likelihood
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']

        for encoding in encodings:
            try:
                content.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                continue

        return 'utf-8'  # Fallback

    def decode_content(self, file_bytes: bytes):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text

    def chunk_text(self, text, chunk_size=500, overlap=50):
        if len(text) <= chunk_size:
            return [text.strip()] if text.strip() else []

        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            # Ensure forward movement
            if end == len(text):
                break
            start = end - overlap
        return chunks
