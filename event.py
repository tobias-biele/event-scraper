from datetime import date

class Event:
    def __init__(self, title=None, start=None, end=None, timeframe=None, topic=None, actor=None, location=None, target_group=None, link=None, added=None, description=None):
        self.title = title
        self.start = start
        self.end = end
        self.timeframe = timeframe
        self.topic = topic
        self.actor = actor
        self.location = location
        self.target_group = target_group
        self.link = link
        self.added = added if added else date.today().strftime("%d.%m.%Y")
        self.description = description

    def __repr__(self):
        return f"Event(title={self.title}, start={self.start}, end={self.end}, timeframe={self.timeframe}, actor={self.actor}, location={self.location}, link={self.link}, added={self.added})"
    
    def to_xlsx_row(self):
        return [
            self.start,
            self.end,
            self.timeframe,
            self.title,
            self.topic,
            self.actor,
            self.location,
            self.target_group,
            self.link,
            self.added,
            self.description
        ]