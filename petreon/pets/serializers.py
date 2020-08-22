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

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.save()
        return instance
        

# This is a serializer that handles the data connected to the Pet model - we include the ID because django automatically assigns it to the model and if we want to use it in the project, we have to list it here. 
class PetSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    pet_name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    med_treatment = serializers.CharField()
    date_created = serializers.DateTimeField(read_only=True)
    goal = serializers.IntegerField()
    active = serializers.BooleanField(default=True)
    # Changed this from a CharField to ReadOnlyField so that we can pass it the username of the logged in user
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.CharField(max_length=100)

    # Added this meta class because of: https://www.django-rest-framework.org/api-guide/fields/#date-and-time-fields
    class Meta:
        model = Pet

    # This allows post method data to be added to the DB
    def create(self, validated_data):
        return Pet.objects.create(**validated_data)

    # This allows the put method data to be added to the DB
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.pet_name = validated_data.get('pet_name', instance.pet_name)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.active = validated_data.get('active', instance.active)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


# Child class of PetSerializer. This is to separate out the serializers so that we don't always get the pledges when we look up a pet.
class PetDetailSerializer(PetSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
