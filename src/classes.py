from src.read_file import read_file_products

class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price  # Делаем цену приватной (Задание 4)
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с валидацией (Задание 4 + допка)."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return


        if new_price < self.__price:
            user_check = input("Цена снижается. Вы уверены, что хотите изменить цену? (y/n): ")
            if user_check.lower() != 'y':
                print("Отмена изменения цены.")
                return

        self.__price = new_price

    def __str__(self):
        """Строковое отображение товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод для складывания двух товаров.
        Возвращает общую стоимость всех единиц обоих товаров на складе.
        Вызывает TypeError, если товары принадлежат к разным классам.
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов.")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products=None):
        """Класс-метод для создания объекта из словаря (Задание 3 + допка)."""
        if existing_products is None:
            existing_products = []

        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        for product in existing_products:
            if product.name == name:
                product.quantity += quantity
                product.price = max(product.price, price)
                return product

        return cls(name, description, price, quantity)

class Smartphone(Product):
    """Класс-наследник для описания смартфонов."""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    """Класс-наследник для описания газонной травы."""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

class Category:
    category_count = 0
    product_count = 0
    name: str
    description: str

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = list(products)  # Приватный атрибут (Задание 1)

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        """
        Добавляет продукт в категорию.
        Вызывает TypeError, если передаваемый объект не является продуктом или его наследником.
        """
        if not isinstance(product, Product):
            raise TypeError("Добавлять можно только объекты класса Product или его наследников.")

        self.__products.append(product)

    @property
    def products(self):
        """Оптимизированный геттер для вывода списка товаров через str()."""
        return '\n'.join([str(product) for product in self.__products])


    def __str__(self):
        """Строковое отображение категории с подсчетом всех товаров на складе"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total_quantity} шт.'


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
