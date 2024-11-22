# Schedule simulator
#
# An entity has a daily schedule of locations where they will be.
# A higher priority event can be set for the entity, causing them to deviate
# from their predefined schedule.

from dataclasses import dataclass

@dataclass
class Event:
    name: str
    start_time_index: int
    duration: int
    priority: int


class Schedule:
    def __init__(self):
        #self._events: list[Event] = []
        self._reoccurring_events: list[Event] = []
        self._current_event: None | Event = None
    
    def add_reoccurring_event(self, event: Event):
        self._reoccurring_events.append(event)

    # def insert_additional_event(self, event: Event):

    def update(self, time_index: int):
        if self._current_event is not None:
            end_time_index = self._current_event.start_time_index + self._current_event.duration
            if time_index < end_time_index:
                return None

        # Find the next event
        

if __name__ == '__main__':

