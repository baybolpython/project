from rest_framework import serializers
from .models import App, AppStors

class AppStorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppStors
        fields = 'name year age_stor'.split()


class AppSerializer(serializers.ModelSerializer):
    stor = AppStorsSerializer(many=False)

    class Meta:
        model = App
        fields = '__all__'
        # depth = 1


class AppValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=54, min_length=5)
    year = serializers.DateField()
    direction = serializers.CharField(required=False)
    stor = serializers.CharField()


    def validate_app_stor(self, stor):
        try:
            AppStors.objects.get(id=stor)
        except AppStors.DoesNotExist:
            raise serializers.ValidationError(f'Smart shop id {stor} not found')
        return stor