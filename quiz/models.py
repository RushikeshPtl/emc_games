from random import choices
from django.db import models

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    therapist_id = models.IntegerField()
    # no_of_questions = models.IntegerField()
    class Meta:
        db_table = 'Quizes'
    
    def get_questions(self):
        return self.question_set.all()


difficulty_choices = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
)

class Question(models.Model):
    question = models.TextField()
    difficulty = models.TextField(max_length = 10, choices=difficulty_choices)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # no_of_answers = models.IntegerField()

    class Meta:
        db_table = 'Questions'
    
    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Answers'

class Performance(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'Performaces'

