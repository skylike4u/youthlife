import openpyxl
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests  # 외부 API를 호출하기 위해 requests 라이브러리 사용
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
from io import BytesIO
from django.shortcuts import render  # 템플릿 렌더링을 위해 render 함수 사용
from .forms import SearchForm  # 폼을 불러오기 위해 SearchForm 클래스 임포트
from django.conf import settings
import environ
import time
import random

import logging
from django.http import HttpResponseServerError


# Initialize environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set up a logger instance
logger = logging.getLogger(__name__)


# 검색을 처리하고 결과를 렌더링하는 메인 뷰 함수
def search_view(request):

    try:
        # 검색 결과를 저장할 data 변수를 빈 리스트로 항상 초기화 # Initialize as an empty list, ready to store search results
        data = []
        form = SearchForm()  # Initialize the form here to ensure it always has a value

        # Load API credentials from environment variables(네이버API Key)
        client_id = env("NAVER_CLIENT_ID")
        client_secret = env("NAVER_CLIENT_SECRET")
        start = 1
        # num_loops - 원래 10개로 세팅추천(서버에서 한번에 허용/1000개 생성) / 100개하면 너무 많다(1만개 생성-)
        num_loops = 10

        if request.method == "GET" and "query" in request.GET:
            # GET 요청이며, 쿼리 파라미터가 요청에 포함된 경우
            form = SearchForm(
                request.GET
            )  # 폼 인스턴스를 생성하고 사용자의 입력값을 바인딩
            if form.is_valid():
                # 폼이 유효하다면
                query_text = form.cleaned_data[
                    "query"
                ]  # 사용자가 입력한 검색어를 가져옴

                for index in range(num_loops):
                    print(f"{index+1}번째 요청 실행 중...")
                    start_number = start + (index * 100)
                    naver_open_api = (
                        "https://openapi.naver.com/v1/search/news.json?query="
                        + query_text
                        + "&display=100&start="
                        + str(start_number)
                    )
                    header_params = {
                        "X-Naver-Client-Id": client_id,
                        "X-Naver-Client-Secret": client_secret,
                    }
                    # 외부 API 호출
                    res = requests.get(naver_open_api, headers=header_params)
                    # 응답이 성공적인 경우 (상태 코드 200)
                    if res.status_code == 200:
                        data.extend(
                            res.json().get("items", [])
                        )  # Adding items to the list
                        # JSON 응답을 파싱하여 data 변수에 저장

                    else:
                        print("Error Code: ", res.status_code)

                    print(f"{index+1}번째 요청 완료")

        # Paginate the results
        """view의 pagenator :
            Paginator 객체는 data와 페이지당 항목 수(이 경우 10)로 생성됩니다.
            'page' 변수는 쿼리 매개변수에서 추출되어 표시할 결과 페이지를 결정합니다.
            paginated_data에는 현재 페이지의 항목만 포함됩니다.
        """
        page = request.GET.get("page", 1)  # Get the page number from the request
        paginator = Paginator(data, 10)  # Show 10 results per page

        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(
                1
            )  # If page is not an integer, deliver the first page.
        except EmptyPage:
            paginated_data = paginator.page(
                paginator.num_pages
            )  # If page is out of range, deliver the last page.

        # 템플릿에 폼과 data(paginated_data)를 전달하여 렌더링
        return render(
            request, "search/news_search.html", {"form": form, "data": paginated_data}
        )
    except Exception as e:
        # Log the error and return an appropriate response
        logger.error(f"Error in search_view: {str(e)}")
        return HttpResponseServerError("Internal Server Error")


# remove_html_tags Function
def remove_html_tags(text):
    """Remove HTML tags from a string using BeautifulSoup."""
    return BeautifulSoup(text, "html.parser").get_text()


# 검색결과 엑셀파일 다운로드 Logic
def download_excel(request):
    query = request.GET.get("query", "")
    data = []
    # num_loops - 원래 10개로 세팅추천(서버에서 한번에 허용/최대 1000개 생성)
    num_loops = 10

    if query:
        # API calling logic (네이버API Key)
        client_id = env("NAVER_CLIENT_ID")
        client_secret = env("NAVER_CLIENT_SECRET")
        start, num = 1, 0
        # range 인수 - 원래 10개로 세팅해야함.(1000개 생성) 100개하면 너무 많다(1만개 생성)
        for index in range(num_loops):
            print(f"{index+1}번째 요청 실행 중...")
            start_number = start + (index * 100)
            naver_open_api = (
                "https://openapi.naver.com/v1/search/news.json?query="
                + query
                + "&display=100&start="
                + str(start_number)
            )
            header_params = {
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret,
            }
            res = requests.get(naver_open_api, headers=header_params)
            if res.status_code == 200:
                data.extend(res.json().get("items", []))  # Adding items to the list
            else:
                print("Error Code: ", res.status_code)

            print(f"{index+1}번째 요청 완료")

    # Create an in-memory Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Search Results"
    ws.column_dimensions["B"].width = 70
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 70
    ws.column_dimensions["E"].width = 60

    # Create headers
    ws.append(["num", "Title", "PubDate", "Description", "originallink"])

    # Add data to the worksheet
    for item in data:
        num += 1
        ws.append(
            [
                num,
                remove_html_tags(item.get("title")),
                item.get("pubDate"),
                remove_html_tags(item.get("description")),
                item.get("originallink"),
            ]
        )

    # Save the workbook to an in-memory buffer
    buffer = BytesIO()
    wb.save(buffer)
    wb.close()  # Ensure the workbook is closed
    buffer.seek(0)

    # Set the correct content length in the response
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=search_results.xlsx"
    response["Content-Length"] = str(len(buffer.getvalue()))

    return response
