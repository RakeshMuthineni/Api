from rest_framework import serializers
from Watchlist.models import WatchList,Review,StreamOn


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True,read_only=True)
    # len_name = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'

    # def get_len_name(self,object):
    #     length = len(object.title)
    #     return length

class StreamOnSerializer(serializers.ModelSerializer):
    # stream = serializers.HyperlinkedIdentityField(view_name='streamon-detail',lookup_field=id)


    watchlist = WatchListSerializer(many=True,read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    #watchlist = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='Movie_details'
    # )
    class Meta:
        model = StreamOn



        fields = '__all__'






# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is Too Short")
#
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name =validated_data.get('name',instance.name)
#         instance.description =validated_data.get('description',instance.description)
#         instance.active =validated_data.get('active',instance.active)
#         instance.save()
#
#         return instance
#     # def validate_name(self,value):
#     #     if len(value) <2:
#     #         raise serializers.ValidationError("Name is Too Short")
#     #     else:
#     #         return value
#
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description Should be Different")
#         else:
#             return data












