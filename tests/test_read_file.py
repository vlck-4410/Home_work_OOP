import json
import pytest
from src.read_file import read_file_products

def test_read_file_products_success(tmp_path):
    """Тест успешного чтения корректного JSON-файла с данными."""
    mock_data = [
        {
            "name": "Смартфоны",
            "description": "Гаджеты для жизни",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "Флагман",
                    "price": 180000.0,
                    "quantity": 5
                }
            ]
        }
    ]


    fake_file_path = tmp_path / "test_products.json"

    with open(fake_file_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False)

    result = read_file_products(str(fake_file_path))

    assert result == mock_data
    assert len(result) == 1
    assert result[0]["name"] == "Смартфоны"
    assert result[0]["products"][0]["price"] == 180000.0

def test_read_file_products_empty_list(tmp_path):
    """Тест чтения JSON-файла, в котором сохранен пустой список."""
    fake_file_path = tmp_path / "empty_products.json"

    with open(fake_file_path, "w", encoding="utf-8") as f:
        json.dump([], f)

    result = read_file_products(str(fake_file_path))

    assert result == []
    assert len(result) == 0

def test_read_file_products_not_found():
    """Тест проверяет, что при передаче несуществующего пути вызывается ошибка FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_file_products("this_file_does_not_exist_123.json")
