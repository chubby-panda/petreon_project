from rest_framework import serializers

from .models import Pet, Pledge


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    pet_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    anonymous = serializers.BooleanField(default=False)
    supporter = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)
        

# This is a serializer that handles the data connected to the Pet model - we include the ID because django automatically assigns it to the model and if we want to use it in the project, we have to list it here. Now we write views...
class PetSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    pet_name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    date_created = serializers.DateTimeField(read_only=True)
    goal = serializers.IntegerField()
    active = serializers.BooleanField()
    owner = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)

    # Added this meta class because of: https://www.django-rest-framework.org/api-guide/fields/#date-and-time-fields
    class Meta:
        model = Pet

    # This allows post method data to be added to the DB
    def create(self, validated_data):
        return Pet.objects.create(**validated_data)

# This is to separate out the serializers so that we don't always get the pledges when we look up a pet
class PetDetailSerializer(PetSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
