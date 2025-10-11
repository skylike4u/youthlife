# 네이버 뉴스검색API : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4

import requests
import openpyxl

client_id = "Csp2vloqx3TeASk6jMHs"
client_secret = "rLyfSKx9Oa"
start, num = 1, 0

excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.column_dimensions["B"].width = 100
excel_sheet.column_dimensions["C"].width = 70
excel_sheet.column_dimensions["D"].width = 70
excel_sheet.column_dimensions["E"].width = 40
excel_sheet.append(
    ["순번", "제목", "원문링크", "네이버링크", "보도일시"]
)  # 맨 첫 row 줄 컬럼 제목 기재

# 네이버 에서는 ""로 검색어를 넣으면 해당텍스트를 필수 인입

query_text = '"부산청년주간"'


for index in range(10):
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
    res = requests.get(naver_open_api, headers=header_params)
    if res.status_code == 200:
        data = res.json()
        for item in data["items"]:
            num += 1
            excel_sheet.append(
                [
                    num,
                    item["title"],
                    item["link"],
                    item["originallink"],
                    item["pubDate"],
                ]
            )
    else:
        print("Error Code: ", res.status_code)

excel_file.save("Youthweek.xlsx")
excel_file.close()
