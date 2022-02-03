from rest_framework import generics, status

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Game
from api.serializers import StartGameSerializer, PlayGameSerializer


class StartGameView(generics.ListCreateAPIView):
    serializer_class = StartGameSerializer
    queryset = Game.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            reverse(
                "api:game_detail",
                kwargs={"game_id": serializer.data["game_id"]},
                request=request,
            ),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class PlayGameDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "game_id"
    serializer_class = PlayGameSerializer
    queryset = Game.objects.all()
