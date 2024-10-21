from Math.matrix import Matrix

from decimal import Decimal
from fractions import Fraction
import math
class Equation:
    def __init__(self, equation: str):
        equation = equation.replace("-", "+-").replace("=+-", "=-")
        for i in "qwertyuiopasdfghjklzxcvbnm":
            equation = equation.replace(i, "")
        self.result = Decimal(equation.split("=")[-1])
        self.nomials = list(map(Decimal, equation.split("=")[0].split("+")))
        
    def linear(self):
        """
        Calculates root of linear equation
        
        Args:
        None
        
        Return:
        Decimal: root of linear equation
        """
        return self.result - self.nomials[0]
    
    def square(self):
        """
        Calculates roots of square equation
        
        Args:
        None
        
        Return:
        list: roots of square equation
        """
        D = self.nomials[1] ** 2 + 4 * self.nomials[0] * self.result
        if D >= 0:
            D **= Decimal(0.5)
            return  (-self.nomials[1] - D) / (2 * self.nomials[0]), (-self.nomials[1] + D) / (2 * self.nomials[0])
        else:
            return "Действительных корней нет"
        
    def symmetric3(self):
        """
        Calculates roots of symmetric cubic equation

        Args:
        None
        
        Return:
        list: roots of symmetric cubic equation
        """
        result = [-1, *Equation(f"{self.nomials[0]}+{self.nomials[0]-self.nomials[1]}={-self.nomials[0]}".replace("+-", "-")).square()]
        for i in range(len(result)):
            if result[i] % 1 != 0:
                frac = Fraction(result[i]).limit_denominator()
                result[i] = f"{frac.numerator}/{frac.denominator}"
        return result
    
    def symmetric4(self):
        """
        Calculates roots of symmetric equation of fourth degree

        Args:
        None
        
        Return:
        list: roots of symmetric equation of fourth degree
        """
        t1, t2 = Equation(f"{self.nomials[0]}+{self.nomials[1]}={-(self.nomials[2] - 2 * self.nomials[0])}".replace("+-", "-")).square()
        result = [*Equation(f"1-{t1}=-1".replace("--", "+")).square(), *Equation(f"1-{t2}=-1".replace("--", "+")).square()]
        for i in range(len(result)):
            result[i] = result[i].normalize()
            if result[i] % 1 != 0:
                frac = Fraction(result[i]).limit_denominator()
                result[i] = f"{frac.numerator}/{frac.denominator}"
        return result
    
    def symmetric(self):
        """
        Calculates roots of symmetric equation of third or fourth degree

        Args:
        None
        
        Return:
        list: roots of symmetric equation of third or fourth degree
        """
        if len(self.nomials) == 3:
            return self.symmetric3()
        if len(self.nomials) == 4:
            return self.symmetric4()

def parseToMatrix(equations: list):
    """
    Parses equations system to matrix
    
    Args:
    equations (list): list of equations in system
    Return:
    list:  [0] - matrix of coefficients of system, [1] - matrix of results of system
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
    Calculates roots of equations system by
    """
    nomials, results = parseToMatrix(equations)
    result = []
    
    D = Matrix(len(nomials[0]), len(nomials), nomials).determinant()

    if D == 0:
        return "Основной определитель равен 0"
    for i in range(len(equations)):
        temp = Matrix(len(nomials[0]), len(nomials), nomials).replaceColumn(results, i)
        if (temp.determinant() / D).normalize() % 1 != 0:
            frac = Fraction(temp.determinant() / D).limit_denominator()
            result.append(f"{frac.numerator}/{frac.denominator}")
        else:
            result.append(f"{int(temp.determinant()/D)}")
    return result

def inverseMatrix(equations: list):
    nomials, results = parseToMatrix(equations)
    results = Matrix(1, len(results), [[res] for res in results])
    A = Matrix(len(nomials), len(nomials[0]), nomials).inverse()

    result = [round(i[0], 10) for i in (A * results).data]
    for i in range(len(result)):
        result[i].normalize()
        if result[i] % 1 != 0:
            frac = Fraction(result[i]).limit_denominator()
            result[i] = f"{frac.numerator}/{frac.denominator}"
        else:
            result[i] = f"{int(result[i])}"
    return result

def Gauss(equations: list):
    nomials, results = parseToMatrix(equations)
    matrix = [row + [result] for row, result in zip(nomials, results)]
    matrix = Matrix(len(nomials) + 1, len(nomials), matrix).stair()
    result = matrix.transpose().data[-1]
    for i in range(len(result)):
        result[i].normalize()
        if result[i] % 1 != 0:
            frac = Fraction(result[i]).limit_denominator()
            result[i] = f"{frac.numerator}/{frac.denominator}"
        else:
            result[i] = f"{int(result[i])}"
    return result