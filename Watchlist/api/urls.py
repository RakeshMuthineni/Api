from django.urls import path,include
from Watchlist.api.views import (WatchListGV,StreamOnVs,WatchListAV,UserReview,WatchDetailAv,StreamOnAv,StreamOnDetailAv,ReviewtList,ReviewDetail,ReviewCreate)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamOnVs, basename= 'streamon')


urlpatterns =[

    path('list/',WatchListAV.as_view(),name='Movie_list'),
    path('<int:pk>',WatchDetailAv.as_view(),name='Movie_details'),
    path('list2/',WatchListGV.as_view(),name='watch_list'),

    path('',include(router.urls)),

    # path('stream/',StreamOnAv.as_view(),name='stream'),
    # path('stream/<int:pk>',StreamOnDetailAv.as_view(),name='stream_details'),

    # path('review/',ReviewtList.as_view(),name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name= 'review-detail'),
    # path('stream/<int:pk>/review', ReviewtList.as_view(), name='review-list'),

    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/reviews/',ReviewtList.as_view(),name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name= 'review-detail'),
    path('reviews/',UserReview.as_view(),name= 'user-review-detail'),


]