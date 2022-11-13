# Name: Jiahao Lai
# User id: jvl6364@psu.edu
# Description: Using Python to write a recursive descent parser for a restricted form of SQL
# declaration: Apply some code from the example parser file posted on Canvas

KEYWORD, INT, FLOAT, ID, COMMA, OPERATOR, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7, 8
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

# change to string
def typeToString(tp):
    if (tp == INT):
        return "Int"
    elif (tp == FLOAT):
        return "Float"
    elif (tp == ID):
        return "ID"
    elif (tp == KEYWORD):
        return "Keyword"
    elif (tp == COMMA):
        return "Comma"
    elif (tp == OPERATOR):
        return "Operator"
    elif (tp == EOI):
        return "EOI"
    return "Invalid"

class Token:
    # a Token object has two fields: the token's type and its value
    def __init__(self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    # define the behavior when printing a Token object
    def __repr__(self):
        if (self.type == KEYWORD):
            return self.val
        elif (self.type in [INT, FLOAT, ID]):
            return self.val
        elif (self.type == COMMA):
            return ","
        elif (self.type == OPERATOR):
            return self.val
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

class Lexer:
    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__(self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    # nextToken() returns the next available token
    def nextToken(self):
        while True:
            # is a letter
            if self.ch.isalpha():
                id = self.consumeChars(LETTERS+DIGITS)
                # judge if it is a Keyword
                if id in ["SELECT", "FROM", "WHERE", "AND"]:
                    return Token(KEYWORD, id)
                # judge if it is an Id
                else:
                    return Token(ID, id)
            # is a digit and judge if it is an Int or a Float
            elif self.ch.isdigit():
                num = self.consumeChars(DIGITS)
                if self.ch != ".":
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit():
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                else:
                    return Token(INVALID, num)
            # white space
            elif self.ch == ' ':
                self.nextChar()
            # comma
            elif self.ch == ',':
                self.nextChar()
                return Token(COMMA, "")
            # three operators (=|<|>):
            elif self.ch == '=':
                self.nextChar()
                return Token(OPERATOR, "=")
            elif self.ch == '<':
                self.nextChar()
                return Token(OPERATOR, "<")
            elif self.ch == '>':
                self.nextChar()
                return Token(OPERATOR, ">")
            # EOI($):
            elif self.ch == '$':
                return Token(EOI, "")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)
    # go to next Char:
    def nextChar(self):
        self.ch = self.stmt[self.index]
        self.index = self.index + 1

    # consume Chars:
    def consumeChars(self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    # check Chars:
    def checkChar(self, c):
        self.nextChar()
        if (self.ch == c):
            self.nextChar()
            return True
        else:
            return False

import sys

class Parser:
    def __init__(self, s):
        # manually set $ as the EOI
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.query()

    # start parse Query:
    def query(self):
        print("<Query>")
        # In the SQL, the first token should be a Keyword
        # and here the value of it should be SELECT
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "SELECT":
            print("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.token = self.lexer.nextToken()
            # go to IDList
            self.idList()
        # If the first token is a keyword, but the value is not SELECT
        # Syntax error
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() != "SELECT":
            print("Syntax error: expecting: " + "SELECT"
                  + "; saw: " + self.token.getTokenValue())
            sys.exit(1)
        # If the first token is not a keyword
        # Syntax error
        else:
            self.error(KEYWORD)

        # After the first IDList, the next token should be a keyword
        # and the value of this keyword should be FROM
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "FROM":
            print("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.token = self.lexer.nextToken()
            #go to IDList
            self.idList()
        # If the token here is a keyword, but the value of it is not FROM
        # Syntax error
        elif self.token.getTokenType() == KEYWORD and self.token.getTokenValue() != "FROM":
            print("Syntax error: expecting: " + "FROM"
                  + "; saw: " + self.token.getTokenValue())
            sys.exit(1)
        # If the token here is not a keyword
        # Syntax error
        else:
            self.error(KEYWORD)

        # If the query has keyword WHERE
        # then go to CondList
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "WHERE":
            print("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.token = self.lexer.nextToken()
            self.condList()

        # If reach to the EOI
        # end the Query
        if self.token.getTokenType() == EOI:
            print("</Query>")

        # If the token is invalid
        if self.token.getTokenType() == INVALID:
            self.error(INVALID)
            self.token = self.lexer.nextToken()

    # start parse IDList
    def idList(self):
        print("\t<IDList>")
        # IDList should start from an ID
        if self.token.getTokenType() == ID:
            print("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
            self.token = self.lexer.nextToken()
        else:
            self.error(ID)
        # If comma appears, then there should be another ID after comma
        while self.token.getTokenType() == COMMA:
            print("\t\t<Comma>,</Comma>")
            self.token = self.lexer.nextToken()
            # If the token after comma is not an ID
            if self.token.getTokenType() == ID:
                print("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
                self.token = self.lexer.nextToken()
            else:
                self.error(ID)
        # IDList end
        print("\t</IDList>")


    def condList(self):
        # start parse CondList
        print("\t<CondList>")
        # the first token in Condlist should be an ID, then can go to Cond
        # becasue <CondList> -> <Cond> {AND <Cond>} and <Cond> -> <id> <operator> <Term>
        if self.token.getTokenType() == ID:
            #go to Cond
            self.cond()
        else:
            self.error(ID)

        # If there are more than one Cond, then keyword AND is needed
        if self.token.getTokenType() == KEYWORD and self.token.getTokenValue() != "AND":
            print("Syntax error: expecting: " + "AND"
                  + "; saw: " + self.token.getTokenValue())
            sys.exit(1)
        # the token after AND should be an ID, too
        # then can go to Cond
        while self.token.getTokenType() == KEYWORD and self.token.getTokenValue() == "AND":
            print("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.token = self.lexer.nextToken()
            if self.token.getTokenType() == ID:
                self.cond()
            else:
                self.error(ID)
        print("\t</CondList>")

    def cond(self):
        # start parse Cond
        print("\t\t<Cond>")
        # because in CondList, we ensure that Cond starts with and ID
        print("\t\t\t<Id>" + self.token.getTokenValue() + "</Id>")
        self.token = self.lexer.nextToken()
        # the next token should be an Operator
        if self.token.getTokenType() == OPERATOR:
            print("\t\t\t<Operator>" + self.token.getTokenValue() + "</Operator>")
            self.token = self.lexer.nextToken()
            # then go to Term
            self.term()
        else:
            self.error(OPERATOR)
        print("\t\t</Cond>")

    def term(self):
        # start parse Term
        print("\t\t\t<Term>")
        # If the Term is an ID
        if self.token.getTokenType() == ID:
            print("\t\t\t\t<Id>" + self.token.getTokenValue() + "</Id>")
            self.token = self.lexer.nextToken()
        # If the Term is an Int
        elif self.token.getTokenType() == INT:
            print("\t\t\t\t<Int>" + self.token.getTokenValue() + "</Int>")
            self.token = self.lexer.nextToken()
        # If the Term is a Float
        elif self.token.getTokenType() == FLOAT:
            print("\t\t\t\t<Float>" + self.token.getTokenValue() + "</Float>")
            self.token = self.lexer.nextToken()
        else:
            print("Syntax error: expecting an ID, an int, or a float"
                  + "; saw:" + typeToString(self.token.getTokenType()))
            sys.exit(1)
            self.token = self.lexer.nextToken()

        # Because we can only choose one from [ID, INT, FLOAT],
        # If the token after Term is a Keyword AND,
        # then start another Cond
        # otherwise, the query should reach to EOI
        if self.token.getTokenType() != EOI and self.token.getTokenValue() != "AND":
            self.error(EOI)
        print("\t\t\t</Term>")

    # check if the token type is matched
    def match(self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else:
            self.error(tp)
        return val
    # Syntax error
    def error(self, tp):
        print("Syntax error: expecting: " + typeToString(tp) + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)

# start test:
parser = Parser ("SELECT C1,C2 FROM T1 WHERE C1=5.23")
parser.run()



