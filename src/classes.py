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

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """
        Класс-метод для создания объекта из словаря с проверкой на дубликаты.
        Если товар с таким именем уже есть в existing_products,
        обновляет его количество и цену, возвращая измененный объект.
        """
        if existing_products:
            for product in existing_products:
                if product.name == product_data["name"]:
                    product.quantity += product_data["quantity"]
                    product.price = max(product.price, product_data["price"])
                    return product
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )


class Category:
    category_count = 0
    product_count = 0
    name = str
    description = str
    __products = list


    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

        def add_product(self, product):
            """Метод для добавления товарав приватный список категории"""
            self.__products.append(product)
            Category.product_count += 1

        @property
        def products(self):
            """Геттер для вывода списка товаров в виде отформатированный
            строк"""
            products_strings = []
            for product in self.__products:
                products_strings.append(f'{product.name}, {product.price} руб. Остаток: {product.quantity} шт')
            return '\n'.join(products_strings)


if __name__ == "__main__":
    product_data = read_file_products("C:/Users/Serega/PycharmProjects/Home_work_OOP/data/products.json")

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
