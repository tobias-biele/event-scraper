class Event:
    def __init__(self, title=None, start=None, end=None, actor=None, link=None, added=None):
        self.title = title
        self.start = start
        self.end = end
        self.actor = actor
        self.link = link
        self.added = added

    def __repr__(self):
        return f"Event(title={self.title}, start={self.start}, end={self.end}, actor={self.actor}, link={self.link}, added={self.added})"