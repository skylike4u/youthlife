from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    "Room Model Definition"

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=180, default="")
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    categories = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    # 첫번째 인자는 통상 self라고 하는 데, 우리는 직관적으로 room 이라고 하자
    # 여기서 reviews는 related_name이라는 거 잊지 말아라 / foreign key로 room을 가르키는 모든 review들을 나에게 보여줌
    # room.reviews.all()은 리스트 형식의 쿼리셋임 / review.rating 각각의 리뷰의 평점들이 될 것
    # 방의 모든 리뷰를 돌면서 각 리뷰의 rating을 total_rating에 더하고 있어. 방들의 평균 점수를 반환
    # 모든 데이터를 가지고 오면 DB에 부하 심함, 쿼리셋에서 values 함수를 통해 원하는 값(rating)만 가지고 온다
    # room.reviews.all().values("rating")는 평점 5점, 3점, 5점으로 된 딕셔너리들을 가진 리스트로 형태가 바뀐다.
    """
    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
                return round(total_rating / count, 2)"""
