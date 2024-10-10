import copy
from fractions import Fraction
from decimal import Decimal

class Matrix:
    def __init__(self, width: int, height: int, data: list):
        self.width = width
        self.height = height
        self.data = data
    
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
        newData = copy.deepcopy(self.data)
        print(newData, self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j].normalize()
        return Matrix(self.width, self.height, newData)

    def toFrac(self):
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.height):
                if newData % 1 != 0:
                    frac = Fraction(newData[i][j]).limit_denominator()
                    newData[i][j] = f"{frac.numerator}/{frac.denominator}"
        return Matrix(self.width, self.height, newData)
    
    def transpose(self):
        newData = []
        for j in range(self.width):
            temp = []
            for i in range(self.height):
                temp.append(self.data[i][j])
            newData.append(temp)
        return Matrix(self.height, self.width, newData)
    
    def mul(self, num: Decimal):
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                newData[i][j] = newData[i][j] * num
        return Matrix(self.height, self.width, newData)
    
    def minor(self, i: int, j: int):
        newData = copy.deepcopy(self.data)
        newData.pop(j)
        for x in newData:
            x.pop(i)
        return Matrix(self.width - 1, self.height - 1, newData)

    def determinant(self):
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
        newData = copy.deepcopy(self.data)
        for i in range(self.height):
            for j in range(self.width):
                if (j == column):
                    newData[i][j] = newColumn[i]
        return Matrix(self.width, self.height, newData)

    def addition(self):
        newData = []

        for j in range(self.height):
            temp = []
            for i in range(self.width):
                temp.append(self.minor(i, j).determinant() * (-1)**(i+j+2))
            newData.append(temp)
        return Matrix(self.width, self.height, newData).transpose()
    
    def inverse(self):
        return Matrix(self.width, self.height, self.data).addition().mul(1 / self.determinant())
    
    def swapRows(self, j1: int, j2: int):
        newData = copy.deepcopy(self.data)
        newData[j1], newData[j2] = newData[j2], newData[j1]
        return Matrix(self.width, self.height, newData)
    
    def divideRow(self, j: int, divider: Decimal):
        newData = copy.deepcopy(self.data)
        try:
            newData[j] = [a / divider for a in newData[j]]
            return Matrix(self.width, self.height, newData)
        except ZeroDivisionError:
            return Matrix(self.width, self.height, newData)
    
    def combineRows(self, j1: int, j2: int, weight: Decimal):
        newData = copy.deepcopy(self.data)
        newData[j1] = [(a + k * weight) for a, k in zip(newData[j1], newData[j2])]
        return Matrix(self.width, self.height, newData)
    
    def stair(self):
        new = Matrix(self.width, self.height, copy.deepcopy(self.data))
        column = 0
        while (column < self.height):
            current_row = None
            for r in range(column, self.height):
                if current_row is None or abs(new.data[r][column]) > abs(new.data[current_row][column]):
                    current_row = r
            if current_row != column:
                new = new.swapRows(current_row, column)
            new = new.divideRow(column, new.data[column][column])
            for r in range(column + 1, self.height):
                new = new.combineRows(r, column, -new.data[r][column])
            column += 1
        return new
    
    def rang(self):
        stair = self.stair()
        result = 0
        for i in stair.data:
            if any(i):
                result += 1
        return result
