from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

from auth.adapter import validate_users

def index(request):
    result = validate_users()
    # You can use the result in your response
    response_data = {
        "message": "Validation task run!",
        "result_from_otherapp": result,
    }

    return JsonResponse(response_data)