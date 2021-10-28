
from Watchlist.api.serializers import WatchListSerializer, StreamOnSerializer, ReviewSerializer
from Watchlist.models import WatchList, StreamOn, Review
from rest_framework import generics, filters
from rest_framework import status
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Watchlist.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from Watchlist.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from Watchlist.api.pagination import WatchListPagination,WatchListLOPagination


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)


        #getting user information
        review_user = self.request.user
        #check user already made review regarding that movie
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviwed this movie")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1

        watchlist.save()
        serializer.save(watchlist=watchlist , review_user= review_user)
class ReviewtList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


#
# class ReviewtList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    pagination_class = WatchListLOPagination

    # permission_classes = [IsAuthenticated]

    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # filterset_fields = ['title','platform__name']
    # search_fields = ['title', 'platform__name']
    #It will show start the name with
    # search_fields = ['^title', 'platform__name']
    #the title name exact
    # search_fields = ['=title', 'platform__name']

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['avg_rating']
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request):
        if request.method == 'POST':
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

class WatchDetailAv(APIView):

    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Movie Id not found'},status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)


    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        content = {'please move along': 'nothing to see here'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)


#modelviewset
class StreamOnVs(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamOn.objects.all()
    serializer_class  = StreamOnSerializer


# viewset & routers
# class StreamOnVs(viewsets.ViewSet):
#     def list(self,request):
#         queryset = StreamOn.objects.all()
#         serializer = StreamOnSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
#     def retrieve(self,request, pk=None):
#         queryset = StreamOn.objects.all()
#         watchlist = get_object_or_404(queryset,pk=pk)
#         serializer = StreamOnSerializer(watchlist)
#         return Response(serializer.data)
#
#     def create(self):
#         serializer = StreamOnSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#     def destroy(self,request,pk):
#         movie = StreamOn.objects.get(pk=pk)
#         movie.delete()
#         content = {'please move along': 'nothing to see here'}
#         return Response(content, status=status.HTTP_404_NOT_FOUND)



class StreamOnAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        platform = StreamOn.objects.all()
        serializer = StreamOnSerializer(platform, many=True,context={'request':request})
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamOnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamOnDetailAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = StreamOn.objects.get(pk=pk)
        except StreamOn.DoesNotExist:
            return Response({'Error':'Movie Id not found'},status=status.HTTP_404_NOT_FOUND)


        serializer = StreamOnSerializer(movie, context= {'request':request})
        return Response(serializer.data)


    def put(self,request ,pk):
        movie = StreamOn.objects.get(pk=pk)
        serializer = StreamOnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self,request,pk):
        movie = StreamOn.objects.get(pk=pk)
        movie.delete()
        content = {'please move along': 'nothing to see here'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)


#
#
# @api_view(['GET','POST'])
# def Movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
# #
#
#
# @api_view(['GET','PUT','DELETE'])
# def Movie_details(request,pk):
#
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie Id not found'},status=status.HTTP_404_NOT_FOUND)
#
#         else:
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors)
#
#
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         content = {'please move along': 'nothing to see here'}
#         return Response(content, status=status.HTTP_404_NOT_FOUND)