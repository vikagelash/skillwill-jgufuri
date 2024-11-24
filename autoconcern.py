import random
from abc import ABC, abstractmethod


class Mixin:
    existing_codes = set()

    @staticmethod
    def generate_unique_code():
        while True:
            code = random.randint(1000, 1000000)
            if code not in Mixin.existing_codes:
                Mixin.existing_codes.add(code)
                return code


class Vehicle(ABC):
    def __init__(self, name: str, model: str):
        self._name = name
        self._model = model

    @abstractmethod
    def describe(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def model(self):
        return self._model


class Engine:
    def __init__(self, horsepower: int):
        if horsepower <= 0:
            raise ValueError("Horsepower must be a positive number.")
        self.__horsepower = horsepower

    @property
    def horsepower(self):
        return self.__horsepower

    @horsepower.setter
    def horsepower(self, value: int):
        if value <= 0:
            raise ValueError("Horsepower must be a positive number.")
        self.__horsepower = value

    def display_info(self):
        return f"Engine Horsepower: {self.__horsepower} HP"


class Car(Mixin, Vehicle):
    def __init__(self, name: str, model: str, engine: Engine, price: float, year_of_manufacture: int):
        super().__init__(name, model)
        self._engine = engine
        self._price = price
        self._year_of_manufacture = year_of_manufacture
        self._car_code = self.generate_unique_code()
        self._is_sold = False  

    @property
    def engine(self):
        return self._engine

    @property
    def price(self):
        return self._price

    @property
    def car_code(self):
        return self._car_code

    @property
    def year_of_manufacture(self):
        return self._year_of_manufacture

    def describe(self):
        return f"{self.name} {self.model} with engine: {self.engine.display_info()} and costs ${self.price}."

    def __str__(self):
        status = "Sold" if self._is_sold else "Available"
        return f"Car(Name: {self.name}, Model: {self.model}, Engine: {self.engine.display_info()}, Price: ${self.price}, Code: {self.car_code}, Status: {status})"

    def mark_as_sold(self):
        self._is_sold = True

    def apply_discount(self, discount_percentage: float):
        if self._is_sold:
            raise ValueError(f"Cannot apply discount: {self.name} {self.model} has been sold.")
        self._price -= self._price * (discount_percentage / 100)
        print(f"New price of {self.name} {self.model}: ${self._price:.2f}")

    def update_price(self, new_price: float):
        if self._is_sold:
            raise ValueError(f"Cannot update price: {self.name} {self.model} has been sold.")
        self._price = new_price
        print(f"Price of {self.name} {self.model} updated to ${self._price:.2f}")


class Factory:
    def __init__(self):
        self.available_cars = []

    def create_car(self, name: str, model: str, engine: Engine, price: float, year_of_manufacture: int):
        car = Car(name, model, engine, price, year_of_manufacture)
        self.available_cars.append(car)
        print(f"Car {car.name} {car.model} added to the factory's inventory.")
        return car

    def check_availability(self, model: str):
        available_cars = [car for car in self.available_cars if car.model == model and not car._is_sold]
        return available_cars

    def dispatch_car(self, car: Car, customer: 'Customer'):
        if car not in self.available_cars:
            raise ValueError(f"Car {car.name} is not available in the factory.")
        self.available_cars.remove(car)
        car.mark_as_sold()  
        customer.purchases.append(car)
        print(f"Car {car.name} has been dispatched to customer {customer.name}.")


class Customer(Mixin):
    def __init__(self, name: str, contact: str):
        self.name = name
        self.contact = contact
        self.customer_code = self.generate_unique_code()
        self.__purchases = []

    @property
    def purchases(self):
        return self.__purchases

    def request_car(self, factory: Factory, car_model: str):
        print(f"{self.name} (Code: {self.customer_code}) is requesting a {car_model}.")
        available_cars = factory.check_availability(car_model)
        if available_cars:
            car = available_cars[0]  
            factory.dispatch_car(car, self)  
            print(f"Car {car.name} is now owned by {self.name}.")
        else:
            print(f"Car model '{car_model}' is not available.")

    def get_details(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "customer_code": self.customer_code,
            "purchases": [str(car) for car in self.purchases],
        }

    def describe(self):
        return f"Customer '{self.name}' has purchased {len(self.purchases)} car(s)."

    def __str__(self):
        return f"Customer(Name: {self.name}, Contact: {self.contact})"


if __name__ == "__main__":
    factory = Factory()
    car1 = factory.create_car("BMW", "Series 3", Engine(300), 20000.50, 2022)
    car2 = factory.create_car("Mercedes", "Series C", Engine(500), 22000.00, 2022)

    print("\nAvailable cars in the factory:")
    for car in factory.available_cars:
        print(car)

    customer1 = Customer(name="Vika", contact="123-456-7890")
    customer1.request_car(factory, "Series 3")

    print("\nCustomer Details:")
    print(customer1.get_details())

    print("\nAvailable cars in the factory after sale:")
    for car in factory.available_cars:
        print(car)

    
    try:
        car1.apply_discount(10)
    except ValueError as e:
        print(e)

    try:
        car1.update_price(18000)
    except ValueError as e:
        print(e)
