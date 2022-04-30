from django.http import JsonResponse ,HttpResponse
from .models import Workout , Exercise , Set
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        User.objects.create_user(username = username , password = password).save()
        newuser = authenticate(username=username, password=password)
        refresh = RefreshToken.for_user(newuser)
        return JsonResponse({"refresh" : str(refresh) , 'access' : str(refresh.access_token) })
    except:
        pass

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({"refresh" : str(refresh) , 'access' : str(refresh.access_token) })
    except:
        pass

#creates new workout and returns workout list
@api_view(['POST'])
def newworkout(request):
    try:
        body = json.loads(request.body)
        description = body['description']
        wo=Workout(description=description , owner = request.user ).save()
        wol=list(Workout.objects.all().order_by('-id').values("id","date","description"))
        return JsonResponse({"workout_list":wol})
    except:
        pass

#returns list of all workouts
@api_view(['GET'])
def workouts(request):
    try:
        wol=list(Workout.objects.filter(owner = request.user ).order_by('-id').values("id","date","description"))
        return JsonResponse({"workout_list":wol})
    except:
        pass

#gets all exercises for a specific workout
@api_view(['GET'])
def workout(request, woid):
    try:
        workout = Workout.objects.get(id=woid )
        print(request.user)
        print(workout.owner)
        if workout.owner == request.user:
            exercises = list(Exercise.objects.filter(workout=workout , owner = request.user).order_by('-id').values('name','id'))
            return JsonResponse({"exercises":exercises})
    except:
        pass

#adds exercise and returns exercise list
@api_view(['POST'])
def addexercise(request,woid):
    try:
        body = json.loads(request.body)
        ex_type = body['exercise']
        wo = Workout.objects.get(id=woid)
        if wo.owner == request.user:
            exercise = Exercise(workout=wo , name=ex_type , owner = request.user ).save()
            exercise_list = list(Exercise.objects.filter(workout=wo).order_by('-id').values("id","name"))
            return JsonResponse({"exercise_list":exercise_list})
    except:
        pass

#gets all sets for a specific exercise
@api_view(['GET'])
def exercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id)
        if exercise.owner == request.user:
            sets = list(Set.objects.filter(exercise=exercise , owner = request.user).order_by('-id').values('reps','id','weight'))
            return JsonResponse({"set_list":sets,'exercise_name':exercise.name})
    except:
        pass

#creates new set and returns set list
@api_view(['POST'])
def addset(request,exercise_id):
    try:
        # creates new set and returns set list
        body = json.loads(request.body)
        set = body['set']
        reps = set['reps']
        weight = set['weight']
        exercise = Exercise.objects.get(id=exercise_id )
        if exercise.owner == request.user:
            newset = Set(exercise = exercise , reps=int(reps) , weight=int(weight) , owner = request.user ).save()
            sets = list(Set.objects.filter(exercise=exercise).values('id','reps','weight'))
            return JsonResponse({"set_list":sets})
    except:
        pass
