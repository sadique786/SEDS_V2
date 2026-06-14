from uuid import uuid4


class EventManager:

    def create_event_id(self):

        return (
            "EVT-" +
            str(uuid4())[:8]
        )
