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
    
    def outputList(self, out: list) -> None:
        print("+")
        for i in out:
            print("|", i)
        print("+")

    def outputMatrix(self, matrix: Matrix) -> None:
        self.outputList(str(matrix).split("\n"))

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
                    self.outputMatrix(self.memory[inp[1]])
                    
            
            elif inp[0] == "set":
                if self.path == "Matan/Matrix> ":
                    self.matrix = self.memory[inp[1]]

            elif inp[0] == "matrix":
                if not self.matrix or len(inp) > 1:
                    self.matrix = self.inputMatrix(int(inp[1]), int(inp[2]), inp[3:])
                    self.context = "matrix"
                self.outputMatrix(self.matrix)
                

            elif inp[0] == "minor":
                if self.matrix:
                    self.outputMatrix(self.matrix.minor(int(inp[1]) - 1, int(inp[2]) - 1))

            elif inp[0] == "dt":
                if self.matrix:
                    print(f"+\n| {self.matrix.determinant()}\n+")

            elif inp[0] == "tr":
                if self.matrix:
                    res:Matrix = self.matrix.transpose()
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "add":
                if self.matrix:
                    res = self.matrix + self.inputMatrix(self.matrix.width, self.matrix.height, inp[1:])
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "sub":
                if self.matrix:
                    res = self.matrix - self.inputMatrix(self.matrix.width, self.matrix.height, inp[1:])
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res

            elif inp[0] == "mul":
                if self.matrix:
                    if len(inp) <= 3:
                        res = self.matrix.mul(sp.S(inp[1]))
                    else:
                        res = self.matrix * self.inputMatrix(int(inp[1]), int(inp[2]), inp[3:])
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res
            
            elif inp[0] == "ech":
                if self.matrix:
                    res = self.matrix.echelon()
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res
            
            elif inp[0] == "inv":
                if self.matrix:
                    res = self.matrix.inverse()
                    self.outputMatrix(res)
                    if "-s" in inp:
                        self.matrix = res
 
            elif inp[0] == "rang":
                if self.matrix:
                    res = self.matrix.rang()
                    print(f"+\n| {res}\n+")
 
            elif inp[0] == "cramer":
                self.outputList(Cramer(inp[1:]))

            elif inp[0] == "invm":
                self.outputList(inverseMatrix(inp[1:]))
            
            elif inp[0] == "gauss":
                self.outputList(Gauss(inp[1:]))
                
            elif inp[0] == "calc":
                for i in self.memory.keys():
                    inp[1] = inp[1].replace(i, f"Matrix({self.memory[i].width}, {self.memory[i].height}, {self.memory[i].data})")
                res = eval(inp[1])
                if type(res) == Matrix:
                    self.outputMatrix(res)
                else:
                    print("|", res)
                
            elif inp[0] == "poly":
                if not self.polynomial or len(inp) > 1:
                    self.polynomial = Polynomial(parseFromString(inp[1]))
                print(f"+\n| {self.polynomial}\n+")
            
            elif inp[0] == "div":
                if self.polynomial:
                    res = self.polynomial / Polynomial(parseFromString(inp[1]))
                    print(f"+\n| {res[0]}{res[1]} + {res[2]}\n+".replace(" + 0", "").replace("+ -", "- ").replace("(x)", "x"))
                    if "-s" in inp:
                        self.polynomial = res
            
            elif inp[0] == "fact":
                if self.polynomial:
                    print(f"+\n| {''.join(map(str, self.polynomial.factorio()))}\n+")
                
            elif inp[0] == "solve":
                if self.polynomial:
                    self.outputList(self.polynomial.solve())
