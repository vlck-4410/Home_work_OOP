import pytest
from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    """
    Фикстура, которая автоматически запускается ПЕРЕД каждым тестом.
    Она сбрасывает счетчики в 0, чтобы тесты были изолированными
    и не ломали логику друг друга из-за накопления.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест корректности создания объекта Product и его атрибутов."""
    product = Product(
        name="Samsung Galaxy C23 Ultra",
        description="Смартфон для удобства жизни",
        price=180000.0,
        quantity=5
    )

    assert product.name == "Samsung Galaxy C23 Ultra"
    assert product.description == "Смартфон для удобства жизни"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization():
    """Тест корректности создания объекта Category и хранения списка товаров."""
    product1 = Product("Samsung", "Смартфон", 100000.0, 3)
    product2 = Product("iPhone", "Смартфон", 120000.0, 2)

    category = Category(
        name="Смартфоны",
        description="Гаджеты",
        products=[product1, product2]
    )

    assert category.name == "Смартфоны"
    assert category.description == "Гаджеты"
    assert category.products == [product1, product2]
    assert len(category.products) == 2


def test_category_counters_accumulation():
    """
    Тест проверяет правильность НАКОПЛЕНИЯ количества категорий и товаров.
    Именно этот тест падал у Александры из-за знака '=' вместо '+='.
    """
    assert Category.category_count == 0
    assert Category.product_count == 0

    p1 = Product("Товар 1", "Описание 1", 100.0, 1)
    p2 = Product("Товар 2", "Описание 2", 200.0, 2)
    Category("Категория 1", "Описание категории 1", [p1, p2])

    assert Category.category_count == 1
    assert Category.product_count == 2

    p3 = Product("Товар 3", "Описание 3", 300.0, 3)
    p4 = Product("Товар 4", "Описание 4", 400.0, 4)
    p5 = Product("Товар 5", "Описание 5", 500.0, 5)
    Category("Категория 2", "Описание категории 2", [p3, p4, p5])

    assert Category.category_count == 2
    assert Category.product_count == 5


def test_empty_category():
    """Тест создания категории без товаров (пустой список)."""
    empty_category = Category(
        name="Пустая категория",
        description="Здесь пока ничего нет",
        products=[]
    )

    assert empty_category.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_zero_values():
    """Тест корректности создания товара с нулевой ценой и нулевым количеством."""
    free_product = Product(
        name="Промо-товар",
        description="Бесплатный тестер",
        price=0.0,
        quantity=0
    )

    assert free_product.price == 0.0
    assert free_product.quantity == 0