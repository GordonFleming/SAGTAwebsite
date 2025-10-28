from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from auth.adapter import validate_users


class CustomSuccessView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        result = validate_users()
        response_data = {
            "message": "Validation task run!",
            "members": result,
        }
        return Response(response_data, status=status.HTTP_200_OK)
