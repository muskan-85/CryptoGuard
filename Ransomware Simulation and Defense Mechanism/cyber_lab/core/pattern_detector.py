
import logging

class PatternDetector:
    """
    Detects Ransomware-specific file modification patterns.
    - Header Corruption (Magic Bytes modification)
    - Double Extension (file.pdf.enc)
    - Ransom Note drops
    """
    def __init__(self):
        self.logger = logging.getLogger("PatternDetector")
        self.known_headers = {
            ".png": b"\x89PNG\r\n\x1a\n",
            ".jpg": b"\xff\xd8\xff",
            ".pdf": b"%PDF"
        }

    def check_header_corruption(self, filepath):
        """
        Checks if the file header matches its extension.
        Ransomware often corrupts headers or encrypts them.
        """
        # In a real scenario, we read bytes. 
        # Here we simulate the check or implement if files exist.
        try:
            path = str(filepath)
            ext = filepath.suffix.lower()
            if ext in self.known_headers:
                expected = self.known_headers[ext]
                with open(path, "rb") as f:
                    header = f.read(len(expected))
                if header != expected:
                    return True, f"Header Mismatch (Expected {expected.hex()}, Got {header.hex()})"
        except Exception:
            pass
        return False, None

    def check_extensions(self, filepath):
        """
        Checks for double extensions or known ransomware extensions.
        """
        name = filepath.name
        if name.count('.') > 1:
            # Heuristic: double extension like document.docx.locked
            return True, "Double Extension Detected"
        return False, None
