from rest_framework import serializers

from .models import Pet, Pledge, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    category = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    pet = serializers.ReadOnlyField(source='pet.id')
    amount = serializers.IntegerField()
    anonymous = serializers.BooleanField(default=False)
    supporter = serializers.ReadOnlyField(source='supporter.username')

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.save()
        return instance
        

class PetSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    pet_name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    med_treatment = serializers.CharField()
    date_created = serializers.DateTimeField(read_only=True)
    goal = serializers.IntegerField()
    pledged_amount = serializers.SerializerMethodField()
    goal_reached = serializers.BooleanField(default=False)
    active = serializers.BooleanField(default=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    pet_category = serializers.SlugRelatedField(slug_field='category', queryset=Category.objects.all())


    # Added this meta class because of: https://www.django-rest-framework.org/api-guide/fields/#date-and-time-fields
    class Meta:
        model = Pet

    def get_pledged_amount(self, obj):
        pledged = 0
        for pledge in obj.pledges.all():
            pledged += pledge.amount
        return pledged

    def get_goal_reached(self, obj):
        if obj.goal < obj.pledged_amount:
            return False
        else:
            return True

    def create(self, validated_data):
        return Pet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.pet_name = validated_data.get('pet_name', instance.pet_name)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.active = validated_data.get('active', instance.active)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.pet_category = validated_data.get('pet_category', instance.pet_category)
        instance.save()
        return instance


class PetDetailSerializer(PetSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

