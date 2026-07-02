from src.read_file import read_file_products


class Product:
    name = str
    description = str
    price = float
    quantity = int
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0
    product_count = 0
    name = str
    description = str
    products = list


    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count = len(products)


if __name__ == "__main__":
    product_data = read_file_products("products.json")

    categories = []
    for category_data in product_data:
        product_list = []
        for product_data in category_data['products']:
            product = Product(name = product_data["name"],
                                        description = product_data["description"],
                                        price = product_data["price"],
                                        quantity = product_data["quantity"])
            product_list.append(product)

        category = Category(name = category_data["name"],
                                description = category_data["description"],
                            products =product_list)
        categories.append(category)
    print('=' * 30)
    print('Статистика по классам')
    print('=' * 30)
    print(f'Всего создано категорий: {Category.category_count}')
    print(f'Всего товаров подсчитано: {Category.product_count}')
    print('=' * 30)
