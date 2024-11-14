from Math.matrix import Matrix

import sympy as sp

class Equation:
    def __init__(self, equation: str):
        equation = equation.replace("-", "+-").replace("=+-", "=-")
        if equation[0] == "+":
            equation = equation[1:]
        self.result = sp.S(equation.split("=")[-1])
        self.nomials = list(map(sp.S, equation.split("=")[0].split("+")))
    

def parseToMatrix(equations: list):
    """
    Parses equations system to matrix
    
    Args:
    equations (list): list of equations in system
    
    Return: [0] - matrix of coefficients of system, [1] - matrix of results of system
    """
    nomials = []
    results = []
    for equation in equations:
        equation = Equation(equation)
        nomials.append(equation.nomials)
        results.append(equation.result)
    return [nomials, results]


def Cramer(equations: list):
    """
    Calculates roots of equations system by Cramer's method
    
    Args:
    equations (list): The SLAE to calculate
    
    Return: The list of roots of SLAE
    """
    nomials, results = parseToMatrix(equations)
    result = []
    D = Matrix(len(nomials[0]), len(nomials), nomials).determinant()
    if D == 0:
        return Gauss(equations)
    for i in range(len(equations)):
        result.append(sp.simplify(f"{Matrix(len(nomials[0]), len(nomials), nomials).replaceColumn(results, i).determinant()} / {D}"))
    return result


def inverseMatrix(equations: list):
    """
    Calculates roots of SLAE by inversed matrix method
    
    Args:
    equations (list): The SLAE to calculate
    
    Return: The list of roots of SLAE
    """
    nomials, results = parseToMatrix(equations)
    results = Matrix(1, len(results), [[res] for res in results])
    A = Matrix(len(nomials), len(nomials[0]), nomials).inverse() * results
    result = [i[0] for i in (A).data]
    return result


def Gauss(equations: list):
    """
    Calculates roots of SLAE by Gauss's method
    
    Args:
    equations (list): The SLAE to calculate
    
    Return:
    List: The list of roots of SLAE
    """
    nomials, results = parseToMatrix(equations)
    matrix = [row + [result] for row, result in zip(nomials, results)]
    matrix = Matrix(len(nomials) + 1, len(nomials), matrix).echelon()
    result = [0] * len(nomials)
    letters = sp.symbols("x y z t w")
    for i in range(len(matrix.data) - 1, -1, -1):
        if matrix.data[i][i] == 0 and matrix.data[i][-1] == 0:
            result[i] = letters[i]
        elif matrix.data[i][i] == 0:
            return  ["Система не имеет решений."]
        else:
            result[i] = matrix.data[i][-1]
            for j in range(i + 1, len(nomials)):
                result[i] -= matrix.data[i][j] * result[j]
    return result
    
    