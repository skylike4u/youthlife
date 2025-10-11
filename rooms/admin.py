from django.contrib import admin
from .models import Room


# admin.action은 세 개의 파라미터가 필요해 / 첫번째로 오는 것은 이 액션을 호출하는 클래스야. 두번째 것은 request 객체야, 마지막은 Queryset이다.
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        # "rating",
        "owner",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "created_at",
        "updated_at",
    )

    """ <admin의 클래스에서도 아래와 같이 쓰면 가능함(아래 예시) - 통상 models.py에 적지만>
    def total_amenities(self, room):
        return room.amenities.count()
    """

    # default로 __contains__로 검색하고, ^ 문자를 맨 앞에 쓰면, __startswith__로, 해당 키워드로 시작하는 문자를 찾는다.
    # foreign key를 사용해서 username을 검색(더블언더스코어__의 마법)
    search_fields = (
        "name",
        "^price",
        "=owner__username",
    )
