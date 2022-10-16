""""""

import sys

#TAB = '^I'
from typing import Dict

TAB = '\t'

Look: chr
Table: Dict[chr, int] = dict()


CR = '\r'
LF = '\n'


# Read new character from input stream.
def GetChar() -> chr:
    global Look
    Look = sys.stdin.read(1)
    return Look


# Report an error.
def Error(s: str):
    print()
    print(f'^GError: {s}.')


# Report error and halt.
def Abort(s: str):
    Error(s)
    sys.exit(1)


# Report what was expected.
def Expected(s: str):
    Abort(f'{s} Expected')


# Match a specific input character.
def Match(x: chr):
    if Look != x: Expected(f"'{x}'")
    else:
        GetChar()
        SkipWhite()



# Recognize an alpha character.
def IsAlpha(c: chr) -> bool:
    return c.isalpha()


# Recognize a decimal digit.
def IsDigit(c: chr) -> bool:
    return c.isdigit()


# Recognize an alphanumeric.
def IsAlNum(c: chr) -> bool:
    return IsAlpha(c) or IsDigit(c)



# Get an identifier.
def GetName() -> str:
    Token: str = ''
    if not IsAlpha(Look): Expected('Name')
    while IsAlNum(Look):
        Token += Look.upper()
        GetChar()
    _GetName = Token
    SkipWhite()
    return _GetName



# Get a number.
def GetNum() -> int:
    Value: int = 0
    if not IsDigit(Look): Expected('Integer')
    while IsDigit(Look):
        Value = 10 * Value + ord(Look) - ord('0')
        GetChar()
    return Value



# Parse and translate an assignment statement.
def Assignment():
    Name: chr = GetName()
    Match('=')
    Table[Name] = Expression()


# Recognize and skip over a newline.
def NewLine():
    if Look == CR:
        GetChar()
        if Look == LF: GetChar()



# Recognize white space.
def IsWhite(c: chr) -> bool:
    return c in [' ', TAB]


# Skip over leading white space.
def SkipWhite():
    while IsWhite(Look): GetChar()


# Output a string with tab.
def Emit(s: str):
    print(TAB, s)


# Output a string with tab and CRLF.
def EmitLn(s: str):
    Emit(s)
    print()


# Initialize.
def Init():
    InitTable()
    GetChar()
    SkipWhite()




# Initialize the variable area.
def InitTable():
    i: chr
    for i in range(ord('A'), ord('Z') + 1):
        Table[chr(i)] = 0




# Parse and translate a math term.
def Term() -> int:
    Value: int = GetNum()
    while Look in ['*', '/']:
        if Look == '*':
            Match('*')
            Value *= GetNum()
        elif Look == '/':
            Match('/')
            Value /= GetNum()
        else: Expected('Mulop')
    return Value


# Recognize and translate an add.
def Add():
    Match('+')
    Term()
    EmitLn('ADD (SP)+,D0')

# Recognize and translate a subtract.
def Subtract():
    Match('-')
    Term()
    EmitLn('SUB (SP)+,D0')
    EmitLn('NEG D0')


# Parse and translate an identifier.
def Ident():
    Name: chr = GetName()
    if Look == '(':
        Match('(')
        Match(')')
        EmitLn(f'BSR {Name}')
    else: EmitLn(f'MOVE {Name}(PC),D0')


# Parse and translate a math factor.
def Factor() -> int:
    _Factor: int = 0
    if Look == '(':
        Match('(')
        _Factor = Expression()
        Match(')')
    elif IsAlpha(Look): _Factor = Table[GetName()]
    else: _Factor = GetNum()
    return _Factor



# Recognize and translate a multiply.
def Multiply():
    Match('*')
    Factor()
    EmitLn('MULS (SP)+,D0')


# Recognize and translate a divide.
def Divide():
    Match('/')
    Factor()
    EmitLn('MOVE (SP)+,D1')
    EmitLn('DIVS D1,D0')


# Recognize an Addop.
def IsAddop(c: chr) -> bool:
    return c in ['+', '-']



# Parse and translate an assignment statement.
def Assignment():
    Name: chr = GetName()
    Match('=')
    Expression()
    EmitLn(f'LEA {Name}(PC),A0')
    EmitLn('MOVE D0,(A0)')





# Parse and translate a math expression.
def Expression() -> int:
    Value: int
    if IsAddop(Look): Value = 0
    else: Value = GetNum()
    while IsAddop(Look):
        EmitLn('MOVE D0,-(SP)')
        if Look == '+':
            Match('+')
            Value += GetNum()
        elif Look == '-':
            Match('-')
            Value -= GetNum()
        else: Expected('Addop')
    return Value






# Main program.
Init()
while Look != '.':
    Assignment()
    NewLine()






