from decimal import Decimal

from Math.matrix import Matrix
from Math.equation import *
from Math.polynomial import Polynomial, parseFromString
import mathParser

class Terminal:
    path: str = "Matan> "
    matrix: Matrix = None
    memory: dict = {}
    polynomial: Polynomial = None

    def output(self, output: str) -> None:
        """
        Prints the output string with indentation based on self.path
        
        Args:
        output (str): The string to be printed
        
        Return:
        None
        """
        print(" " * len(self.path) + f"{output}")

    def outputMatrix(self, matrix: Matrix) -> None:
        """
        Prints the matrix with indentation based on self.path and with indentation between columns
        
        Args:
        matrix (Matrix): The matrix to be printed
        
        Return:
        None
        """
        row = ""
        matrix = matrix.round()
        lens = []
        for i in matrix.transpose().data:
            lens.append(max(map(lambda x: len(str(x)), [j for j in i])))
        for i in range(matrix.height):
            for j in range(matrix.width):
                row += " " * (lens[j] - len(str(matrix.data[i][j])) + 1) + str(matrix.data[i][j])
            print(" " * (len(self.path) - lens[0]) + row)
            row = ""

    def changePath(self, newPath: str) -> None:
        """
        Changes the path of the terminal

        Args:
        newPath (str): The new path
        
        Return:
        None
        """
        self.path = "Matan/" + newPath + "> "

    def calculate(self, calculation: str, context: str):
        """
        Calculates the result of the calculation with variables and prints it

        Args:
        calculation (str): The calculation to be done
        context (str): The context for right calculation
        
        Return:
        Any
        """
        if context == "matrix":
            stack = []
            scalar = ""
            for i in calculation:
                if i in "1234567890./":
                    scalar += i
                if i in self.memory.keys():
                    if scalar:
                        stack.append(self.memory[i].mul(Decimal(eval(scalar))))
                        scalar = ""
                    else:
                        stack.append(self.memory[i])
                if i in "*+()":
                    stack.append(i)
        return mathParser.calc(mathParser.shuntingYard(stack))

    def division(self, dividend: list, divider: list) -> list:
        result, dividend = [], dividend.copy()
        for i in range(len(dividend) - 1):
            result.append(dividend[i] / divider[0])
            dividend[i + 1] -= result[i] * divider[1]
        result.append(dividend[-1] / divider[0])  # append the last result
        return result
                
    def divOutput(self, divident: list, divider: list = [], last: int = 0) -> str:
        """
        Prints a list of coefficients converted to a string representation of a polynomial.
        
        Args:
        dividend (list): The coefficients of the polynomial dividend.
        divider (list): The coefficients of the polynomial divider.
        last (int, optional): The last index to consider. Defaults to 0.
        
        Returns:
        result (str): The string form of polynomial
        """
        output = ""
        for i in range(len(divident) - 1, last, -1):
            if divident[::-1][i] == 1:
                if i == 1: output += " + 1"
                elif i == 2: output += " + x"
                else: output += f" + x^{i - 1}"
            elif divident[::-1][i] == -1:
                if i == 1: output += " - 1"
                elif i == 2: output += " - x"
                else: output += f" - x^{i - 1}"
            elif divident[::-1][i] != 1 and divident[::-1][i] != 0:
                if i == 1: output += f" + {divident[::-1][i]}"
                elif i == 2: output += f" + {divident[::-1][i]}x"
                else: output += f" + {divident[::-1][i]}x^{i - 1}"
        if divider:
            outDiv = ""
            for i in range(len(divider) - 1, -1, -1):
                if divider[::-1][i] == 1:
                    if i == 0: outDiv += " + 1"
                    elif i == 1: outDiv += " + x"
                    else: outDiv += f" + x^{i}"
                elif divider[::-1][i] == -1:
                    if i == 0: outDiv += " - 1"
                    elif i == 1: outDiv += " - x"
                    else: outDiv += f" - x^{i}"
                elif divider[::-1][i] != 1 and divider[::-1][i] != 0:
                    if i == 0: outDiv += f" + {divider[::-1][i]}"
                    elif i == 1: outDiv += f" + {divider[::-1][i]}x"
                    else: outDiv += f" + {divider[::-1][i]}x^{i}"
            return f"({outDiv[3:]})({output[3:]}) + {divident[-1]}".replace(" + -", " - ").replace(" + 0", "")
        else:
            return f"({output[3:]}) + {divident[-1]}".replace(" + 0", "")

    def factorio(self, polyNoimal: list) -> None:
        a, b = polyNoimal[0], polyNoimal[-1]
        dividersA, dividersB = [], []
        output = ""
        for i in range(1, int(round(a ** Decimal(0.5), 0)) + 2):
            if a % Decimal(i) == 0:
                dividersA.append(Decimal(i))
        for i in range(1, int(round(b ** Decimal(0.5), 0)) + 2):
            if b % Decimal(i) == 0:
                dividersB.append(Decimal(i))
        dividersA += list(map(lambda x: -x, dividersA.copy()))
        dividersB += list(map(lambda x: -x, dividersB.copy()))
        for q in dividersA:
            for p in dividersB:
                shorter = self.division(polyNoimal, [1, (p/q)])
                if len(polyNoimal) == 2:
                    if p/q % 1 != 0:
                        frac = Fraction(polyNoimal[1]).limit_denominator()
                        output += f"({polyNoimal[0]}x + {frac.numerator}{frac.denominator})".replace(" + -", " - ")
                    else:
                        output += f"({polyNoimal[0]}x + {polyNoimal[1]})".replace(" + -", " - ")
                    break
                if shorter[-1] == 0:
                    polyNoimal = shorter
                    if p/q % 1 != 0:
                        frac = Fraction(p/q).limit_denominator()
                        output += f"(x + {frac.numerator}{frac.denominator})".replace(" + -", " - ")
                    else:
                        output += f"(x + {p/q})".replace(" + -", " - ")
        if len(list(filter(lambda x: x != 0, polyNoimal.copy()))) <= 2:
            self.output(output) 
        else: 
            output += self.divOutput(polyNoimal)
            self.output(output)
    
    def Gorner(self, polyNomial: list, divider: Decimal) -> None:        
        result = [polyNomial[0]]
        for i in range(1, len(polyNomial)):
            result.append(divider * result[i - 1] + polyNomial[i])
        self.output(self.divOutput(result, [1, -divider], len(polyNomial) - len(result)))
        
    def mainLoop(self) -> None:
        """
        Loops through the main menu
        
        Args:
        None
        
        Return:
        None
        """
        while True:
            inp: list = input(self.path).split()
            if inp[0] == "stop":
                break

            if inp[0] == "exit":
                self.path = "Matan> "

            elif inp[0] == "remember":
                if self.path == "Matan/Matrix> ":
                    self.memory[inp[1]] = self.matrix
            
            elif inp[0] == "out":
                if type(self.memory[inp[1]]) == Matrix:
                    self.outputMatrix(self.memory[inp[1]])
                else:
                    self.output(self.memory[inp[1]])
            
            elif inp[0] == "set":
                if self.path == "Matan/Matrix> ":
                    self.matrix = self.memory[inp[1]]

            elif inp[0] == "matrix":
                if self.path == "Matan> ":
                    temp = []
                    width, height = int(inp[1]), int(inp[2])
                    for j in range(height):
                        temp.append(list(map(Decimal, inp[j * width + 3:j * width + width + 3])))
                    self.matrix = Matrix(width, height, temp)
                    self.changePath("Matrix")
                elif self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix)

            elif inp[0] == "minor":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.minor(int(inp[1]) - 1, int(inp[2]) - 1))

            elif inp[0] == "dt":
                if self.path == "Matan/Matrix> ":
                    self.output(self.matrix.determinant())

            elif inp[0] == "new":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    width, height = int(inp[1]), int(inp[2])
                    for j in range(height):
                        temp.append(list(map(Decimal, inp[j * width + 3:j * width + width + 3])))
                    self.matrix = Matrix(width, height, temp)

            elif inp[0] == "add":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    for j in range(height):
                        temp.append(list(map(Decimal, inp[j * self.matrix.width + 1:j * self.matrix.width + self.matrix.width + 1])))
                    self.outputMatrix(self.matrix + Matrix(self.matrix.width, self.matrix.height, temp))
                    if "-s" in inp:
                        self.matrix += Matrix(self.matrix.width, self.matrix.height, temp)

            elif inp[0] == "sub":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    for j in range(height):
                        temp.append(list(map(Decimal, inp[j * self.matrix.width + 1:j * self.matrix.width + self.matrix.width + 1])))
                        self.outputMatrix(self.matrix - Matrix(self.matrix.width, self.matrix.height, temp))
                    if "-s" in inp:
                        self.matrix -= Matrix(self.matrix.width, self.matrix.height, temp)

            elif inp[0] == "mul":
                if self.path == "Matan/Matrix> ":
                    if len(inp) == 2:
                        self.outputMatrix(self.matrix.mul(Decimal(eval(inp[1]))))
                        if "-s" in inp:
                            self.matrix = self.matrix.mul(Decimal(eval(inp[1])))
                    else:
                        temp = []
                        width, height = int(inp[1]), int(inp[2])
                        for j in range(height):
                            temp.append(list(map(int, inp[j * width + 3:j * width + width + 3])))
                        self.outputMatrix(self.matrix * Matrix(width, height, temp))
                        if "-s" in inp:
                            self.matrix *= Matrix(width, height, temp)
                       
            elif inp[0] == "transpose":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.transpose())
                    if "-s" in inp:
                        self.matrix = self.matrix.transpose()

            elif inp[0] == "addition":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.addition())
                    if "-s" in inp:
                        self.matrix = self.matrix.addition()

            elif inp[0] == "inv":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.inverse())
                    if "-s" in inp:
                        self.matrix = self.matrix.inverse()
            
            elif inp[0] == "stair":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.stair())
                    if "-s" in inp:
                        self.matrix = self.matrix.stair()
            
            elif inp[0] == "rang":
                if self.path == "Matan/Matrix> ":
                    self.output(self.matrix.rang())


                if self.path == "Matan/Matrix> ":
                    self.matrix = self.memory[inp[1]]
 
            elif inp[0] == "cramer":
                self.output(" ".join(map(str, Cramer(inp[1:]))))
            
            elif inp[0] == "invm":
                self.output(" ".join(map(str, inverseMatrix(inp[1:]))))
            
            elif inp[0] == "gauss":
                self.output(" ".join(map(str, Gauss(inp[1:]))))
                
            elif inp[0] == "symm":
                self.output(" ".join(map(str, Equation(inp[1]).symmetric())))
            
            elif inp[0] == "poly":
                if self.path == "Matan> ":
                    self.poly = Polynomial(parseFromString(inp[1]))
                    self.changePath("Polynomial")
                elif self.path == "Matan/Polynomial> ":
                    self.output(str(self.poly))
            
            elif inp[0] == "div":
                self.output(self.poly / Polynomial(parseFromString(inp[1])))
                if "-s" in inp:
                    self.poly /= Polynomial(parseFromString(inp[1]))
                
            elif inp[0] == "gorner":
                self.output(self.poly.Gorner(Decimal(inp[1])))
                if "-s" in inp:
                    self.poly = self.Gorner(Decimal(inp[1]))
                
            elif inp[0] == "fact":
                self.output(self.poly.factorio())
                