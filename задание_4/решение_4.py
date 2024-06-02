from decimal import Decimal, InvalidOperation
import json


JSON_PATH = "database.json"


class Product:
    """Базовый класс для всех классов"""

    def __init__(self, name: str, category: str, price: Decimal, weight: float) -> None:
        self.set_name(name)
        self.set_category(category)
        self.set_price(price)
        self.set_weight(weight)

    def set_name(self, name) -> None:
        if isinstance(name, str) and 0 < len(name) <= 30:
            self.__name = name
        else:
            raise ValueError("Не является строкой или длиннее 30 символов")

    def get_name(self) -> str:
        return self.__name

    def set_category(self, category):
        if isinstance(category, str) and 0 < len(category) <= 30:
            self.__category = category
        else:
            raise ValueError("Не является строкой или длиннее 30 символов")

    def get_category(self) -> str:
        return self.__category

    def set_price(self, price):
        try:
            value = Decimal(price)
            if value >= 0 and value == value.quantize(Decimal("0.01")):
                self.__price = value
            else:
                raise ValueError("Больше 2 знаков после запятой")
        except InvalidOperation:
            print("Не является числом")

    def get_price(self) -> Decimal:
        return self.__price

    def set_weight(self, weight):
        if isinstance(weight, float) and weight >= 0:
            self.__weight = weight
        else:
            raise ValueError("Не является числом")

    def get_weight(self) -> float:
        return self.__weight


class Buy(Product):
    """производный класс для класса Product и базовый класс для класса Check"""

    def __init__(
        self, name: str, category: str, price: Decimal, weight: float, quantity: int
    ) -> None:
        super().__init__(name, category, price, weight)
        self.set_quantity(quantity)

    def set_quantity(self, quantity) -> None:
        if isinstance(quantity, int) and quantity > 0:
            self.__quantity = quantity
        else:
            raise ValueError("Не является целым числом или количество меньше 1 штуки")

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_total_price(self) -> Decimal:
        return self.get_quantity() * self.get_price()

    def calculate_total_weight(self) -> float:
        return self.get_quantity() * self.get_weight()


class Check(Buy):
    """производный класс для класса Buy"""

    def __init__(
        self, name: str, category: str, price: Decimal, weight: float, quantity: int
    ) -> None:
        super().__init__(name, category, price, weight, quantity)

    def display_info(self):
        print("Товар:", self.get_name())
        print("Категория:", self.get_category())
        print("Цена за единицу:", self.get_price())
        print("Вес товара:", self.get_weight())
        print("Количество:", self.get_quantity())
        print("Полная стоимость покупки:", self.calculate_total_price())
        print("Общий вес покупки:", self.calculate_total_weight())


def get_products(path: str = JSON_PATH) -> list:
    """Получить список продуктов из json"""

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print("Ошибка чтения json")

    products = []

    try:
        for record in data:
            product = Product(
                record["name"],
                record["category"],
                Decimal(record["price"]),
                float(record["weight"]),
            )
            products.append(product) 
    except ValueError:
        print("Ошибка чтения записи")
    return products


# with open("database.json", "w", encoding="utf-8") as json_file:
#     try:
#         json.dump(product, json_file)
#     except Exception as e:
#         print("Ошибка записи в файл", e)


def main():
    get_products()


if __name__ == "__main__":
    main()
