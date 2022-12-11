import requests
import json
import re
from bs4 import BeautifulSoup
from collections import namedtuple

Category = namedtuple("Category", "name url")


class Course:
    def __init__(self, title, img_src, price, description, level, lectures_num, resources_num, subcategory, category):
        self.title = title
        self.img_src = img_src
        self.price = price
        self.description = description
        self.level = level
        self.lectures_num = lectures_num
        self.resources_num = resources_num
        self.subcategory = subcategory
        self.category = category

    @staticmethod
    def parse_data(data):
        kwargs = {
            "title": data.find("div", {"class": "name desktop"}).text,
            "img_src": data.find("img").get("data-src"),
            "price": data.find("div", {"class": "new desktop"}).text,
            "description": data.find("div", {"class": "description"}).text
        }

        details = data.find("div", {"class": "content__information--footer"}).\
            find_all("div", {"class": "information desktop"})
        if (details_len := len(details)) >= 1:
            kwargs["level"] = details[0].text.split(":")[1].strip()
        else:
            kwargs["level"] = ""

        if details_len >= 2:
            kwargs["lectures_num"] = details[1].text.split()[0]
        else:
            kwargs["lectures_num"] = ""

        if details_len >= 3:
            kwargs["resources_num"] = details[2].text.split()[0]
        else:
            kwargs["resources_num"] = ""

        subcategory_pattern = re.compile(r"\['.*',\s?'.*'\]")
        assignment = re.search(subcategory_pattern, data["onclick"])
        kwargs["category"], kwargs["subcategory"] = eval(assignment.group())

        return Course(**kwargs)


def scrap_categories(url="https://strefakursow.pl"):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'lxml')
    course_categories_container = soup.find("div", {"class": "menu-navigation__container"})
    course_categories_content = course_categories_container.find("div", {"class": "content"})
    href_tags = course_categories_content.find_all("a")
    return [Category(name=category.find("span").text, url=f"{url}{category.get('href')}") for category in href_tags]


def scrap_courses(categories):
    output = {"products": []}
    course_names_list = []
    for category in categories:
        page_num = 1

        while True:
            response = requests.get(category.url.replace(".html", f"/{page_num}.html"))
            if response.status_code != 200:
                break

            course_list_soup = BeautifulSoup(response.text, "lxml")
            courses = course_list_soup.find("div", {"class": "b-product-list"})\
                .find_all("div", {"class": "b-product-box desktop"})

            for course_data in courses:
                course = Course.parse_data(course_data)
                if "#" not in course.title not in course_names_list:
                    output["products"].append(vars(course))
                    course_names_list.append(course.title)

            page_num += 1

    return output


def save_product_list(product_list):
    with open("products.json", "w") as f:
        f.write(json.dumps(product_list, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    categories = scrap_categories()
    product_list = scrap_courses(categories)
    save_product_list(product_list)
