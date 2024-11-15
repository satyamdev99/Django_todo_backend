from rest_framework import serializers  # Importing serializers for API input/output handling
from .models import User  # Importing the User model

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):  
    """
    Converts User model instances into JSON format and validates input data for creating/updating users.
    """

    class Meta:
        model = User  # Specify the model the serializer is based on
        fields = ['id', 'username', 'email', 'password']  # Fields to include in the API response
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only to avoid exposure

    def create(self, validated_data):
        """
        Overrides the default creation process to hash passwords before saving.
        """
        # Create a new user instance using the validated data
        return User.objects.create(**validated_data)  
