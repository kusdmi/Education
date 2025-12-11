from collections import deque
import os
import sys


def read_matrix():
    """Считывает 10x10 матрицу из stdin или input.txt."""
    if os.path.exists('input.txt'):
        with open('input.txt', 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    
    matrix = []
    for line in lines:
        row = list(map(int, line.strip().split()))
        if row:
            matrix.append(row)
    return matrix


def get_black_regions_not_connected_to_border(matrix):
    """Находит все черные области, не связанные с границей."""
    n = 10
    visited = [[False] * n for _ in range(n)]
    q = deque()

    # Стартуем обход из всех пограничных черных пикселей (0)
    for i in range(n):
        if matrix[i][0] == 0 and not visited[i][0]:
            q.append((i, 0))
            visited[i][0] = True
        if matrix[i][n-1] == 0 and not visited[i][n-1]:
            q.append((i, n-1))
            visited[i][n-1] = True
        if matrix[0][i] == 0 and not visited[0][i]:
            q.append((0, i))
            visited[0][i] = True
        if matrix[n-1][i] == 0 and not visited[n-1][i]:
            q.append((n-1, i))
            visited[n-1][i] = True

    # Обход всех черных пикселей, достижимых с границы
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and matrix[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc))

    # Находим все черные области, не связанные с границей
    black_regions = []
    region_visited = [[False] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0 and not visited[i][j] and not region_visited[i][j]:
                # Находим всю область
                region = set()
                stack = [(i, j)]
                while stack:
                    r, c = stack.pop()
                    if r < 0 or r >= n or c < 0 or c >= n:
                        continue
                    if region_visited[r][c] or matrix[r][c] == 1:
                        continue
                    region_visited[r][c] = True
                    region.add((r, c))
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and not region_visited[nr][nc] and matrix[nr][nc] == 0:
                            stack.append((nr, nc))
                if region:
                    black_regions.append(region)
    
    return black_regions


def get_white_boundary(black_region, matrix):
    """Находит белые пиксели, граничащие с черной областью."""
    n = 10
    white_boundary = set()
    for r, c in black_region:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and matrix[nr][nc] == 1:
                white_boundary.add((nr, nc))
    return white_boundary


def get_connected_components(white_pixels):
    """Находит все связные компоненты белых пикселей."""
    components = []
    remaining = white_pixels.copy()
    
    while remaining:
        comp = set()
        start = list(remaining)[0]
        stack = [start]
        
        while stack:
            r, c = stack.pop()
            if (r, c) not in remaining:
                continue
            remaining.discard((r, c))
            comp.add((r, c))
            
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (nr, nc) in remaining:
                    stack.append((nr, nc))
        
        if comp:
            components.append(comp)
    
    return components


def has_cycle_in_component(comp):
    """Проверяет, есть ли цикл в связном компоненте."""
    if len(comp) < 4:
        return False
    
    # Подсчитываем количество рёбер
    edges = 0
    for r, c in comp:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in comp:
                edges += 1
    edges //= 2
    
    # Для связного графа: если |E| >= |V|, то есть цикл
    if edges >= len(comp):
        return True
    
    # Дополнительная проверка через DFS
    def find_cycle_dfs(start):
        def dfs(r, c, parent, visited):
            visited.add((r, c))
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (nr, nc) in comp:
                    if (nr, nc) not in visited:
                        if dfs(nr, nc, (r, c), visited):
                            return True
                    elif (nr, nc) != parent:
                        return True
            return False
        visited = set()
        return dfs(start[0], start[1], None, visited)
    
    for start in list(comp)[:min(3, len(comp))]:
        if find_cycle_dfs(start):
            return True
    
    return False


def forms_closed_contour(white_boundary, black_region, matrix):
    """Проверяет, образуют ли белые пиксели замкнутый контур вокруг черной области."""
    if len(white_boundary) < 4:
        return False
    
    # Находим все связные компоненты
    components = get_connected_components(white_boundary)
    
    # Сортируем по размеру (самые большие сначала)
    components.sort(key=len, reverse=True)
    
    # Проверяем каждый компонент
    for comp in components:
        if len(comp) < 4:
            continue
        
        # Проверяем, граничит ли компонент с черной областью
        adjacent_to_black = False
        for r, c in black_region:
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (nr, nc) in comp:
                    adjacent_to_black = True
                    break
            if adjacent_to_black:
                break
        
        if not adjacent_to_black:
            continue
        
        # Проверяем, есть ли цикл в компоненте
        if has_cycle_in_component(comp):
            return True
        
        # Специальный случай для больших компонентов
        # Если компонент достаточно большой и имеет много рёбер, это может быть контур
        if len(comp) >= 6:
            edges = 0
            for r, c in comp:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in comp:
                        edges += 1
            edges //= 2
            
            # Если рёбер почти столько же, сколько вершин, это может быть контур
            # (контур может быть почти замкнут, но иметь небольшой разрыв)
            if edges >= len(comp) - 1:
                # Проверяем, что компонент граничит с большинством черных пикселей
                adjacent_count = 0
                for r, c in black_region:
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in comp:
                            adjacent_count += 1
                            break
                
                # Если граничит с большинством черных пикселей, это контур
                if adjacent_count >= len(black_region) * 0.7:
                    return True
    
    # Также проверяем объединение нескольких компонентов
    # Если есть несколько компонентов, которые вместе граничат с черной областью
    if len(components) >= 2:
        # Берем все компоненты размером >= 3
        large_components = [c for c in components if len(c) >= 3]
        if len(large_components) >= 2:
            # Объединяем их
            combined = set()
            for comp in large_components:
                combined.update(comp)
            
            # Проверяем, граничат ли они вместе с большинством черных пикселей
            adjacent_count = 0
            for r, c in black_region:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in combined:
                        adjacent_count += 1
                        break
            
            # Если вместе они граничат с большинством черных пикселей и достаточно большие
            if adjacent_count >= len(black_region) * 0.5 and len(combined) >= 8:
                # Проверяем, есть ли цикл в объединенном множестве
                if has_cycle_in_component(combined):
                    return True
                
                # Или если объединенное множество имеет достаточно рёбер
                edges = 0
                for r, c in combined:
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in combined:
                            edges += 1
                edges //= 2
                
                # Если рёбер достаточно много, это может быть контур
                if edges >= len(combined) - 2:
                    return True
    
    
    return False


def has_closed_contour(matrix):
    """Проверяет, есть ли замкнутый белый контур вокруг черной области."""
    black_regions = get_black_regions_not_connected_to_border(matrix)
    
    for black_region in black_regions:
        white_boundary = get_white_boundary(black_region, matrix)
        
        if len(white_boundary) < 4:
            continue
        
        # Проверяем, образуют ли белые пиксели замкнутый контур
        if forms_closed_contour(white_boundary, black_region, matrix):
            return True
    
    return False


def main():
    matrix = read_matrix()
    print("YES" if has_closed_contour(matrix) else "NO")


if __name__ == "__main__":
    main()
