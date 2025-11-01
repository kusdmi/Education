import threading
import time
#Задание 1
# def square():
#     for i in range(1, 11):
#         print(f'Квадрат {i} = {i**2}')
#
# def cube():
#     for i in range(1, 11):
#         print(f'Куб {i} = {i**3}')
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=square)
#     t2 = threading.Thread(target=cube)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print("Вычисления завершены!")


#Задание 2

# def square():
#     for i in range(1, 11):
#         print(f'Квадрат {i} = {i**2}')
#         time.sleep(1)
#
# def cube():
#     for i in range(1, 11):
#         print(f'Куб {i} = {i**3}')
#         time.sleep(1)
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=square)
#     t2 = threading.Thread(target=cube)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print("Вычисления завершены!")


