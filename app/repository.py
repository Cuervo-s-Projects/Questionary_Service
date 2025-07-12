from app.models import Questionary
from config.db import mongodb
from bson import ObjectId

class Repository:

    def __init__(self):
        self.collection_questionary = mongodb['quiz']


    def create(self, Quiz):
        questionary_data = {
            '_id': Quiz._id,
            'title': Quiz.title,
            'author_id': Quiz.author_id,
            'created_at': Quiz.created_at,
            'questions': Quiz.questions,
        }
        result = self.collection_questionary.insert_one(questionary_data)
        return result
    
    def update(self,Quiz):
        questionary_data = {
            'title': Quiz.title,
            'author_id': Quiz.author_id,
            'created_at': Quiz.created_at,
            'questions': Quiz.questions,
        }
        return self.collection_questionary.update_one(
            {'_id': Quiz._id},
            {'$set': questionary_data}
        )

    def find_by_id(self, questionary_id):
        questionary_data = self.collection_questionary.find_one({'_id': ObjectId(questionary_id)})
        return Questionary.from_dict(questionary_data) if questionary_data else None
    
    def find_by_author_id(self, author_id):
        author_id_data = list(self.collection_questionary.find({}, {'author_id': author_id}))
        return author_id_data
    
    def delete(self, class_id):
        return self.collection_questionary.delete_one({'_id': ObjectId(class_id)})
