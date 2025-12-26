from rest_framework import serializers
from ..models.user import User
from bureautique.serializers.ordinateur import ProgressionUtilisateurSerializer

class ProfileUserSerializer(serializers.ModelSerializer):
    progress = ProgressionUtilisateurSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", 
                "address", "ville", "level", "email", "gender", 
                "role", "avatar", "created_at", "progress"]
        


    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request", None)

        if instance.avatar and request:
            data["avatar"] = request.build_absolute_uri(instance.avatar.url)

        return data
