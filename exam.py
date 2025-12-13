import sys
import math


class MinHeap:
    """
    Реализация минимальной кучи (min-heap) для использования в алгоритме Дейкстры.
    Обеспечивает операции добавления элемента и извлечения минимального за O(log n).
    """

    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] >= self.heap[parent][0]:
                break
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest

    def __len__(self):
        return len(self.heap)

    def empty(self):
        return len(self.heap) == 0


class RouteOptimizer:
    """
    Класс для оптимизации маршрутов по нескольким критериям.
    Обрабатывает города, дороги и запросы на поиск маршрутов.
    Реализует алгоритм Дейкстры для каждого критерия отдельно.
    Использует собственную реализацию кучи для ускорения работы с большими объемами данных.
    """

    def __init__(self):
        """
        Инициализация оптимизатора маршрутов.
        Создает структуры для хранения данных о городах и дорогах.
        Все графы инициализируются для всех городов, даже если у них нет дорог.
        """
        self.cities = {}
        self.city_names = {}
        self.graph_length = {}
        self.graph_time = {}
        self.graph_cost = {}
        self.requests = []

    def read_input(self, filename):
        """
        Чтение входных данных из файла.
        Разбирает секции CITIES, ROADS и REQUESTS.
        Обрабатывает возможные ошибки формата входных данных.
        filename: Имя входного файла
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            sys.exit(1)

        section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line == "[CITIES]":
                section = "CITIES"
            elif line == "[ROADS]":
                section = "ROADS"
            elif line == "[REQUESTS]":
                section = "REQUESTS"
            elif section == "CITIES":
                self._parse_city(line)
            elif section == "ROADS":
                self._parse_road(line)
            elif section == "REQUESTS":
                self._parse_request(line)

    def _parse_city(self, line):
        """
        Парсинг строки с информацией о городе.
        Формат: "ID: Название_города"
        Инициализирует графы для каждого города сразу при его добавлении.
        line: Строка с данными о городе
        """
        parts = line.split(':', 1)
        if len(parts) != 2:
            return

        try:
            city_id = int(parts[0].strip())
            city_name = parts[1].strip()
            self.cities[city_name] = city_id
            self.city_names[city_id] = city_name

            if city_id not in self.graph_length:
                self.graph_length[city_id] = {}
                self.graph_time[city_id] = {}
                self.graph_cost[city_id] = {}
        except ValueError:
            return

    def _parse_road(self, line):
        """
        Парсинг строки с информацией о дороге.
        Формат: "ID1 - ID2: длина(км), время(мин), Стоимость(руб)"
        Корректно обрабатывает пробелы вокруг дефиса.
        line: Строка с данными о дороге
        """
        if ':' not in line:
            return

        cities_part, params_part = line.split(':', 1)
        cities_part = cities_part.strip()
        params_part = params_part.strip()

        if '-' not in cities_part:
            return

        try:
            city1_str, city2_str = [part.strip() for part in cities_part.split('-')]
            city1 = int(city1_str)
            city2 = int(city2_str)
        except ValueError:
            return

        params = [p.strip() for p in params_part.split(',')]
        if len(params) != 3:
            return

        try:
            length = int(params[0])
            time = int(params[1])
            cost = int(params[2])
        except ValueError:
            return

        if city1 not in self.graph_length:
            self.graph_length[city1] = {}
            self.graph_time[city1] = {}
            self.graph_cost[city1] = {}
        if city2 not in self.graph_length:
            self.graph_length[city2] = {}
            self.graph_time[city2] = {}
            self.graph_cost[city2] = {}

        self.graph_length[city1][city2] = length
        self.graph_length[city2][city1] = length
        self.graph_time[city1][city2] = time
        self.graph_time[city2][city1] = time
        self.graph_cost[city1][city2] = cost
        self.graph_cost[city2][city1] = cost

    def _parse_request(self, line):
        """
        Парсинг строки с запросом на маршрут.
        Формат: "Город_отправления -> Город_назначения | Приоритеты (Д,В,С)"
        line: Строка с запросом
        """
        if '|' not in line:
            return

        route_part, priority_part = line.split('|', 1)
        route_part = route_part.strip()
        priority_part = priority_part.strip()

        if '->' not in route_part:
            return

        try:
            from_city, to_city = [c.strip() for c in route_part.split('->')]

            priorities = []
            if priority_part.startswith('(') and priority_part.endswith(')'):
                priority_str = priority_part[1:-1]
                priorities = [p.strip() for p in priority_str.split(',')]

            self.requests.append({
                'from': from_city,
                'to': to_city,
                'priorities': priorities
            })
        except (ValueError, IndexError):
            return

    def dijkstra(self, start_id, end_id, graph):
        """
        Реализация алгоритма Дейкстры для поиска кратчайшего пути
        в графе с неотрицательными весами.
        Использует собственную реализацию кучи MinHeap для эффективности O(E log V).
        start_id: ID города отправления
        end_id: ID города назначения
        graph: Граф в виде словаря смежности с весами
        Return: Кортеж (кратчайшее расстояние, список ID городов пути)
        """
        if start_id not in graph or end_id not in graph:
            return math.inf, []

        distances = {node: math.inf for node in graph}
        previous = {node: None for node in graph}
        distances[start_id] = 0

        heap = MinHeap()
        heap.push((0, start_id))

        while not heap.empty():
            current_distance, current = heap.pop()

            if current_distance > distances[current]:
                continue

            if current == end_id:
                break

            for neighbor, weight in graph[current].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heap.push((distance, neighbor))

        if distances[end_id] == math.inf:
            return math.inf, []

        path = []
        current = end_id
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return distances[end_id], path

    def calculate_route_metrics(self, path):
        """
        Вычисление метрик маршрута (длина, время, стоимость)
        на основе найденного пути.
        Проверяет существование дорог между всеми соседними городами в пути.
        path: Список ID городов в маршруте
        Returns: Словарь с метриками маршрута или None если путь некорректен
        """
        total_length = 0
        total_time = 0
        total_cost = 0

        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]

            if (city2 not in self.graph_length.get(city1, {}) or
                    city2 not in self.graph_time.get(city1, {}) or
                    city2 not in self.graph_cost.get(city1, {})):
                return None

            total_length += self.graph_length[city1][city2]
            total_time += self.graph_time[city1][city2]
            total_cost += self.graph_cost[city1][city2]

        return {
            'length': total_length,
            'time': total_time,
            'cost': total_cost
        }

    def find_optimal_routes(self, request):
        """
        Поиск оптимальных маршрутов по трем критериям:
        длина, время и стоимость.
        Возвращает None если города не существуют или пути не найдены.
        request: Словарь с данными запроса
        Return: Словарь с оптимальными маршрутами по каждому критерию
        """
        from_city = request['from']
        to_city = request['to']

        if from_city not in self.cities or to_city not in self.cities:
            return None

        start_id = self.cities[from_city]
        end_id = self.cities[to_city]

        routes = {}

        length_dist, length_path = self.dijkstra(start_id, end_id, self.graph_length)
        if length_path:
            metrics = self.calculate_route_metrics(length_path)
            if metrics:
                routes['Д'] = {
                    'path': length_path,
                    'metrics': metrics
                }

        time_dist, time_path = self.dijkstra(start_id, end_id, self.graph_time)
        if time_path:
            metrics = self.calculate_route_metrics(time_path)
            if metrics:
                routes['В'] = {
                    'path': time_path,
                    'metrics': metrics
                }

        cost_dist, cost_path = self.dijkstra(start_id, end_id, self.graph_cost)
        if cost_path:
            metrics = self.calculate_route_metrics(cost_path)
            if metrics:
                routes['С'] = {
                    'path': cost_path,
                    'metrics': metrics
                }

        return routes if routes else None

    def find_compromise_route(self, routes, priorities):
        """
        Выбор компромиссного маршрута на основе заданных приоритетов.
        Сравнивает маршруты по критериям в порядке их приоритета.
        Возвращает None если нет доступных маршрутов.
        routes: Словарь с оптимальными маршрутами по критериям
        priorities: Список приоритетов в порядке убывания важности
        Return: Выбранный компромиссный маршрут
        """
        if not routes:
            return None

        available_routes = [(criterion, routes[criterion]) for criterion in routes]

        if not available_routes:
            return None

        def route_comparator(route_tuple):
            """
            Функция сравнения маршрутов по приоритетам.
            Возвращает кортеж значений критериев в порядке приоритетов.
            """
            criterion, route = route_tuple
            metrics = route['metrics']

            priority_values = []
            for priority in priorities:
                if priority == 'Д':
                    priority_values.append(metrics['length'])
                elif priority == 'В':
                    priority_values.append(metrics['time'])
                elif priority == 'С':
                    priority_values.append(metrics['cost'])
                else:
                    priority_values.append(math.inf)

            return tuple(priority_values)

        best_route = min(available_routes, key=route_comparator)
        return best_route[1]

    def format_route(self, criterion, route, from_city, to_city):
        """
        Форматирование маршрута для вывода в файл.
        Преобразует путь из ID городов в названия.
        criterion: Критерий оптимизации
        route: Данные маршрута
        from_city: Название города отправления
        to_city: Название города назначения
        Return: Отформатированная строка маршрута
        """
        if not route:
            return None

        criterion_names = {
            'Д': 'ДЛИНА',
            'В': 'ВРЕМЯ',
            'С': 'СТОИМОСТЬ'
        }

        path_names = [self.city_names[city_id] for city_id in route['path']]
        metrics = route['metrics']

        return (f"{criterion_names[criterion]}: {' -> '.join(path_names)} | "
                f"Д={metrics['length']}, В={metrics['time']}, С={metrics['cost']}")

    def process_requests(self):
        """
        Основной метод обработки всех запросов.
        Для каждого запроса находит оптимальные маршруты
        и выбирает компромиссный вариант.
        Обрабатывает случаи когда маршруты не найдены.
        Return: Список строк для записи в выходной файл
        """
        results = []

        for request in self.requests:
            from_city = request['from']
            to_city = request['to']
            priorities = request['priorities']

            routes = self.find_optimal_routes(request)

            if not routes:
                results.append(f"Маршрут {from_city} -> {to_city} не найден")
                results.append('')
                continue

            compromise_route = self.find_compromise_route(routes, priorities)

            for criterion in ['Д', 'В', 'С']:
                if criterion in routes:
                    route_str = self.format_route(
                        criterion, routes[criterion], from_city, to_city
                    )
                    results.append(route_str)

            if compromise_route:
                path_names = [self.city_names[city_id]
                              for city_id in compromise_route['path']]
                metrics = compromise_route['metrics']
                compromise_str = (f"КОМПРОМИСС: {' -> '.join(path_names)} | "
                                  f"Д={metrics['length']}, В={metrics['time']}, "
                                  f"С={metrics['cost']}")
                results.append(compromise_str)
            else:
                results.append(f"Компромиссный маршрут {from_city} -> {to_city} не найден")

            results.append('')

        return results

    def write_output(self, filename, results):
        """
        Запись результатов в выходной файл.
        filename: Имя выходного файла
        results: Список строк для записи
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for result in results:
                if result:
                    file.write(result + '\n')


def main():
    optimizer = RouteOptimizer()
    optimizer.read_input('input.txt')
    results = optimizer.process_requests()
    optimizer.write_output('output.txt', results)


if __name__ == "__main__":
    main()