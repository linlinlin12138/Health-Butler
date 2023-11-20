from django.shortcuts import get_object_or_404
from rest_framework import generics
from healthbutler.models import Foods
from healthbutler.api.serializers import FoodSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class FoodListView(generics.ListAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodSerializer

class FoodDetailView(generics.RetrieveAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodSerializer

class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        food = get_object_or_404(Foods, pk=pk)
        food.students.add(request.user)
        return Response({'enrolled': True})
