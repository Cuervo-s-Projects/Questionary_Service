from app.repository import Repository
from app.models import Questionary

class QuestionaryService:
    def __init__(self):
        self.repository = Repository()

    def create(self, id, title, author_id, questions):

        quiz = Questionary(
            _id=id,
            title=title,
            author_id=author_id,
            questions=questions
                    ) 
        
        status = self.repository.create(quiz)
        return status
    
    def get_by_id(self, quiz_id):
        quiz = self.repository.find_by_id(questionary_id=quiz_id)
        return quiz
    
    def delete_by_id(self, quiz_id):
        status = self.repository.delete(class_id=quiz_id)
        return status
