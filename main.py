import requests
from bs4 import BeautifulSoup
import lxml
import openpyxl
book = openpyxl.Workbook()
sheet = book.active


user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
header = {"User-Agent": user}
session = requests.Session()
count = 2

for j in range(1, 25):
    print(f"Page = {j}")
    url = f"https://allo.ua/ua/products/notebooks/page={j}"
    response = session.get(url, headers=header)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        all_products = soup.find_all('div', class_="product-card")
        print(len(all_products))

        for product in all_products:
            price = product.find("div", class_="v-pb__cur discount")
            title = product.find("a", class_="product-card__title")
            try:
                review = product.find("span", class_="review-button__text review-button__text--count")
            except AttributeError:
                review = 0
            with open("All_Products.txt", "a", encoding="utf-8") as file:
                file.write(f"{price.text} {title.text} {review.text}\n")
            book.save("All_products.xlsx")
            if product.find("div", class_="v-pb__old"):
                with open("With_Discounts.txt", "a", encoding = "utf-8") as file:
                    file.write(f"{price.text} {title.text} {review.text}\n")
                    sheet[f"A{count}"] = title.text
                    sheet[f"B{count}"] = price.text
                    sheet[f"C{count}"] = review.text
                    count += 1
                    book.save("With_Discounts.xlsx")

book.close()