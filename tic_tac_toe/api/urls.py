from django.urls import path
from . import views

app_name = "accounts_api"
urlpatterns = [
    path("v1/games/", views.StartGameView.as_view(), name="games_list"),
    path(
        "v1/games/<uuid:game_id>/",
        views.PlayGameDetailView.as_view(),
        name="game_detail",
    ),
]
