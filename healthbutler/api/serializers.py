from rest_framework import serializers
from healthbutler.models import Foods
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ['id', 'name', 'calories']