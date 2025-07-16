from datetime import datetime
from typing import List, Dict
from mongoengine import Document as MongoDocument, StringField, DateTimeField, ListField
import uuid

class Questionary:
    def __init__(
        self,
        _id: str = None,
        title: str=None,
        author_id: str = None,
        created_at: datetime = None,
        questions: List[Dict] = None,
    ):
        self._id = _id or str(uuid.uuid4())
        self.title = title
        self.author_id = author_id or ""
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

class Document(MongoDocument):
    title = StringField(required=True)
    description = StringField(default="")
    tags = ListField(StringField(max_length=50), default=list)
    upload_date = DateTimeField(default=datetime.utcnow)
    filename = StringField(required=True)
    content_type = StringField(required=True)
    file_size = StringField(required=True)
    user_id = StringField(required=True)
    file_id = StringField(required=True)
    pages = StringField(default="1")

    meta = {
        'collection': 'documents'
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'upload_date': self.upload_date.isoformat(),
            'filename': self.filename,
            'content_type': self.content_type,
            'file_size': self.file_size,
            'user_id': self.user_id,
            'file_id': self.file_id,
            'pages': self.pages
        }

    def __str__(self):
        return f"{self.title} ({self.filename})"