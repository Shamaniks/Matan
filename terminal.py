from decimal import Decimal

import sympy as sp

from Math.matrix import Matrix
from Math.equation import *
from Math.polynomial import Polynomial, parseFromString

class Terminal:
    context: str = ""
    matrix: Matrix = None
    memory: dict = {}
    polynomial: Polynomial = None

    def inputMatrix(self, width: int, height: int, inp: list) -> Matrix:
        """
        Parses matrix from list of string
        
        Args:
        inp (list): The list to be parsed
        
        Return:
        Matrix: Parsed matrix
        """
        data = []
        for i in range(height):
            data.append(list(map(sp.simplify, inp[width * i:width + width * i])))
        return Matrix(width, height, data)

    def outputMatrix(self, matrix: Matrix) -> None:
        """
        Prints the matrix with indentation based on self.path and with indentation between columns
        
        Args:
        matrix (Matrix): The matrix to be printed
        
        Return:
        None
        """
        for i in str(matrix).split("\n"):
            print(f"|{i}")

    def mainLoop(self) -> None:
        """
        Loops through the main menu
        
        Args:
        None
        
        Return:
        None
        """
        while True:
            inp: list = input("> ").split()
            
            if inp[0] == "stop":
                break

            elif inp[0] == "rem":
                if inp[1] == "mat":
                    self.memory[inp[2]] = self.matrix
            
            elif inp[0] == "out":
                if type(self.memory[inp[1]]) == Matrix:
                    print("+")
                    self.outputMatrix(self.memory[inp[1]])
                    print("+")
            
            elif inp[0] == "set":
                if self.path == "Matan/Matrix> ":
                    self.matrix = self.memory[inp[1]]

            elif inp[0] == "matrix":
                if not self.matrix or len(inp) > 1:
                    self.matrix = self.inputMatrix(int(inp[1]), int(inp[2]), inp[3:])
                    self.context = "matrix"
                print("+")
                self.outputMatrix(self.matrix)
                print("+")

            elif inp[0] == "minor":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.minor(int(inp[1]) - 1, int(inp[2]) - 1))

            elif inp[0] == "dt":
                if self.matrix:
                    print(f"+\n| {self.matrix.determinant()}\n+")

            elif inp[0] == "tr":
                if self.matrix:
                    res:Matrix = self.matrix.transpose()
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "add":
                if self.matrix:
                    res = self.matrix + self.inputMatrix(self.matrix.width, self.matrix.height, inp[1:])
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "sub":
                if self.matrix:
                    res = self.matrix - self.inputMatrix(self.matrix.width, self.matrix.height, inp[1:])
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "mul":
                if self.matrix:
                    if len(inp) <= 3:
                        res = self.matrix.mul(sp.S(inp[1]))
                    else:
                        res = self.matrix * self.inputMatrix(int(inp[1]), int(inp[2]), inp[3:])
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res
            
            elif inp[0] == "ech":
                if self.matrix:
                    res = self.matrix.echelon()
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res
            
            elif inp[0] == "inv":
                if self.matrix:
                    res = self.matrix.inverse()
                    print("+")
                    self.outputMatrix(res)
                    print("+")
                    if "-s" in inp:
                        self.matrix = res
 
            elif inp[0] == "cramer":
                print("+\n|", "\n| ".join(map(str, Cramer(inp[1:]))), "\n+")
            
            elif inp[0] == "invm":
                print("+\n|", "\n| ".join(map(str, inverseMatrix(inp[1:]))), "\n+")
            
            elif inp[0] == "gauss":
                print("+\n|", "\n| ".join(map(str, Gauss(inp[1:]))), "\n+")
                
            elif inp[0] == "calc":
                print("+")
                for i in self.memory.keys():
                    inp[1] = inp[1].replace(i, f"Matrix({self.memory[i].width}, {self.memory[i].height}, {self.memory[i].data})")
                res = eval(inp[1])
                if type(res) == Matrix:
                    self.outputMatrix(res)
                else:
                    print(f"| {res}")
                print("+")
            
            elif inp[0] == "eq":
                print("+\n|", "\n| ".join(map(lambda x: str(x), Equation(inp[1]).square())), "\n+")
                
            elif inp[0] == "symm":
                self.output(" ".join(map(str, Equation(inp[1]).symmetric())))
            
            elif inp[0] == "cardano":
                print("+\n|", "\n| ".join(map(lambda x: str(x), Equation(inp[1]).Cardano())), "\n+")
            
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
                