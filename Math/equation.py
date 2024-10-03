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
    data = []
    height = len(nomials)
    for i in range(height):
        temp = []
        for j in range(height):
            temp.append(nomials[i][j])
        temp.append(results[i])
        data.append(temp)
    res = Matrix(height + 1, height, data).stair()
    results = res.transpose().data[-1][::-1]
    res = res.data[::-1]
    result = [results[0]]
    for i in range(1, height):
        temp = res[i][:-1]
        for j in range(1, height):
            temp[j] *= results[j - 1]
        temp.append(-results[i])
        result.append(-sum(temp[1:]))
    return result[::-1]