# -*- coding: utf-8 -*-

ILLEGAL = "ILLEGAL"
EOF = "EOF"
	
# 識別子
IDENT = "IDENT"
INT = "INT"
	
# 演算子
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
	
LT = "<"
GT = ">"
	
EQ = "=="
NOT_EQ = "!="
	
# デリミタ
COMMA = ","
SEMICOLON = ";"
	
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
	
# キーワード
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"
	
#
STRING = "STRING"
	
# 配列
LBRACKET = "["
RBRACKET = "]"

# HASH
COLON = ":"
	
keywords = {
	"fn": FUNCTION,
	"let": LET,
	"true": TRUE,
	"false": FALSE,
	"if": IF,
	"else": ELSE,
	"return": RETURN,
}

def LookupIdent(ident):
	#print("LookuoIdent: ", ident)
	#print("call LookupIdent")
	if ident in keywords:
		#print("pass1")
		#print(ident, ":", keywords[ident])
		return keywords[ident]
	else:
		return IDENT


class Token:
	def __init__(self, tokenType, ch):
		self.Type = tokenType
		self.Literal = ch
	
	def printout(self):
		print("{Type:", self.Type, "Literal:", self.Literal, "}")


if __name__ == "__main__":
	#print(keywords)
	for key in keywords:
		print(key, ":", keywords[key])
	
	tok = LookupIdent("let")
	print(tok)
	tok = LookupIdent("aaa")
	print(tok)
	
