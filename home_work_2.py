# Exercise №1
# with open('files_home_work_2/source.txt', 'r') as file:
#     with open('files_home_work_2/destination.txt', 'w') as new_file:
#         for line in file:
#             new_file.write(line)


# Exercise №2
# lists = []
# for i in open('files_home_work_2/prices.txt', 'r'):
#     lists.append(i.split())
#
# count = 0
# for i in range(len(lists)):
#     count += int(lists[i][2])
# print(f'Стоимость заказа составляет: {count}')


# Exercise №3
# lists = []
# for i in open('files_home_work_2/prices.txt', 'r'):
#     lists.append(i.split())
#
# count = 0
# for i in range(len(lists)):
#     for j in range(len(lists[i])):
#         if lists[i][j].isalpha():
#             count += 1
# print(f'Количество слов: {count}')

# Exercise №4
# lines = []
# with open('files_home_work_2/input.txt', 'r') as file:
#     with open('files_home_work_2/unique_output.txt', 'w') as new_file:
#         for line in file:
#             if line not in lines:
#                 lines.append(line)
#
#         for line in lines:
#             new_file.write(str(line))