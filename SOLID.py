from abc import ABC, abstractmethod
from typing import List, Dict
import json

class Pizza(ABC):
    """Базовый класс для пиццы."""
    @abstractmethod
    def __init__(self, name: str, base_price: float, toppings: List[str] = []):
        self.name = name
        self.base_price = base_price
        self.toppings = toppings
        self.price = base_price

    def add_topping(self, topping: str):
        """Добавляет топпинг к пицце."""
        self.toppings.append(topping)
        self.price += 0.5

    def get_price(self) -> float:
        """Возвращает цену пиццы."""
        return self.price

    def __str__(self) -> str:
        """Представление пиццы в виде строки."""
        toppings_str = ", ".join(self.toppings) if self.toppings else "без добавок"
        return f"{self.name} ({toppings_str}): {self.price:.2f}"

class StandardPizza(Pizza):
    """Класс для стандартной пиццы."""
    def __init__(self, name: str, base_price: float, toppings: List[str] = []):
        super().__init__(name, base_price, toppings)

class CustomPizza(Pizza):
    """Класс для пользовательской пиццы."""
    def __init__(self, name: str, base_price: float, toppings: List[str] = []):
        super().__init__(name, base_price, toppings)

class PaymentMethod(ABC):
    """Базовый класс для способа оплаты."""
    @abstractmethod
    def pay(self, amount: float):
        """Обрабатывает оплату."""

class CashPayment(PaymentMethod):
    """Класс для оплаты наличными."""
    def pay(self, amount: float):
        print("Оплата наличными: ", amount)

class CardPayment(PaymentMethod):
    """Класс для оплаты картой."""
    def pay(self, amount: float):
        print("Оплата картой: ", amount)

class Order:
    """Класс для заказа."""
    def __init__(self, pizza: Pizza, payment_method: PaymentMethod):
        self.pizza = pizza
        self.payment_method = payment_method

    def place_order(self):
        """Создает заказ."""
        print(f"Заказана пицца: {self.pizza}")
        self.payment_method.pay(self.pizza.get_price())
        self.save_order_to_file()

    def save_order_to_file(self):
        """Сохраняет информацию о заказе в файл."""
        with open("orders.json", "a", encoding="utf-8") as f:
            order_data = {
                "name": self.pizza.name,
                "base_price": self.pizza.base_price,
                "toppings": self.pizza.toppings,
                "price": self.pizza.price
            }
            json.dump(order_data, f, indent=4, ensure_ascii=False)
            f.write("\n")

class Pizzeria:
    """Класс для пиццерии."""
    def __init__(self):
        self.orders: List[Order] = []
        self.standard_pizzas: List[Pizza] = [
            StandardPizza("Маргарита", 7.99),
            StandardPizza("Пепперони", 8.99),
            StandardPizza("Вегетарианская", 9.99),
            StandardPizza("Четыре сыра", 10.99),
            StandardPizza("Гавайская", 11.99)
        ]
        self.toppings: List[str] = [
            "сладкий лук", "халапеньо", "чили",
            "соленый огурец", "оливки", "прошутто"
        ]
        self.total_sales: float = 0
        self.total_profit: float = 0

    def create_order(self):
        """Создает новый заказ."""
        while True:
            print("\nВыберите пиццу:")
            for i, pizza in enumerate(self.standard_pizzas):
                print(f"{i+1}. {pizza.name} - {pizza.base_price:.2f}")
            print("6. Создать собственную пиццу")

            choice = input("Введите номер пиццы: ")
            if choice == "6":
                name = input("Введите название пиццы: ")
                base_price = float(input("Введите базовую цену пиццы: "))
                pizza = CustomPizza(name, base_price)
            elif choice.isdigit() and 1 <= int(choice) <= 5:
                pizza = self.standard_pizzas[int(choice) - 1]
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

        while True:
            print("\nДобавить топпинги? (y/n)")
            choice = input("Введите y или n: ")
            if choice.lower() == 'y':
                print("\nДоступные топпинги:")
                for i, topping in enumerate(self.toppings):
                    print(f"{i+1}. {topping}")
                topping_choice = input("Введите номер топпинга (или 0, чтобы завершить): ")
                if topping_choice.isdigit() and 1 <= int(topping_choice) <= len(self.toppings):
                    pizza.add_topping(self.toppings[int(topping_choice) - 1])
                elif topping_choice == "0":
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            else:
                break

        while True:
            print("\nВыберите способ оплаты:")
            print("1. Наличными")
            print("2. Картой")
            payment_choice = input("Введите 1 или 2: ")
            if payment_choice == "1":
                payment_method = CashPayment()
                break
            elif payment_choice == "2":
                payment_method = CardPayment()
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

        order = Order(pizza, payment_method)
        self.orders.append(order)
        order.place_order()

    def get_statistics(self):
        """Выводит статистику о продажах."""
        print("\nСтатистика:")
        print(f"Количество проданных пицц: {len(self.orders)}")
        print(f"Выручка: {self.total_sales:.2f}")
        print(f"Прибыль: {self.total_profit:.2f}")

    def run(self):
        """Запускает приложение."""
        while True:
            print("\nЧто вы хотите сделать?")
            print("1. Создать заказ")
            print("2. Просмотреть статистику")
            print("3. Выход")

            choice = input("Введите 1, 2 или 3: ")
            if choice == "1":
                self.create_order()
                self.total_sales += self.orders[-1].pizza.get_price()
                self.total_profit += self.orders[-1].pizza.get_price()
            elif choice == "2":
                self.get_statistics()
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    pizzeria = Pizzeria()
    pizzeria.run()
