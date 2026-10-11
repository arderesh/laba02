from collections import Counter

from streamstats.models import Event


class Statistics:
    def __init__(self):
        self.total_evs = 0
        self.level = Counter()
        self.source = Counter()
        self.err_sources = Counter()
        self.frst_timestmp = None
        self.last_timestmp = None
        self.skip_invalid = 0

    def add_event(self, event: Event):
        self.total_evs += 1
        self.level[event.level] += 1
        self.source[event.source] += 1

        if event.level in {"ERROR", "CRITICAL"}:
            self.err_sources[event.source] += 1

        if self.frst_timestmp is None:
            self.frst_timestmp = event.timestamp
        elif event.timestamp < self.frst_timestmp:
            self.frst_timestmp = event.timestamp

        if self.last_timestmp is None:
            self.last_timestmp = event.timestamp
        elif event.timestamp > self.last_timestmp:
            self.last_timestmp = event.timestamp

    def top_errors(self, lim=5):
        return sorted(self.err_sources.items(),
                      key=lambda item: (-item[1], item[0]))[:lim]


def analyze_events(events):
    statistics = Statistics()

    for event in events:
        statistics.add_event(event)

    return statistics
