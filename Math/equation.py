from Math.matrix import Matrix

from decimal import Decimal

import math
import sympy as sp

from sympy.abc import x, y, z, t, I
class Equation:
    def __init__(self, equation: str):
        equation = equation.replace("-", "+-").replace("=+-", "=-")
        if equation[0] == "+":
            equation = equation[1:]
        for i in "qwertyuiopasdfghjklzxcvbnm":
            equation = equation.replace(i, "")
        self.result = sp.S(equation.split("=")[-1])
        self.nomials = list(map(sp.S, equation.split("=")[0].split("+")))
        
    def linear(self):
        """
        Calculates root of linear equation
        
        Args:
        None
        
        Return: Root of linear equation
        """
        return self.result - self.nomials[0]
    
    def square(self):
        """
        Calculates roots of square equation
        
        Args:
        None
        
        Return: Roots of square equation
        """
        return sp.solve(self.nomials[0] * x ** 2 + self.nomials[1] * x - self.result)
        
    def symmetric3(self):
        """
        Calculates roots of symmetric cubic equation

        Args:
        None
        
        Return: Roots of symmetric cubic equation
        """
        result = [-1, *Equation(f"{self.nomials[0]}+{self.nomials[0]-self.nomials[1]}={-self.nomials[0]}".replace("+-", "-")).square()]
        return result
    
    def symmetric4(self):
        """
        Calculates roots of symmetric equation of fourth degree

        Args:
        None
        
        Return: Roots of symmetric equation of fourth degree
        """
        t1, t2 = Equation(f"{self.nomials[0]}+{self.nomials[1]}={-(self.nomials[2] - 2 * self.nomials[0])}".replace("+-", "-")).square()
        result = [*Equation(f"1-{t1}=-1".replace("--", "+")).square(), *Equation(f"1-{t2}=-1".replace("--", "+")).square()]
        return result
    
    def symmetric(self):
        """
        Calculates roots of symmetric equation of third or fourth degree

        Args:
        None
        
        Return: Roots of symmetric equation of third or fourth degree
        """
        if len(self.nomials) == 3:
            return self.symmetric3()
        if len(self.nomials) == 4:
            return self.symmetric4()

    def Cardano(self):
        res = []
        a, b, c, d = self.nomials.copy()
        p, q = ((3 * a * c) - (b ** 2)) / (3 * (a ** 2)), ((2 * (b ** 3)) - (9 * a * b * c) + (27 * (a ** 2) * d)) / (27 * (a ** 3))
        D = ((q / 2) ** 2) + ((p / 3) ** 3)
        if D < 0:
            if q < 0:
                fi = sp.atan(sp.root(-D, 2, 0))
            elif q == 0:
                fi = sp.pi / 2
            else:
                fi = sp.atan(sp.root(-D, 2, 0)) + sp.pi
            res.append(2 * sp.sqrt((-p)/3) * sp.cos(fi / 3) - (b / (3 * a)))
            res.append(2 * sp.sqrt((-p)/3) * sp.cos(fi / 3 + (2 * sp.pi) / 3) - (b / (3 * a)))
            res.append(2 * sp.sqrt((-p)/3) * sp.cos(fi / 3 + (4 * sp.pi) / 3) - (b / (3 * a)))
            res.sort()
        elif D > 0:
            y1 = sp.real_root((-q) / 2 + sp.sqrt(D), 3) + sp.real_root((-q) / 2 - sp.sqrt(D), 3)
            res.append(y1 - (b / (3 * a)))
            yd = I * (sp.re(3) / 2) * (sp.real_root((-q) / 2 + sp.sqrt(D), 3) - sp.real_root((-q) / 2 - sp.sqrt(D), 3))
            y2, y3 = ((-1) / 2) * y1 - (b / (3 * a)) + yd, ((-1) / 2) * y1 - (b / (3 * a)) - yd
            res.append(y2)
            res.append(y3)
        else:
            if q == 0 and p == 0:
                res.append(-(b / (3 * a)))
            else:
                res.append((2 * (sp.real_root(-q / 2 , 3)) - (b / (3 * a))))
                res.append((-(sp.real_root(-q / 2 , 3)) - (b / (3 * a))))
        print(sp.solve(a * x ** 3 + b * x ** 2 + c * x + d))
        return list(map(str, res))

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
    letters = sp.symbols("x y z t")
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
    
    