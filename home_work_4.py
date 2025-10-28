# Задача 1-4

# from pydantic import BaseModel, field_validator
# 
# class Book(BaseModel):
#     title: str
#     author: str
#     year: int
#     available: bool
#     categories: list[str]
# 
#     @field_validator('categories', mode='before')
#     def category_verification(cls, categories) -> list[str]:
# 
#         if type(categories) != list:
#             raise ValueError('Неверный формат')
#         else:
#             return categories
# 
# 
# class User(BaseModel):
#     name: str
#     email: str
#     membership_id: str
# 
#     @field_validator('email', mode='before')
#     def email_validator(cls, email) -> str:
# 
#         if not email:
#             raise ValueError('Забыли указать Email')
#         elif '.' not in email:
#             raise ValueError('Забыли указать "."')
#         elif '@' not in email:
#             raise ValueError('Забыли указать "@"')
#         else:
#             return email
# 
# class Library(BaseModel):
#     books: str
#     users: str
# 
#     def total_books(self, books: str) -> int:
#         print(f'Всего книг в библиотеке: {len(books)}')
# 
# 
# ivan = Book(title='NameBook', author='Man', year=1996, available=True, categories=['HIT'])
# petr = User(name="Peter", email="Peter@ya.ru", membership_id="25")
# print(petr)
# print(ivan)


# Задача 2-4

# def add_book(book: str) -> list[str]:
#     list_book = []
#     if book not in list_book:
#         list_book.append(book)
#
#
# def find_book(book: str) -> bool:
#     list_book = []
#     if book in list_book:
#         print('The book is in the library')
#
#

# class BookNotAvailable(Exception):
#     def is_book_borrow(book: str) -> bool:
#         list_book=[]
#         if book not in list_book:
#             raise BookNotAvailable('Недоступна')
#         else:
#             print('Недоступна')

# def return_book(book: str) -> list[str]:
#     list_book = []
#     list_book.append(book)