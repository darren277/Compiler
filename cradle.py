""""""

import sys

#TAB = '^I'
TAB = '\t'

Look: chr

CR = '\r'


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
def GetNum() -> str:
    Value: str = ''
    if not IsDigit(Look): Expected('Integer')
    while IsDigit(Look):
        Value += Look
        GetChar()
    _GetNum = Value
    SkipWhite()
    return _GetNum




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
    GetChar()
    SkipWhite()







# Parse and translate a math expression.
def Term():
    Factor()
    while Look in ['*', '/']:
        EmitLn('MOVE D0,-(SP)')
        if Look == '*': Multiply()
        elif Look == '/': Divide()
        else: Expected('Mulop')


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
def Factor():
    if Look == '(':
        Match('(')
        Expression()
        Match(')')
    elif IsAlpha(Look): Ident()
    else: EmitLn(f'MOVE #{GetNum()},D0')


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
def Expression():
    if IsAddop(Look): EmitLn('CLR D0')
    else: Term()
    while IsAddop(Look):
        EmitLn('MOVE D0,-(SP)')
        if Look == '+': Add()
        elif Look == '-': Subtract()
        else: Expected('Addop')





# Main program.
Init()
Expression()
if Look != CR: Expected('Newline')






