from django.urls import path
from .views import MatchListView, MatchDetailView, MatchCreateView, \
BatchFixturesCreateView, PublishBetRequestView, RequestCreateView,RequestPatchView, OddsByMatchView, PastMatchCreateView,\
BatchPastFixturesCreateView, RequestUserRelationCreateView, UserRequestsList, PastMatchListView, ProtectedView

urlpatterns = [
    path('fixtures/', MatchListView.as_view(), name='match-list'),
    path('fixtures/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('fixtures/create/', MatchCreateView.as_view(), name='match-create'),
    path('fixtures/create/batch/', BatchFixturesCreateView.as_view(), name='fixtures-create-batch'),
    # path('fixtures/<int:match_id>/place-bond/', PlaceBondView.as_view(), name='place-bond'),
    path('publish/', PublishBetRequestView.as_view(), name='publish-bet-request'),
    path('requests/create/', RequestCreateView.as_view(), name='requests-create'),
    path('requests/validation/<str:request_id>/', RequestPatchView.as_view(), name='requests-validation'),
    path('odds/<int:match_id>/', OddsByMatchView.as_view(), name='odds-by-match'),
    path('fixtures/history/', PastMatchListView.as_view(), name='match-history'),
    path('fixtures/history/create', PastMatchCreateView.as_view(), name='match-history-create'),
    path('fixtures/history/create/batch', BatchPastFixturesCreateView.as_view(), name='match-history-create-batch'),
    path('request/create/relation/', RequestUserRelationCreateView.as_view(), name='request-relation-create'),
    path('requests/<str:user_email>/', UserRequestsList.as_view(), name='user-requests-list'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),
]