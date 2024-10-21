from decimal import Decimal

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
                elif i == 1: output += f" + {self.coefficients[::-1][i]}x"
                else: output += f" + {self.coefficients[::-1][i]}x^{i}"
        return f"({output[3:]})".replace(" + -", " - ")
    
    def __getitem__(self, index):
        return self.coefficients[index]
    
    def __truediv__(self, other):
        """
        Divide two polynomials represented as lists of coefficients.

        Args:
        dividend (list): The coefficients of the dividend polynomial.
        divider (list): The coefficients of the divider polynomial.

        Returns:
        list: The coefficients of the result polynomial.
        """
        result, dividend = [], self.coefficients.copy()
        for i in range(self.degree):
            result.append(dividend[i] / other.coefficients[0])
            dividend[i + 1] -= result[i] * other.coefficients[1]
        result.append(dividend[-1] / other.coefficients[0])
        return f"{other}{Polynomial(result[:-1])} + {str(result[-1])}".replace(" + 0", "").replace(" + -", " - ")
    
    def Gorner(self, a: Decimal):
        """
        Divides polynomial using the Gorner's method

        Args:
        polyNomial (list): The coefficients of the polynomial to divide
        
        Return:
        None
        """
        result = [self.coefficients[0]]
        for i in range(1, self.degree + 1):
            result.append(a * result[i - 1] + self.coefficients[i])
        return f"{Polynomial([1, -a])}{Polynomial(result[:-1])} + {str(result[-1])}".replace(" + 0", "").replace(" + -", " - ")
    
    def factorio(self) -> list:
        """
        Factorises polynomial and prints the result
        
        Args:
        polyNoimal (list): The coefficients of the polynomial to factorise
        
        Return:
        None
        """
        a, b = self.coefficients[0], self.coefficients[-1]
        if a < 0 or b < 0:
            return "Комплексные числа"
        divident = Polynomial(self.coefficients.copy())
        dividersA, dividersB = [], []
        result = []
        for i in range(1, int(round(Decimal(a) ** Decimal(0.5), 0)) + 1):
            if a % Decimal(i) == 0:
                dividersA.append(i)
        for i in range(1, int(round(Decimal(b) ** Decimal(0.5), 0)) + 1):
            if b % Decimal(i) == 0:
                dividersB.append(Decimal(i))
        dividersA += list(map(lambda x: -x, dividersA.copy()))
        dividersB += list(map(lambda x: -x, dividersB.copy()))
        for q, p in dividersA, dividersB:
            shorter = divident.Gorner(p/q)
            if divident.degree == 2:
                result.append(divident)
                break
            else:
                result.append(Polynomial([1, p/q]))
                divident = shorter
        if len(result) < self.degree:
            result.append(divident)
        elif len(result) > self.degree:
            print("Я без понятия как это вышло")
        result = "".join(map(str, result))
        return result
    
def parseFromString(string: str) -> list:
    return list(map(Decimal, string.replace("-", "+-").split("+")))
    