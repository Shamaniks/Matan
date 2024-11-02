import copy
import sympy as sp

from decimal import Decimal
class Matrix:
    def __init__(self, width: int, height: int, data: list):
        self.width: int = width
        self.height: int = height
        self.data: list = data
    
    def __str__(self) -> str:
        """
        Converts matrix to string with space between columns
        """
        res = []
        lens = []
        for i in self.transpose().data:
            lens.append(max(map(lambda x: len(str(x)), [j for j in i])))
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                row += " " * (lens[j] - len(str(self.data[i][j])) + 1) + str(self.data[i][j])
            res.append(row)
        return "\n".join(res)

    def __add__(self, other):
        """
        Adds one matrix to another.
        
        Args:
        self (Matrix): The first matrix
        other (Matrix): The second matrix
        
        Return: The sum of matrixes
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] += other.data[i][j]
        return Matrix(self.width, self.height, newData)
    
    def __sub__(self, other):
        """
        Adds one matrix to another.
        
        Args:
        self (Matrix): The first matrix
        other (Matrix): The second matrix
        
        Return: The sum of matrixes
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] -= other.data[i][j]
        return Matrix(self.width, self.height, newData)

    def __mul__(self, other):
        """
        Multiplies two matrixes.
        
        Args:
        self (Matrix): The first matrix to multiply
        other (Matrix): The second matrix to multiply
        
        Return: The multiplied matrix
        """
        newData = []
        other = other.transpose()
        for height in range(other.height):
            row = []
            for width in range(self.height):
                el = 0
                for i in range(other.width):
                    el += self.data[width][i] * other.data[height][i]
                row.append(el)
            newData.append(row)
        return Matrix(width + 1, height + 1, newData).transpose()
    
    def determinant(self) -> str:
        """
        Calculates determinant of the matrix
        
        Args:
        None
        
        Return: The determinant of the matrix
        """
        data = copy.deepcopy(self.data)
        if self.width == 2 and self.height == 2:
            return data[0][0] * data[1][1] - data[1][0] * data[0][1]
        elif self.width == 1 and self.height == 1:
            return data[0][0]
        else:
            result = 0
            for i in range(self.height):
                result += self.addition(0, i) * data[0][i]
            return result

    def minor(self, row:int, col:int):
        newData = copy.deepcopy(self.data)
        newData.pop(row)
        for i in range(self.height - 1):
            newData[i].pop(col)
        return Matrix(self.width - 1, self.height - 1, newData)
    
    def replaceColumn(self, new:list, col:int):
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            newData[i][col] = new[i]
        return Matrix(self.width, self.height, newData)
        
    def transpose(self):
        """
        Transposes the matrix.

        Args:
        None
        
        Return:
        Matrix: The transposed matrix.
        """
        newData = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(self.data[j][i])
            newData.append(row)
        return Matrix(self.height, self.width, newData)

    def mul(self, weight):
        """
        Multiplies matrix on weight.
        
        Args:
        weight: The weight of multiplication
        
        Return: The multiplied matrix
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] *= weight
        return Matrix(self.width, self.height, newData)

    def swapRows(self, j1: int, j2: int):
        """
        Swaps rows of the matrix

        Args:
        j1 (int): The first row to swap.
        j2 (int): The second row to swap.

        Return: The matrix with the rows swapped.
        """
        newData = copy.deepcopy(self.data)
        newData[j1], newData[j2] = newData[j2], newData[j1]
        return Matrix(self.width, self.height, newData)

    def divideRow(self, j: int, divider):
        """
        Divides row of the matrix

        Args:
        j (int): The row to divide.
        divider (sp.S): The divider.

        Return: The matrix with the row divided.
        """
        newData = copy.deepcopy(self.data)
        if divider == 0:
            # If the divider is 0, we cannot divide, return the matrix unchanged
            return Matrix(self.width, self.height, newData)
        newData[j] = [sp.Rational(sp.S(str(a)), sp.S(str(divider))) for a in newData[j]]
        return Matrix(self.width, self.height, newData)

    def combineRows(self, j1: int, j2: int, weight: Decimal):
        """
        Combines rows of the matrix

        Args:
        j1 (int): The row to be combined.
        j2 (int): The row to combine with.
        weight (Decimal): The weight of the second row.

        Return: The matrix with the rows combined.
        """
        newData = copy.deepcopy(self.data)
        newData[j1] = [sp.simplify(f"{a}+{k}*{weight}") for a, k in zip(newData[j1], newData[j2])]
        return Matrix(self.width, self.height, newData)

    def echelon(self):
        """
        Calculates echelon of the matrix

        Args:
        None

        Return: The matrix's echelon calculated.
        """
        newMatrix = Matrix(self.width, self.height, copy.deepcopy(self.data))
        for col in range(self.height):
            max_row = max(range(col, self.height), key=lambda r: abs(newMatrix.data[r][col]))
            if abs(newMatrix.data[max_row][col]) < 1e-10:  # Check for near-zero
                continue 
            if max_row != col:
                newMatrix = newMatrix.swapRows(max_row, col)
            newMatrix = newMatrix.divideRow(col, newMatrix.data[col][col])
            for row in range(col + 1, self.height):  # Start from the next row
                newMatrix = newMatrix.combineRows(row, col, -newMatrix.data[row][col])
        return newMatrix

    def addition(self, row: int, col:int):
        """
        Calculates algebraic addition of matrix element
        
        Args:
        col (int): The column index of element
        row (int): The row index of element
        
        Return: The algebraic addition of matrix element
        """
        return self.minor(row, col).determinant() * (-1) ** (col + row)
    
    def additionMatrix(self):
        """
        Converst all elements of matrix to their algebraic additions
        
        Args:
        None
        
        Return: The matrix with algebraic additions
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] = self.addition(i, j)
        return Matrix(self.width, self.height, newData)

    def inverse(self):
        """
        Calcates inversed version of matrix
        
        Args:
        None
        
        Return: The inversed matrix
        """
        return Matrix(self.width, self.height, copy.deepcopy(self.data)).additionMatrix().transpose().mul(1 / self.determinant())
    
    def rang(self):
        """
        Calculates rang of matrix
        
        Args:
        None
        
        Return: The rang of matrix
        """
        rang = self.height
        echelon = self.echelon()
        for i in range(self.height):
            if echelon[i][i] == 0: rang += 1
        return rang


