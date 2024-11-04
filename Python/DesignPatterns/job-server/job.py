import uuid

NEW = "NEW"
PENDING = "PENDING"
INPROGRESS = "IN PROGRESS"
COMPLETE = "COMPLETE"
FAILED = "FAILED"


class Job:
    """Translation job."""

    def __init__(self, source: str, target: str, text: str):
        self.id = str(uuid.uuid1())  # GUID
        self.status = NEW  # Job status
        self.source: str = source  # Source language
        self.target: str = target  # Target language
        self.text: str = text  # Text to translate
        self.output: None | str = None  # Translated text

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "source": self.source,
            "target": self.target,
            "text": self.text,
            "output": self.output,
        }

    def __str__(self):
        return f"Job(id={self.id}, status={self.status})"

    def __repr__(self):
        return self.__str__()
