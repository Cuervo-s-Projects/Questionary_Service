from app.models import Questionary
from config.db import mongodb

class Repository:

    def __init__(self):
        self.collection = mongodb['quiz']


    def create(self, quiz):
        questionary_data = {
            '_id': quiz._id,
            'title': quiz.title,
            'author_id': quiz.author_id,
            'created_at': quiz.created_at,
            'questions': quiz.questions,
        }
        result = self.collection.insert_one(questionary_data)
        return result
    
    def update(self,quiz):
        questionary_data = {
            'title': quiz.title,
            'author_id': quiz.author_id,
            'created_at': quiz.created_at,
            'questions': quiz.questions,
        }
        return self.collection.update_one(
            {'_id': quiz._id},
            {'$set': questionary_data}
        )

    def find_by_id(self, questionary_id: str):
        questionary_data = self.collection.find_one({'_id': questionary_id})
        return Questionary.from_dict(questionary_data) if questionary_data else None
    
    def find_by_author_id(self, author_id):
        author_id_data = list(self.collection.find({}, {'author_id': author_id}))
        return author_id_data
    
    def delete(self, class_id):
        return self.collection.delete_one({'_id': class_id})