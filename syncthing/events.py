"""
Interface to the Syncthing long polling Event API (https://docs.syncthing.net/dev/events.html)

"""

from . import BaseAPI

class Events(BaseAPI):
    prefix = '/rest/'

    def __init__(self, *args, **kwargs):
        super(Events).__init__(self, *args, **kwargs)

        self._last_seen_id = 0

    def poll(self, limit=None):
        """
        Poll the Events API for new events.

        If no new events exist the API will block until new events are available.

        :param limit: Maximum number of events to return
        :return: list of events
        """

        params = {'since': self._last_seen_id}

        if limit is not None:
            params['limit'] = limit

        data = self.get('events', params=params)
        if data:
            self._last_seen_id = data[-1]['id']

        return data

    def generate(self):
        # TODO : Consider timeout parameter?
        while True:
            for event in self.poll():
                yield event

    def __iter__(self):
        return self.generate()