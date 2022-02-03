import uuid

from django.db import models

from api import helper


class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False)
    board = models.TextField(default="012345678", max_length=9)
    status = models.CharField(
        max_length=7,
        choices=helper.GameEnum.choices(),
        default=helper.GameEnum.RUNNING,
    )
    player = models.CharField(
        max_length=6,
        choices=helper.PlayerEnum.choices(),
        default=helper.PlayerEnum.NOBODY,
    )

    def __str__(self):
        return f"{self.game_id} with status: {self.status}"
