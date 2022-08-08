from ast import While
import json
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView, View
from django.http import JsonResponse
from django.core import serializers as sr
import pdb
from .serializers import *
import random
# Create your views here.

class QuizView(APIView):
    def get(self, request):
        return render(request, 'create_quiz.html')

    def post(self, request):
        quiz = Quiz(
            title = request.data.get('title'),
            category = request.data.get('category'),
            therapist_id = request.data.get('therapist_id')
        )
        if quiz.save():
            quiz_data = QuizSerializer(quiz)
            return Response(quiz_data.data)
        else:
            return Response("Error while savin g the quiz..........")


class QuestionView(APIView):
    def post(self, request):
        try:
            question = Question(
                question = request.data.get('question'),
                difficulty = request.data.get('difficulty'),
                quiz_id = request.data.get('quiz_id')
            )
            question.save()
            answers = request.data.get('answers')
            
            for ans in answers:
                answer = Answer(
                    answer = ans.get('answer'),
                    is_correct = ans.get('is_correct'),
                    question_id = question.id
                )
                answer.save()
            return JsonResponse({"Question" : "Added"}, status=200)
        except Exception as e:
            print(e)



class GetQuizList(APIView):
    def get(self, request):
        quizList = Quiz.objects.all().values("title", "id", "category")       
        return render(request, 'quiz_list.html', context={'quizes' : quizList})

class GetQuiz(APIView):
    def get(self, request, id):
        if id:
            quiz = Quiz.objects.filter(pk=id).first()
            room_codes = QuizRoom.objects.all().values("room_code")
            if quiz:
                quiz_data = QuizSerializer(quiz)
                if not request.query_params.get('room'):
                    room_code = random.randint(100000, 999999)
                    room = QuizRoom.objects.filter(event_id = request.query_params.get('event_id'), quiz_id = id).first()
                    if room:
                        room_code = room.room_code
                    else:
                        room_code = random.randint(100000, 999999)
                        while room_code in room_codes:
                            room_code = random.randint(100000, 999999)
                        room = QuizRoom.objects.create(room_code = room_code, quiz_id = quiz.id, event_id = request.query_params.get('event_id'))
                    context = {'quiz_data' : quiz_data.data, 'room_code' : room_code, 'role' : 'Therapist'}
                    return render(request, 'quiz.html', context=context)
                else:
                    room_code = request.query_params.get('room')   
                    context = {'quiz_data' : quiz_data.data, 'room_code' : room_code, 'role' : 'Client'}
                    return render(request, 'quiz.html', context=context)

            else:
                return Response("Please enter valid quiz ID......")
        else:       
            return Response("Please enter valid quiz ID......")

class GetQuestions(APIView):
    def get(self, request, quiz_id):
        if quiz_id:
            questions = Question.objects.filter(quiz_id = quiz_id)
            all_questions = QuestionSerializer(questions, many = True)
            return Response({'questions' : all_questions.data})
        else:
            return Response("Please provide valis quiz ID...")

class PerformanceView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')
        quiz_id = request.data.get('quiz_id')
        answers = request.data.get('answers')
        for answer in answers:
            question_id = answer.get('question_id')
            answer_id = answer.get('answer_id')
            if answer_id != '':
                is_correct = Answer.objects.get(pk = answer_id).is_correct
                Performance.objects.create(user_id = user_id, event_id = event_id, quiz_id = quiz_id, question_id = question_id, answer_id = answer_id, is_correct = is_correct)
            else:
                Performance.objects.create(user_id = user_id, event_id = event_id, quiz_id = quiz_id, question_id = question_id, is_correct = False)
        performance = Performance.objects.filter(quiz_id = quiz_id, user_id = user_id, event_id = event_id)
        total_questions = performance.count()
        correct_questions = performance.filter(is_correct = True).count()
        performance_data = PerformanceSerializer(performance, many = True)
        percent = (correct_questions/total_questions) * 100
        context = {"performance" : performance_data.data, "total_questions" : total_questions, "correct_questions" : correct_questions, "percent" : percent}
        return Response(context)
    
    def get(self, request, quiz_id):
        if quiz_id:
            user_id = request.data.get("User ID")
            event_id = request.data.get("Event ID")
            performance = Performance.objects.filter(quiz_id = quiz_id, user_id = user_id, event_id = event_id)
            total_questions = performance.count()
            correct_questions = performance.filter(is_correct = True).count()
            performance_data = PerformanceSerializer(performance, many = True)
            context = {"performance" : performance_data.data, "total_questions" : total_questions, "correct_questions" : correct_questions}
            return Response(context)
        else:
            return Response("Please provide valid quiz id......")
