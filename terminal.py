import functools

from Math.matrix import Matrix
from Math.equation import *
import mathParser

class Terminal:
    path = "Matan> "
    matrix = None
    memory = {}

    def output(self, output: str, showPath: bool):
        if showPath: print(self.path + f"{output}")
        else: print(" " * len(self.path) + f"{output}")

    def outputMatrix(self, matrix: Matrix):
        row = ""
        for i in matrix.data:
            for j in i: row += str(j) + " "
            self.output(row, False)
            row = ""

    def changePath(self, newPath: str):
        self.path = "Matan/" + newPath + "> "

    def calculate(self, calculation: str, context: str):
        if context == "matrix":
            stack = []
            scalar = ""
            for i in calculation:
                if i in "1234567890./":
                    scalar += i
                if i in self.memory.keys():
                    if scalar:
                        stack.append(self.memory[i].mul(float(eval(scalar))))
                        scalar = ""
                    else:
                        stack.append(self.memory[i])
                if i in "*+()":
                    stack.append(i)
        return mathParser.calc(mathParser.shunting_yard(stack))


    def mainLoop(self):
        while True:
            inp = input(self.path).split()
            if inp[0] == "stop":
                break

            if inp[0] == "exit":
                self.path = "Matan> "

            elif inp[0] == "matrix":
                if self.path == "Matan> ":
                    temp = []
                    width, height = int(inp[1]), int(inp[2])
                    for j in range(height):
                        temp.append(list(map(float, inp[j * width + 3:j * width + width + 3])))
                    self.matrix = Matrix(width, height, temp)
                    self.changePath("Matrix")
                elif self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix)

            elif inp[0] == "minor":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.minor(int(inp[1]) - 1, int(inp[2]) - 1))

            elif inp[0] == "dt":
                if self.path == "Matan/Matrix> ":
                    self.output(self.matrix.determinant(), False)

            elif inp[0] == "new":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    width, height = int(inp[1]), int(inp[2])
                    for j in range(height):
                        temp.append(list(map(float, inp[j * width + 3:j * width + width + 3])))
                    self.matrix = Matrix(width, height, temp)

            elif inp[0] == "add":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    for j in range(height):
                        temp.append(list(map(int, inp[j * self.matrix.width + 1:j * self.matrix.width + self.matrix.width + 1])))
                    self.outputMatrix(self.matrix + Matrix(self.matrix.width, self.matrix.height, temp))
                    if "-s" in inp:
                        self.matrix += Matrix(self.matrix.width, self.matrix.height, temp)

            elif inp[0] == "sub":
                if self.path == "Matan/Matrix> ":
                    temp = []
                    for j in range(height):
                        temp.append(list(map(int, inp[j * self.matrix.width + 1:j * self.matrix.width + self.matrix.width + 1])))
                        self.outputMatrix(self.matrix - Matrix(self.matrix.width, self.matrix.height, temp))
                    if "-s" in inp:
                        self.matrix -= Matrix(self.matrix.width, self.matrix.height, temp)

            elif inp[0] == "mul":
                if self.path == "Matan/Matrix> ":
                    if len(inp) < self.matrix.width * self.matrix.height:
                        self.outputMatrix(self.matrix.mul(float(eval(inp[1]))))
                        if "-s" in inp:
                            self.matrix = self.matrix.mul(float(eval(inp[1])))
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
            
            elif inp[0] =="stair":
                if self.path == "Matan/Matrix> ":
                    self.outputMatrix(self.matrix.stair())
                    if "-s" in inp:
                        self.matrix = self.matrix.stair()

            elif inp[0] == "remember":
                if self.path == "Matan/Matrix> ":
                    self.memory[inp[1]] = self.matrix

            elif inp[0] == "set":
                if self.path == "Matan/Matrix> ":
                    self.matrix = self.memory[inp[1]]

            elif inp[0] == "out":
                if type(self.memory[inp[1]]) == Matrix:
                    self.outputMatrix(self.memory[inp[1]])

            elif inp[0] == "calc":
                if self.path == "Matan/Matrix> ":
                    inp[1] = inp[1].replace("/", "*1/").replace("-", "+-")
                    res = self.calculate(inp[1], "matrix")
                    if type(res) == int:
                        self.output(res, False)
                    elif type(res) == Matrix:
                        if inp[-1] == "-s":
                            self.matrix = res
                        self.outputMatrix(res)

            elif inp[0] == "cramer":
                equations = inp[1:]
                self.output(" ".join(list(map(str, Cramer(equations)))), False)

            elif inp[0] == "gauss":
                equations = inp[1:]
                self.output(" ".join(list(map(str, Gauss(equations)))), False)

            elif inp[0] == "ieqs":
                equations = inp[1:]
                self.output(" ".join(list(map(str, inverseMatrix(equations)))), False)
