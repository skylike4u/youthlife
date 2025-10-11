from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):

    # Django REST Framework convection(관습)인 get_object를 쓴다. (get, put, delete가 모두 해당 pk의 object가 필요하니, 중복으로 실행될 코드를 막기 위해서 만들어진 것으로 보임)
    # 해당 컨벡션은 : (detail 작업 시) 상세한 부분을 작업할 때는 항상 get_object로 객체를 가져온 뒤, get, put, delete method에서 공유될거야.
    def get_object(self, pk):
        # try/except 구문 통해 error 처리
        try:
            return Category.objects.get(pk=pk)
        # NotFound를 발생시키면 모든게 멈춰 (아래구문 모두 실행되지 않는다)
        except Category.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            # updated_category에 새로운 카테고리가 들어온다는 것
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
