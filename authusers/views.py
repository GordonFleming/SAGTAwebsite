# from django.shortcuts import render
# from django.http import JsonResponse
# from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.adapter import validate_users

# def index(request):
#     result = validate_users()
#     # You can use the result in your response
#     response_data = {
#         "message": "Validation task run!",
#         "members_now_activated": result,
#         "count": len(result),
#     }

#     return JsonResponse(response_data)

class CustomSuccessView(APIView):
    def get(self, request):
        result = validate_users()
        # You can use the result in your response
        response_data = {
            "message": "Validation task run!",
            "members": result,
        }
        return Response(response_data, status=status.HTTP_200_OK)
