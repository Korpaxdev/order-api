from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    @staticmethod
    def get(request: HttpRequest):
        return Response({'hello': 'world'})
