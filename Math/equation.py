from Math.matrix import Matrix

import copy

class Equation:
    def __init__(self, equation: str):
        equation = equation.replace("-", "+-").replace("=+-", "=-")
        for i in "qwertyuiopasdfghjklzxcvbnm":
            equation = equation.replace(i, "")
        self.result = float(equation.split("=")[-1])
        self.nomials = list(map(float, equation.split("=")[0].split("+")))

def parseToMatrix(equations: list):
    nomials = []
    results = []
    for equation in equations:
        equation = Equation(equation)
        nomials.append(equation.nomials)
        results.append(equation.result)
    return [nomials, results]

def Cramer(equations: list):
    nomials, results = parseToMatrix(equations)
    result = []
    
    D = Matrix(len(nomials[0]), len(nomials), nomials).determinant()

    if D == 0:
        return "Основной определитель равен 0"

    for i in range(len(equations)):
        temp = Matrix(len(nomials[0]), len(nomials), nomials).replaceColumn(results, i)
        if round(temp.determinant() / D, 10) == temp.determinant() / D:
            result.append(temp.determinant() / D)
        else:
            result.append(f"{temp.determinant()}/{D}")
    return result

def inverseMatrix(equations: list):
    nomials, results = parseToMatrix(equations)
    results = Matrix(1, len(results), [[res] for res in results])
    A = Matrix(len(nomials), len(nomials[0]), nomials).inverse()

    return [round(i[0], 10) for i in (A * results).data]


def Gauss(equations: list):
    nomials, results = parseToMatrix(equations)
    height = len(nomials)
    for i in range(len(results)):
        nomials[i].append(results[i])

    def swapRows(nomials: list, results: list, j1: int, j2: int):
        nomials[j1], nomials[j2], results[j1], results[j2] = nomials[j2], nomials[j1], results[j2], results[j1]
    
    def divideRow(nomials: list, results: list, j: int, divider: float):
        nomials[j] = [a / divider for a in nomials[j]]
        results[j] /= divider
    
    def combineRows(nomials: list, results: list, j1: int, j2: int, weight: float):
        nomials[j1] = [(a + k * weight) for a, k in zip(nomials[j1], nomials[j2])]
        results[j1] += results[j2] * weight
    
    column = 0
    while (column < height):
        current_row = None
        for r in range(column, height):
            if current_row is None or abs(nomials[r][column]) > abs(nomials[current_row][column]):
                current_row = r
        if current_row is None:
            return "Решений нет"
        if current_row != column:
            swapRows(nomials, results, current_row, column)
        divideRow(nomials, results, column, nomials[column][column])
        for r in range(column + 1, height):
            combineRows(nomials, results, r, column, -nomials[r][column])
        column += 1
    X = [0 for i in results]
    for i in range(height - 1, -1, -1):
        X[i] = results[i] - sum(x * a for x, a in zip(X[(i + 1):], nomials[i][(i + 1):]))
    return list(map(lambda x: round(x, 10), X))