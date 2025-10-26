class Product():
    
    def __init__(self, name: str, price: int, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity: int):
        if self.stock + quantity < 0:
            raise ValueError("Недостаточно товара на складе")
        self.stock += quantity
        print(f'Количество товаров на складе обновлено')



class Order():

    def __init__(self):
        self.products = {}

    def add_product(self, product: list, quantity: int):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if product.stock < quantity:
            raise ValueError(f"Недостаточно товара '{product.name}' на складе")
        
        product.update_stock(-quantity)
        self.products[product] = self.products.get(product, 0) + quantity

    def calculate_total(self):
        return sum(product.price * quantity for product, quantity in self.products.items())
    
    # Доп. метод
    def remove_product(self, product, quantity):
        self.products[product] -= quantity

        if self.products[product] == 0:
            del self.products[product]

    # Доп. метод
    def return_product(self, product, quantity):

        product.update_stock(quantity)

        # Закоментировал так как если оставить при вызове метода remove_product и после return_product, неверно считает сумму заказа (2 раза возвращает на склад) 
        #self.products[product] -= quantity

        if self.products[product] == 0:
            del self.products[product]

    # Как вариант апдейт 2-х методов удаление-возврат в один. Когда удаляем количество товаров из заказа не нужно вызывать метод возврата, а он автоматом возвращаеться на склад. Конечно есть вариант что на склад не надо возвращать, но это странно (исключение брак, возможно).
    def remove_return_products(self, product, quantity):

        self.products[product] -= quantity

        product.update_stock(quantity)

        if self.products[product] == 0:
            del self.products[product]



class Store():

    def __init__(self):
        self.products = []

    def add_product(self, product: list):
        self.products.append(product)

    def list_products(self):
        for product in self.products:
            print(f"{product.name} - Цена: {product.price}, Остаток: {product.stock}")

    def create_order(self):
        return Order()




# Создаем магазин
store = Store()

# Создаем товары
product1 = Product("Ноутбук", 1000, 5)
product2 = Product("Смартфон", 500, 10)

# Добавляем товары в магазин
store.add_product(product1)
store.add_product(product2)

# Список всех товаров
store.list_products()

#Обновляем товар (просто как проверка работоспособности)
Product.update_stock(product2, -7)
Product.update_stock(product1, -3)

# Остатки после 1-го обновления товара
store.list_products()

# Создаем заказ
order = store.create_order()

# Добавляем товары в заказ
order.add_product(product1, 2)
order.add_product(product2, 3)

# Выводим общую стоимость заказа
total = order.calculate_total()
print(f"Общая стоимость заказа: {total}")

# Остатки товара после добавления в заказ
store.list_products()

# Удаляем товары из заказа
# order.remove_product(product1, 1)
# order.remove_product(product2, 1)

# Возвращаем товары на склад
# order.return_product(product1, 1)
# order.return_product(product2, 1)

# Удаление и возврат товара в одном методе remove_return_products
order.remove_return_products(product1, 1)
order.remove_return_products(product2, 1)

# Выводим общую стоимость заказа после удаления
total = order.calculate_total()
print(f"Общая стоимость заказа: {total}")

# Проверяем остатки на складе после заказа удаления из заказа
store.list_products()

