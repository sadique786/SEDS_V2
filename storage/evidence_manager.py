from pathlib import Path
from datetime import datetime
import json


class EvidenceManager:

    def __init__(self):

        self.base_dir = Path(
            "captures"
        )

    def create_event_directory(self):

        now = datetime.now()

        path = (
            self.base_dir /
            str(now.year) /
            f"{now.month:02d}" /
            f"{now.day:02d}"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    def save_metadata(
        self,
        event_id,
        metadata
    ):

        directory = (
            self.create_event_directory()
        )

        file_path = (
            directory /
            f"{event_id}.json"
        )

        with open(
            file_path,
            "w"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        return file_path
