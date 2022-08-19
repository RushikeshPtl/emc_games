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
from room.models import Room
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
        quiz.save()
        if request.data.get('duration'):
            quiz.duration = request.data.get('duration')
        quiz_data = QuizSerializer(quiz)
        return Response(quiz_data.data)


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

class GetRoom(APIView):
    def get(self, request, id):
        if id:
            room_codes = Room.objects.all().values("room_code")
            quiz = Quiz.objects.get(pk=id)
            therapist_id = random.randint(100000, 999999)
            client_id = random.randint(100000, 999999)
            if quiz:
                if not request.query_params.get('room'):
                    quizroom = QuizRoom.objects.filter(event_id = request.query_params.get('event_id'), quiz_id = id).first()
                    if quizroom:
                        room_code = quizroom.room.room_code
                    else:
                        room_code = random.randint(100000, 999999)
                        while room_code in room_codes:
                            room_code = random.randint(100000, 999999)
                        rm = Room.objects.create(room_code = room_code, therapist_id = therapist_id, client_id = client_id)
                        room = QuizRoom.objects.create(room_id = rm.id, quiz_id = id, event_id = request.query_params.get('event_id'))
                    context = {'room_code' : room_code, 'role' : 'Therapist', 'quiz_id' : quiz.id, 'quiz_title' : quiz.title, 'quiz_category' : quiz.category}
                    return render(request, 'quiz.html', context=context)
                else:
                    room_code = request.query_params.get('room')
                    context = {'room_code' : room_code, 'role' : 'Client', 'quiz_id' : quiz.id, 'quiz_title' : quiz.title, 'quiz_category' : quiz.category}
                    return render(request, 'quiz.html', context=context)
            else:
                return Response("Quiz Not Found......")
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
        room_code = request.data.get('room_code')
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
        correct_answers = performance.filter(is_correct = True).count()
        performance_data = PerformanceSerializer(performance, many = True)
        percent = (correct_answers/total_questions) * 100
        room = Room.objects.filter(room_code=room_code).first()
        quizroom_id = QuizRoom.objects.get(room_id=room.id).id
        result = Result(
            room_id = quizroom_id,
            user_id = user_id,
            quiz_id = quiz_id,
            correct_answers = correct_answers,
            wrong_answers = total_questions - correct_answers,
            percent = percent
        )
        result.save()
        result_data = ResultSerializer(result)
        context = {"performance" : performance_data.data, "total_questions" : total_questions, "correct_questions" : correct_answers, "percent" : percent, "result" : result_data.data}
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
