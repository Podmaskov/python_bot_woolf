from dataclasses import asdict, dataclass, field
from datetime import datetime

@dataclass
class Contact:
    name: str
    address: str
    phone: str
    email: str
    birthday: datetime

    def to_dict(self):
        data = asdict(self)
        data['birthday'] = self.birthday.strftime("%Y-%m-%d")
        return data

    @staticmethod
    def from_dict(data):
        data['birthday'] = datetime.strptime(data['birthday'], "%Y-%m-%d")
        return Contact(**data)

@dataclass
class Note:
    content: str
    tags: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Note(**data)