from pyexpat import model
from random import choices
from django.db import models
from room.models import Room
from client_app.models import *

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    therapist_id = models.IntegerField()
    duration = models.IntegerField(default=10)
    # no_of_questions = models.IntegerField()
    class Meta:
        db_table = 'Quizes'
    
    def get_questions(self):
        return self.question_set.all()

    def __str__(self):
        return self.title


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
    
    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Answers'
    
    def __str__(self):
        return self.answer

class Performance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name='quiz_performances')    
    event_id = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
    quizroom = models.ForeignKey('QuizRoom', null=True, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'Performaces'

    def __str__(self):
        return str(self.client)


class QuizRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,null=True)
    event_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'QuizRoom'
    
    def __str__(self):
        return str(self.id) + " | " +str(self.room)
    
class Result(models.Model):
    room = models.ForeignKey(QuizRoom, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name='quiz_results')    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    percent = models.IntegerField()
    time_taken = models.IntegerField(null=True)
    time_over = models.BooleanField(default=False)


    class Meta:
        db_table = 'Result'
    

    def __str__(self):
        return str(self.room)
