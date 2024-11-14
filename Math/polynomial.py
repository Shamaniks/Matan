from decimal import Decimal
import sympy as sp
from sympy import I
class Polynomial:
    def __init__(self, coefficients: list) -> None:
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        
    def __str__(self) -> str:
        output = ""
        for i in range(self.degree + 1, 0, -1):
            i -= 1
            if self.coefficients[::-1][i] == 1:
                if i == 0: output += " + 1"
                elif i == 1: output += " + x"
                else: output += f" + x^{i}"
            elif self.coefficients[::-1][i] == -1:
                if i == 0: output += " - 1"
                elif i == 1: output += " - x"
                else: output += f" - x^{i}"
            elif self.coefficients[::-1][i] != 0 and self.coefficients[::-1][i] % 1 == 0:
                if i == 0: output += f" + {self.coefficients[::-1][i]}"
                elif i == 1: output += f" + {self.coefficients[::-1][i]}*x"
                else: output += f" + {self.coefficients[::-1][i]}*x^{i}"
        return f"({output[3:]})".replace(" + -", " - ")
    
    def __getitem__(self, index):
        return self.coefficients[index]
    
    def __mod__(self, other):
        return sp.simplify(str(self).replace("x", f"({-other[-1]})"))
    
    def __truediv__(self, other):
        result = Polynomial(self.coefficients.copy())
        result = result.Gorner(-other[-1])
        return [other, result, self % other]
    
    def Gorner(self, a):
        """
        Divides polynomial using the Gorner's method

        Args:
        a: The divider
        
        Return:
        None
        """
        result = [self[0]]
        for i in range(1, len(self.coefficients)):
            result.append(a * result[i - 1] + self[i])
        return Polynomial(result[:-1])
    
    def factorio(self) -> list:
        """
        Factorises polynomial and prints the result
        
        Args:
        polyNoimal (list): The coefficients of the polynomial to factorise
        
        Return:
        None
        """
        if self[-1] == 0:
            return ["Я хз что тут делать"]
        dividersQ, dividersP = [], []
        result = []
        poly = Polynomial(self.coefficients.copy())
        for i in range(round(-abs(self[0]) ** 0.5) - 1, round(abs(self[0]) ** 0.5) + 2):
            if i != 0 and self[0] % i == 0:
                dividersQ.append(i)
        for i in range(round(-abs(self[-1]) ** 0.5) - 1, round(abs(self[-1]) ** 0.5) + 2):
            if i != 0 and self[-1] % i == 0:
                dividersP.append(i)
        for i in range(self.degree):
            for p in dividersP:
                for q in dividersQ:
                    a = sp.S(f"{p}/{q}")
                    if poly % Polynomial([1, -a]) == 0:
                        result.append(Polynomial([1, -a]))
                        poly = poly.Gorner(a)
                        if poly.degree == 1:
                            result.append(poly)
                            return result
        result.append(poly)
        return result
                        
        
    
    def linear(self):
        """
        Calculates root of linear equation
        
        Args:
        None
        
        Return: Root of linear equation
        """
        return -self[1] - self[0]

    def square(self):
        """
        Calculates roots of square equation
        
        Args:
        None
        
        Return: Roots of square equation
        """
        a, b, c = self.coefficients
        b, c = b / a, c / a
        D = sp.sqrt(b ** 2 - 4 * c)
        return [(-b - D) / 2, (-b + D) / 2]
    
    def symmetric(self):
        """
        Calculates roots of symmetric equation of third or fourth degree

        Args:
        None
        
        Return: Roots of symmetric equation
        """
        if self.degree == 3:
            return [-1, *Polynomial(f"{self[0]}+{self[0]-self[1]}+{self[0]}=0".replace("+-", "-")).square()]
        if self.degree == 4:
            t1, t2 = Polynomial(f"{self[0]}+{self[1]}+{self[2] - 2 * self[0]}=0".replace("+-", "-")).square()
            return [*Polynomial(f"1-{t1}+1=0".replace("--", "+")).square(), *Polynomial(f"1-{t2}+1=0".replace("--", "+")).square()]
    
    def Cardano(self):
        """
        Calculates roots of cubic equation
        
        Args:
        None
        
        Return: roots of cubic equation    
        """
        a, b, c, d = self.coefficients.copy()
        p = c - b ** 2 / (3 * a)
        q = d - (b * c) / (3 * a) + (2 * b ** 3) / (27 * a ** 2)
        D = (q / 2) ** 2 + (p / 3) ** 3
        r = b / (3 * a)
        print(sp.solve(str(self)))
        if D > 0:
            u, v = sp.cbrt(-q / 2 + sp.sqrt(D)), sp.cbrt(-q / 2 - sp.sqrt(D))
            return [
                u + v - r,
                -((u + v) / 2) + (u - v) * (sp.sqrt(3) * sp.I / 2) - r,
                -((u + v) / 2) - (u - v) * (sp.sqrt(3) * sp.I / 2) - r
                ]
        elif D == 0:
            return [
                2 * sp.cbrt(-q / 2) - r,
                sp.real_root(-(-q / 2), 3) - r
            ]
        elif D < 0:
            theta = sp.acos(-q / (2 * sp.sqrt((-p / 3) ** 3)))
            return [
                2 * sp.sqrt(-p / 3) * sp.cos(theta / 3) - r,
                2 * sp.sqrt(-p / 3) * sp.cos((theta + 2 * sp.pi) / 3) - r,
                2 * sp.sqrt(-p / 3) * sp.cos((theta + 4 * sp.pi) / 3) - r 
            ]
    
    def Ferrari(self):
        """
        Calculates roots of quartic equation
        
        Args:
        None
        
        Return: Roots of quartic equation
        """
        a, b, c, d, e = self.coefficients.copy()
        b, c, d, e = b / a, c / a, d / a, e / a
        p = (8 * c - 3 * b ** 2) / 8
        q = b ** 3 / 8 - (b * c) / 2 + d
        r = -(3 * b ** 4 / 256) - b * c ** 2 / 16 - b * d / 4 + e
    def solve(self):
        """
        Calculates roots of different equations

        Args:
        None
        
        Return: Roots of equation
        """
        if self.degree == 1:
            return self.linear()
        elif self.degree == 2:
            return self.square()
        elif self.degree == 3:
            if self[0] == self[3] and self[1] == self[2]:
                return self.symmetric3()
            return self.Cardano()
        elif self.degree == 4:
            if self[0] == self[4] and self[1] == self[3]:
                return self.symmetric4()
            return self.Ferrari()
        
def parseFromString(string: str) -> list:
    return list(map(sp.S, string.replace("-", "+-").split("+")))
    