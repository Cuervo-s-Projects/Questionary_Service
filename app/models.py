from datetime import datetime
from bson import ObjectId
from typing import List, Dict

class Questionary:
    def __init__(
        self,
        _id: ObjectId = None,
        title: str=None,
        author_id: str = None,
        created_at: datetime = None,
        questions: List[Dict] = None,
    ):
        self._id = ObjectId(_id) or ObjectId()
        self.title = title
        self.author_id = ObjectId(author_id)
        self.created_at = created_at or datetime.now()
        self.questions = questions or []

    def to_dict(self):
        return {
            '_id': self._id,
            'title': self.title,
            'author_id': self.author_id,
            'created_at': self.created_at,
            'questions': self.questions,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get('_id', None),
            title=data.get('title',''),
            author_id=data.get('author_id',''),
            created_at=data.get('created_at',''),
            questions=data.get('questions', []),
        )