from datetime import date

class Event:
    def __init__(self, title=None, start=None, end=None, timeframe=None, topic=None, actor=None, target_group=None, link=None, added=None):
        self.title = title
        self.start = start
        self.end = end
        self.timeframe = timeframe
        self.topic = topic
        self.actor = actor
        self.target_group = target_group
        self.link = link
        self.added = added if added else date.today().strftime("%d.%m.%Y")

    def __repr__(self):
        return f"Event(title={self.title}, start={self.start}, end={self.end}, actor={self.actor}, link={self.link}, added={self.added})"
    
    def to_xlsx_row(self):
        return [
            self.start,
            self.end,
            self.timeframe,
            self.title,
            self.topic,
            self.actor,
            self.target_group,
            self.link,
            self.added
        ]