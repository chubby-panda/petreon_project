from rest_framework import serializers
from django.utils.translation import ugettext as _

from .models import Pet, Pledge, Category, PetImage


class CategorySerializer(serializers.Serializer):
    """
    Serializer for category model.
    """
    id = serializers.ReadOnlyField()
    category = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class PledgeSerializer(serializers.Serializer):
    """
    Serializer for pledge model.
    """
    id = serializers.ReadOnlyField()
    pet = serializers.ReadOnlyField(source='pet.id')
    amount = serializers.IntegerField()
    anonymous = serializers.BooleanField(default=False)
    supporter = serializers.ReadOnlyField(source='supporter.username')

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.anonymous = validated_data.get(
            'anonymous', instance.anonymous)
        instance.supporter = validated_data.get(
            'supporter', instance.supporter)
        instance.save()
        return instance


# class ConstrainedImageField(serializers.ImageField):
#     """
#     ImageField with additional constraints (size)
#     """
#     MAX_SIZE = 2000000  # in Bytes
#     default_error_messages = {
#         'image_size': _('The size of the image is {image_size} KB. The maximum size allowed is: {max_size} KB.'),
#     }

#     def to_internal_value(self, data):
#         super(ConstrainedImageField, self).to_internal_value(data=data)
#         file_size = data.size
#         if file_size > self.MAX_SIZE:
#             max_size_kb = self.MAX_SIZE/1000
#             file_size_kb = file_size/1000
#             self.fail('image_size', max_size=max_size_kb, image_size=file_size_kb)


class PetImageSerializer(serializers.ModelSerializer):
    """
    Serializer for pet image model (included in PetSerializer)
    """
    id = serializers.ReadOnlyField()
    pet = serializers.ReadOnlyField(source='pet.title')

    class Meta:
        model = PetImage
        fields = ('id', 'image', 'pet', 'created_at')

    def create(self, validated_data):
        print('PetImageSerializer', validated_data)
        return PetImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer for pet model (without pledges).
    """
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    pet_name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    med_treatment = serializers.CharField()
    date_created = serializers.DateTimeField(read_only=True)
    goal = serializers.IntegerField()
    pledged_amount = serializers.SerializerMethodField(default=0)
    goal_reached = serializers.BooleanField(default=False)
    active = serializers.BooleanField(default=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    pet_category = serializers.SlugRelatedField(
        slug_field='category', queryset=Category.objects.all())

    class Meta:
        model = Pet
        fields = ('id', 'title', 'pet_name', 'description', 'med_treatment', 'date_created',
                  'goal', 'pledged_amount', 'goal_reached', 'active', 'owner', 'pet_category')

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
        instance.description = validated_data.get(
            'description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.active = validated_data.get('active', instance.active)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.pet_category = validated_data.get(
            'pet_category', instance.pet_category)
        instance.save()
        return instance


class PetDetailSerializer(PetSerializer):
    """
    Serializer for pet model (with pledges).
    """
    pledges = PledgeSerializer(many=True, read_only=True)
    images = PetImageSerializer(many=True, read_only=True)
