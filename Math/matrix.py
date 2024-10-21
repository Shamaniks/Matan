import copy
from fractions import Fraction
from decimal import Decimal

class Matrix:
    def __init__(self, width: int, height: int, data: list):
        self.width: int = width
        self.height: int = height
        self.data: list = data
    
    def __add__(self, other):
        new = Matrix(self.width, self.height, copy.deepcopy(self.data))
        for i in range(self.height):
            for j in range(self.width):
                new.data[i][j] = self.data[i][j] + other.data[i][j]
        return new
    
    def __sub__(self, other):
        new = Matrix(self.width, self.height, copy.deepcopy(self.data))
        for i in range(self.height):
            for j in range(self.width):
                new.data[i][j] -= other.data[i][j]
        return new
    
    def __mul__(self, other):
        other = other.transpose()
        newData = []

        for i in range(self.height):
            tempRow = []
            for j in range(other.height):
                tempEl = 0
                for k in range(self.width):
                    tempEl += self.data[i][k] * other.data[j][k]
                tempRow.append(tempEl)
            newData.append(tempRow)
        return Matrix(other.height, self.height, newData)
    
    def round(self):
        """
        Rounds all elements in the matrix to the nearest integer.

        Args:
        None
        
        Return:
        Matrix: The matrix with all elements rounded to the nearest integer.
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j].normalize()
        return Matrix(self.width, self.height, newData)

    def toFrac(self):
        """
        Converts all elements in the matrix to fractions.

        Args:
        None
        
        Return:
        Matrix: The matrix with all elements converted to fractions.
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.height):
                if newData % 1 != 0:
                    frac = Fraction(newData[i][j]).limit_denominator()
                    newData[i][j] = f"{frac.numerator}/{frac.denominator}"
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
        for j in range(self.width):
            temp = []
            for i in range(self.height):
                temp.append(self.data[i][j])
            newData.append(temp)
        return Matrix(self.height, self.width, newData)
    
    def mul(self, num: Decimal):
        """
        Multiplies matrix by scalar.
        
        Args:
        num (Decimal): The scalar to multiply the matrix by.
        
        Return:
        Matrix: The matrix multiplied by the scalar.
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] = newData[i][j] * num
        return Matrix(self.height, self.width, newData)
    
    def minor(self, i: int, j: int):
        """
        Selects part of the matrix to calculate the determinant.

        Args:
        i (int): The column to select.
        j (int): The row to select.
        
        Return:
        Matrix: The selected part of the matrix.
        """
        newData = copy.deepcopy(self.data)
        newData.pop(j)
        for x in newData:
            x.pop(i)
        return Matrix(self.width - 1, self.height - 1, newData)

    def determinant(self) -> Decimal:
        """
        Calculates determinant of the matrix
        
        Args:
        None
        
        Return:
        Decimal: The determinant of the matrix
        """
        data = copy.deepcopy(self.data)
        if self.width == 2 and self.height == 2:
            return data[0][0] * data[1][1] - data[0][1] * data[1][0]
        elif self.width == 1 and self.height == 1:
            return data[0][0]
        else:
            result = 0
            for i in range(self.height):
                result += data[i][0] * self.minor(0, i).determinant() * (-1)**i
            return result

    def replaceColumn(self, newColumn: list, column: int):
        """
        Replaces a column in the matrix with a new one.

        Args:
        newColumn (list): The new column to replace.
        column (int): The column to replace.
        
        Return:
        Matrix: The matrix with the new column.
        """
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                if (j == column):
                    newData[i][j] = newColumn[i]
        return Matrix(self.width, self.height, newData)

    def addition(self):
        """
        Converts all elements of the matrix to their addition
        
        Args:
        None
        
        Return:
        Matrix: The matrix with all elements's additions

        """
        newData = []

        for j in range(self.height):
            temp = []
            for i in range(self.width):
                temp.append(self.minor(i, j).determinant() * (-1)**(i+j+2))
            newData.append(temp)
        return Matrix(self.width, self.height, newData).transpose()
    
    def inverse(self):
        """
        Inverses the matrix

        Args:
        None
        
        Return:
        Matrix: The inversed matrix
        """
        return Matrix(self.width, self.height, self.data).addition().mul(1 / self.determinant())
    
    def swapRows(self, j1: int, j2: int):
        """
        Swaps rows of the matrix
        
        Args:
        j1 (int): The first row to swap.
        j2 (int): The second row to swap.
        
        Return:
        Matrix: The matrix with the rows swapped.
        """
        newData = copy.deepcopy(self.data)
        newData[j1], newData[j2] = newData[j2], newData[j1]
        return Matrix(self.width, self.height, newData)
    
    def divideRow(self, j: int, divider: Decimal):
        """
        Divides row of the matrix
        
        Args:
        j (int): The row to divide.
        divider (Decimal): The divider.
        
        Return:
        Matrix: The matrix with the row divided.
        """
        newData = copy.deepcopy(self.data)
        try:
            newData[j] = [a / divider for a in newData[j]]
            return Matrix(self.width, self.height, newData)
        except ZeroDivisionError:
            return Matrix(self.width, self.height, newData)
    
    def combineRows(self, j1: int, j2: int, weight: Decimal):
        """
        Combines rows of the matrix

        Args:
        j1 (int): The row to be combined.
        j2 (int): The row to combine with.
        weight (Decimal): The weight of the second row.

        Return:
        Matrix: The matrix with the rows combined.

        """
        newData = copy.deepcopy(self.data)
        newData[j1] = [(a + k * weight) for a, k in zip(newData[j1], newData[j2])]
        return Matrix(self.width, self.height, newData)
    
    def stair(self):
        """
        Calculates stair of the matrix

        Args:
        None
        
        Return:
        Matrix: The matrix with the stair calculated.
        """
        new_matrix = Matrix(self.width, self.height, copy.deepcopy(self.data))
        for col in range(self.height):
            # Find the row with the largest absolute value in the current column
            max_row = max(range(col, self.height), key=lambda r: abs(new_matrix.data[r][col]))
            
            # Swap the current row with the row having the largest absolute value
            if max_row != col:
                new_matrix = new_matrix.swapRows(max_row, col)
            
            # Divide the current row by the pivot element
            new_matrix = new_matrix.divideRow(col, new_matrix.data[col][col])
            
            # Eliminate the current column in the rows below and above
            for row in range(self.height):
                if row != col:
                    new_matrix = new_matrix.combineRows(row, col, -new_matrix.data[row][col])
        
        return new_matrix
    
    def rang(self):
        """
        Calculates rang of the matrix

        Args:
        None        
        
        Return:
        int: The rang of the matrix.
        """
        stair = self.stair()
        result = 0
        for i in stair.data:
            if any(i):
                result += 1
        return result
