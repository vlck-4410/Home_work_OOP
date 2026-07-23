import pytest
from src.classes import BaseProduct, Category, Product, LawnGrass, Smartphone

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

def test_smartphone_initialization():
    """Тест создания объекта класса Smartphone."""
    smartphone = Smartphone(
        name="iPhone 15",
        description="Флагман от Apple",
        price=120000.0,
        quantity=10,
        efficiency="Высокая",
        model="Pro Max",
        memory=256,
        color="Титановый"
    )
    assert smartphone.name == "iPhone 15"
    assert smartphone.price == 120000.0
    assert smartphone.efficiency == "Высокая"
    assert smartphone.model == "Pro Max"
    assert smartphone.memory == 256
    assert smartphone.color == "Титановый"

def test_lawngrass_initialization():
    """Тест создания объекта класса LawnGrass."""
    grass = LawnGrass(
        name="Изумруд",
        description="Быстрорастущий красивый газон",
        price=500.0,
        quantity=50,
        country="Нидерланды",
        germination_period="10–14 дней",
        color="Ярко-зеленый"
    )
    assert grass.name == "Изумруд"
    assert grass.quantity == 50
    assert grass.country == "Нидерланды"
    assert grass.germination_period == "10–14 дней"
    assert grass.color == "Ярко-зеленый"


def test_product_addition_same_type():
    """Тест успешного сложения товаров одного класса (Смартфонов)."""
    sp1 = Smartphone("iPhone 15", "Apple", 100000.0, 2, "Высокая", "15", 256, "Черный")
    sp2 = Smartphone("Xiaomi 14", "Xiaomi", 80000.0, 3, "Высокая", "14", 512, "Серый")

    assert sp1 + sp2 == 440000.0


def test_product_addition_different_types_raises_error():
    """Тест, что сложение товаров разных классов вызывает TypeError."""
    smartphone = Smartphone("iPhone 15", "Apple", 120000.0, 2, "Высокая", "15", 256, "Черный")
    grass = LawnGrass("Изумруд", "Газон", 500.0, 10, "РФ", "7 дней", "Зеленый")

    with pytest.raises(TypeError):
        _ = smartphone + grass


def test_category_add_subclass_product():
    """Тест успешного добавления наследника класса Product в категорию."""
    category = Category("Электроника", "Техника", [])
    smartphone = Smartphone("iPhone 15", "Apple", 120000.0, 2, "Высокая", "15", 256, "Черный")
    category.add_product(smartphone)
    assert "iPhone 15" in category.products


def test_category_add_invalid_product_raises_error():
    """Тест, что добавление стороннего объекта в категорию вызывает TypeError."""
    category = Category("Электроника", "Техника", [])

    with pytest.raises(TypeError):
        category.add_product("Я просто строка, меня нельзя добавлять!")

def test_base_product_cannot_be_instantiated():
    """Тест, что нельзя создать объект напрямую из абстрактного класса BaseProduct."""
    with pytest.raises(TypeError):
        BaseProduct()

def test_product_inherits_base_product():
    """Тест, что Product и его подклассы являются наследниками BaseProduct."""
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, BaseProduct)
    assert issubclass(LawnGrass, BaseProduct)


def test_print_mixin_console_output(capsys):
    """Тест работы PrintMixin: проверка вывода информации о создании объекта в консоль."""
    Product("Продукт1", "Описание продукта", 1200.0, 10)
    captured = capsys.readouterr()
    assert "Product('Продукт1', 'Описание продукта', 1200.0, 10)" in captured.out