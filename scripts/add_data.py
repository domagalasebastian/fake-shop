import json
import requests
import urllib.request
import xml.etree.ElementTree as et


class Category:
    def __init__(self, name, id_parent=2, root_category=0, active=1):
        self.idx = None
        self.name = name
        self.id_parent = id_parent
        self.root_category = root_category
        self.link_rewrite = name.replace(" ", "-")
        self.active = active

    def to_xml(self):
        root = et.Element("prestashop")
        category = et.Element("category")
        for field in filter(lambda x: x != "idx" and not x.startswith('__') and not callable(getattr(self, x)), dir(self)):
            new_element = et.SubElement(category, field)
            if field in ("name", "link_rewrite"):
                lang_element = et.SubElement(new_element, "language")
                lang_element.text = str(getattr(self, field))
                lang_element.attrib["id"] = "2"
            else:
                new_element.text = str(getattr(self, field))

        root.append(category)

        return et.tostring(root, encoding="utf-8", method="xml")

    def post(self):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        response = client.post(url="https://localhost/prestashop/api/categories", headers=headers,
                               data=self.to_xml(), verify=False)
        if response.status_code != 201:
            raise Exception("Post operation failed!")
        else:
            response_xml = et.fromstring(response.text)
            self.idx = response_xml.find("category").find("id").text


class Product:
    def __init__(self, name, price, id_category, id_category_default, description, img_url, features, active=1, minimal_quantity=1, available_for_order=1, id_tax_rules_group=1, on_sale=0, state=1, online_only=1, show_price=1, redirect_type="404"):
        self.idx = None
        self.name = name
        self.active = active
        self.link_rewrite = name.replace(" ", "-")
        self.price = price
        self.minimal_quantity = minimal_quantity
        self.on_sale = on_sale
        self.id_category = id_category
        self.id_category_default = id_category_default
        self.description = description
        self.redirect_type = redirect_type
        self.img_url = img_url
        self.state = state
        self.online_only = online_only
        self.show_price = show_price
        self.id_tax_rules_group = id_tax_rules_group
        self.features = features
        self.available_for_order = available_for_order

    def to_xml(self):
        root = et.Element("prestashop")
        product = et.Element("product")
        for field in filter(lambda x: x not in ["idx", "id_category", "features"] and not x.startswith('__') and not callable(getattr(self, x)),
                            dir(self)):
            new_element = et.SubElement(product, field)
            if field in ("name", "link_rewrite"):
                lang_element = et.SubElement(new_element, "language")
                lang_element.text = str(getattr(self, field))
                lang_element.attrib["id"] = "2"
            else:
                new_element.text = str(getattr(self, field))

        associations_element = et.SubElement(product, "associations")
        categories_element = et.SubElement(associations_element, "categories")
        for idx in self.id_category:
            category_element = et.SubElement(categories_element, "category")
            new_element = et.SubElement(category_element, "id")
            new_element.text = idx

        product_features_element = et.SubElement(associations_element, "product_features")
        for feature_id, feature_value in features.items():
            product_feature_element = et.SubElement(product_features_element, "product_feature")
            new_element = et.SubElement(product_feature_element, "id")
            new_element.text = feature_id
            new_element = et.SubElement(product_feature_element, "id_feature_value")
            new_element.text = feature_value

        root.append(product)
        return et.tostring(root, encoding="utf-8", method="xml")

    def post(self):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        response = client.post(url="https://localhost/prestashop/api/products", headers=headers,
                               data=self.to_xml(), verify=False)
        if response.status_code != 201:
            print(response.text)
            raise Exception("Post operation failed!")
        else:
            response_xml = et.fromstring(response.text)
            self.idx = response_xml.find("product").find("id").text
            self.update_quantity(response_xml.find("product").find("associations").find("stock_availables").find("stock_available").find("id").text)
            self.post_image()

    def update_quantity(self, stock_availables_idx):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        response = client.get(url="https://localhost/prestashop/api/stock_availables/{}".format(stock_availables_idx), headers=headers, verify=False)
        response_xml = et.fromstring(response.text)
        response_xml.find("stock_available").find("quantity").text = "10000000"
        response = client.put(url="https://localhost/prestashop/api/stock_availables/{}".format(stock_availables_idx), headers=headers,
                               data=et.tostring(response_xml, encoding="utf-8", method="xml"), verify=False)
        if response.status_code != 200:
            print(response.text)
            raise Exception("Post operation failed!")

    # def quantity_xml(self, stock_availables_idx):
    #     root = et.Element("prestashop")
    #     stock_available = et.Element("stock_available")
    #     new_element = et.SubElement(stock_available, "id")
    #     new_element.text = stock_availables_idx
    #     new_element = et.SubElement(stock_available, "quantity")
    #     new_element.text = "10000000"
    #     root.append(stock_available)
    #     return et.tostring(root, encoding="utf-8", method="xml")

    def post_image(self):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        urllib.request.urlretrieve(self.img_url, "/var/www/html/prestashop/img/product{}.jpg".format(self.idx))
        files = {'image': open("/var/www/html/prestashop/img/product{}.jpg".format(self.idx), 'rb')}
        response = client.post(url="https://localhost/prestashop/api/images/products/{}".format(self.idx), files=files, verify=False)

    # def image_xml_data(self):
    #     urllib.request.urlretrieve(self.img_url, "/var/www/html/prestashop/img/product{}.jpg".format(self.idx))
    #     root = et.Element("prestashop")
    #     image = et.Element("image")
    #     new_element = et.SubElement(image, "image_path")
    #     new_element.text = "/home/sdomagal/produkt1.jpg"
    #     root.append(image)
    #     return et.tostring(root, encoding="utf-8", method="xml")

# def get_categories(products_data):
#     categories = {}
#     for product in products_data:
#         if product["category"] in categories:
#             categories[product["category"]].add(product["subcategory"])
#         else:
#             categories[product["category"]] = set()
#
#     return categories

def load_product_list(filename="products.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    return data["products"]


# def post_category_data(categories):
#     for category in categories.keys():
#         parent_category = Category(name=category)
#         parent_category.post()
#         for subcategory in categories[category]:
#             if subcategory:
#                 Category(name=subcategory, id_parent=parent_category.idx).post()

class Feature:
    def __init__(self, name):
        self.idx = None
        self.name = name

    def to_xml(self):
        root = et.Element("prestashop")
        product_feature = et.Element("product_feature")
        for field in filter(lambda x: x != "idx" and not x.startswith('__') and not callable(getattr(self, x)),
                            dir(self)):
            new_element = et.SubElement(product_feature, field)
            if field in ("name",):
                lang_element = et.SubElement(new_element, "language")
                lang_element.text = str(getattr(self, field))
                lang_element.attrib["id"] = "2"
            else:
                new_element.text = str(getattr(self, field))

        root.append(product_feature)

        return et.tostring(root, encoding="utf-8", method="xml")

    def post(self):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        response = client.post(url="https://localhost/prestashop/api/product_features", headers=headers,
                               data=self.to_xml(), verify=False)
        if response.status_code != 201:
            raise Exception("Post operation failed!")
        else:
            response_xml = et.fromstring(response.text)
            self.idx = response_xml.find("product_feature").find("id").text


class FeatureValue:
    def __init__(self, id_feature, value, custom=0):
        self.idx = None
        self.id_feature = id_feature
        self.value = value
        self.custom = custom

    def to_xml(self):
        root = et.Element("prestashop")
        product_feature_value = et.Element("product_feature_value")
        for field in filter(lambda x: x != "idx" and not x.startswith('__') and not callable(getattr(self, x)),
                            dir(self)):
            new_element = et.SubElement(product_feature_value, field)
            if field in ("value",):
                lang_element = et.SubElement(new_element, "language")
                lang_element.text = str(getattr(self, field))
                lang_element.attrib["id"] = "2"
            else:
                new_element.text = str(getattr(self, field))

        root.append(product_feature_value)

        return et.tostring(root, encoding="utf-8", method="xml")

    def post(self):
        client = requests.Session()
        client.auth = ("GYNRZ63S9KF3U4M176GFBPAPEKIXNDQC", '')
        headers = {'Content-Type': 'application/xml'}
        print("dupa")
        print(self.to_xml())
        print("zupa")
        response = client.post(url="https://localhost/prestashop/api/product_feature_values", headers=headers,
                               data=self.to_xml(), verify=False)
        if response.status_code != 201:
            print(response.text)
            raise Exception("Post operation failed!")
        else:
            response_xml = et.fromstring(response.text)
            self.idx = response_xml.find("product_feature_value").find("id").text

if __name__ == "__main__":
    products = load_product_list()
    categories = {}
    subcategories = []
    levels = {}
    lectures_nums = {}
    materials_nums = {}
    level_feature = Feature(name="Poziom")
    level_feature.post()
    lectures_feature = Feature(name="Liczba wykładów")
    lectures_feature.post()
    materials_feature = Feature(name="Liczba materiałów")
    materials_feature.post()
#    import pdb

 #   pdb.set_trace()
    for product in products:
        if product["category"] not in categories:
            categories[product["category"]] = Category(name=product["category"])
            categories[product["category"]].post()

        if product["subcategory"]:
            subcategory = next(filter(lambda x: x.id_parent == categories[product["category"]].idx and x.name == product["subcategory"], subcategories), None)
            if subcategory is None:
                subcategory = Category(name=product["subcategory"], id_parent=categories[product["category"]].idx)
                subcategory.post()
                subcategories.append(subcategory)

        level = product["level"].capitalize()
        if level not in levels:
            levels[level] = FeatureValue(id_feature=level_feature.idx, value=level, custom=0)
            levels[level].post()

        if product["lectures_num"] not in lectures_nums:
            lectures_nums[product["lectures_num"]] = FeatureValue(id_feature=lectures_feature.idx, value=product["lectures_num"], custom=0)
            lectures_nums[product["lectures_num"]].post()

        if product["resources_num"] and product["resources_num"] not in materials_nums:
            materials_nums[product["resources_num"]] = FeatureValue(id_feature=materials_feature.idx, value=product["resources_num"], custom=0)
            materials_nums[product["resources_num"]].post()

        id_category = ["2", categories[product["category"]].idx]
        if product["subcategory"]:
            id_category.append(subcategory.idx)

        features = {level_feature.idx: levels[level].idx, lectures_feature.idx: lectures_nums[product["lectures_num"]].idx}
        if product["resources_num"]:
            features[materials_feature.idx] = materials_nums[product["resources_num"]].idx

        Product(name=product["title"], price=round(int(product["price"][:-2])/1.23, 2), id_category=id_category, id_category_default=id_category[-1], description=product["description"], img_url=product["img_src"], features=features).post()

