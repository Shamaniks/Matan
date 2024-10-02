OPERATORS = {"+": (1, lambda x, y: x + y), "-": (1, lambda x, y: x - y), "*": (2, lambda x, y: x * y), "/": (2, lambda x, y: x / y)}


def parse(formulaString):
    number = ""
    for s in formulaString:
        if s in "1234567890.":
            number += s
        elif number:
            yield float(number)
            number = ""
        if s in "/*-+()":
            yield s
    if number:
        yield float(number)


def shunting_yard(parsedFormula):
    stack = []
    for token in parsedFormula:
        if token in OPERATORS:
            while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()


def calc(polish):
    stack = []
    for token in polish:
        if token in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[token][1](x, y))
        else:
            stack.append(token)
    return stack[0]