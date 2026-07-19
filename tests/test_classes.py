import pytest
from h11 import PRODUCT_ID

from src.classes import Category, Product

@pytest.fixture(autouse=True)
def reset_counters():
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture(autouse=True)
def reset_counters():
    """Сброс счетчиков перед каждым тестом, чтобы они не зависели друг от друга."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест создания товара."""
    product = Product("Samsung Galaxy C23 Ultra", "Смартфон", 180000.0, 5)
    assert product.name == "Samsung Galaxy C23 Ultra"
    assert product.description == "Смартфон"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization_and_getter():
    """Тест создания категории и работы строкового геттера товаров."""
    product1 = Product("Samsung", "Смартфон", 100000.0, 3)
    product2 = Product("iPhone", "Смартфон", 120000.0, 2)

    category = Category("Смартфоны", "Гаджеты", [product1, product2])

    assert category.name == "Смартфоны"
    assert category.description == "Гаджеты"
    expected_output = (
        "Samsung, 100000.0 руб. Остаток: 3 шт.\n"
        "iPhone, 120000.0 руб. Остаток: 2 шт."
    )
    assert category.products == expected_output


def test_category_counters_accumulation():
    """Тест корректного накопления (а не перезаписи) счетчиков."""
    p1 = Product("Товар 1", "Описание 1", 100.0, 1)
    p2 = Product("Товар 2", "Описание 2", 200.0, 2)
    Category("Категория 1", "Описание категории", [p1, p2])

    assert Category.category_count == 1
    assert Category.product_count == 2

    p3 = Product("Товар 3", "Описание 3", 300.0, 1)
    Category("Категория 2", "Описание категории 2", [p3])
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_add_product():
    """Тест метода add_product."""
    category = Category("Смартфоны", "Гаджеты", [])
    product = Product("Xiaomi", "Бюджетный", 30000.0, 10)
    category.add_product(product)

    assert "Xiaomi, 30000.0 руб. Остаток: 10 шт." in category.products


def test_price_setter_validation(monkeypatch):
    """Тест работы сеттера цены с валидацией и подтверждением."""
    product = Product("Тест", "Описание", 100.0, 5)

    product.price = -10
    assert product.price == 100.0

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 80.0
    assert product.price == 80.0


def test_product_str_representation():
    """Тест магического метода __str__ для класса Product."""
    product = Product('Samsung Galaxy S25 Ultra', "Смартфон", 90000.0, 5)
    assert str(product) == "Samsung Galaxy S25 Ultra, 90000.0 руб. Остаток: 5 шт."


def test_category_str_representation():
    """Тест магического метода __str__ для класса Category."""
    product_1 = Product('Samsung','Смартфон', 100000.0, 3)
    product_2 = Product('Iphone', 'Смартфон', 120000.0, 2)
    category = Category('Смартфоны', "Гаджеты", [product_1, product_2])

    assert str(category) =="Смартфоны, количество продуктов: 5 шт."

def test_product_addition():
    """Тест магического метода __add__ для класса Product."""
    product_1 = Product('Товар А', "Описание А", 100.0, 10)
    product_2 = Product('Товар Б', "Описание Б", 200.0, 2)

    assert product_1 + product_2 == 1400.0