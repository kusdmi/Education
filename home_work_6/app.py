from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import operator

app = FastAPI(title="Calculator API")


# Модели данных
class BinaryOperation(BaseModel):
    a: float
    op: str
    b: float


class ExpressionRequest(BaseModel):
    expression: str


# Текущее состояние выражения
current_expression = []

# Словарь операторов
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


def parse_expression(expression: str) -> float:
    """Парсинг и вычисление математического выражения"""

    def apply_operation(ops, values):
        op = ops.pop()
        right = values.pop()
        left = values.pop()
        values.append(operators[op](left, right))

    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    # Удаляем пробелы
    expression = expression.replace(' ', '')

    ops = []
    values = []
    i = 0

    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            values.append(float(expression[i:j]))
            i = j
        elif expression[i] == '(':
            ops.append(expression[i])
            i += 1
        elif expression[i] == ')':
            while ops and ops[-1] != '(':
                apply_operation(ops, values)
            ops.pop()  # Удаляем '('
            i += 1
        else:
            while (ops and ops[-1] != '(' and
                   precedence(ops[-1]) >= precedence(expression[i])):
                apply_operation(ops, values)
            ops.append(expression[i])
            i += 1

    while ops:
        apply_operation(ops, values)

    return values[0] if values else 0


# Базовые арифметические операции
@app.post("/add")
async def add(a: float, b: float):
    result = a + b
    current_expression.append(f"({a} + {b})")
    return {"result": result}


@app.post("/subtract")
async def subtract(a: float, b: float):
    result = a - b
    current_expression.append(f"({a} - {b})")
    return {"result": result}


@app.post("/multiply")
async def multiply(a: float, b: float):
    result = a * b
    current_expression.append(f"({a} * {b})")
    return {"result": result}


@app.post("/divide")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    result = a / b
    current_expression.append(f"({a} / {b})")
    return {"result": result}


# Метод для добавления бинарной операции
@app.post("/binary-operation")
async def binary_operation(operation: BinaryOperation):
    if operation.op not in operators:
        raise HTTPException(status_code=400, detail="Invalid operator")

    try:
        result = operators[operation.op](operation.a, operation.b)
        current_expression.append(f"({operation.a} {operation.op} {operation.b})")
        return {"result": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")


# Метод для вычисления сложного выражения из строки
@app.post("/evaluate-expression")
async def evaluate_expression(request: ExpressionRequest):
    try:
        result = parse_expression(request.expression)
        current_expression.append(f"({request.expression})")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error evaluating expression: {str(e)}")


# Просмотр текущего выражения
@app.get("/current-expression")
async def get_current_expression():
    if not current_expression:
        return {"expression": "No expression defined"}

    full_expression = " + ".join(current_expression)
    return {"expression": full_expression}


# Выполнение текущего выражения
@app.post("/execute")
async def execute_expression():
    if not current_expression:
        raise HTTPException(status_code=400, detail="No expression to execute")

    try:
        full_expression = " + ".join(current_expression)
        result = parse_expression(full_expression)

        # Очищаем текущее выражение после выполнения
        current_expression.clear()

        return {"result": result, "expression": full_expression}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing expression: {str(e)}")


# Очистка текущего выражения
@app.delete("/clear")
async def clear_expression():
    current_expression.clear()
    return {"message": "Expression cleared"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)