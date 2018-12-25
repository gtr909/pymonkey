# -*- coding: utf-8 -*-

import token

class Lexer:
	def __init__(self):
		self.input = ""
		self.position = 0
		self.readPosition = 0
		self.ch = ''
		self.p = 0
		
	def readChar(self):
		#print("call readChar")
		if self.readPosition >= len(self.input):
			self.ch = ""
			#self.ch = 0
			#print("END")
		else:
			self.ch = self.input[self.readPosition]
			#print("readChar() self.ch: ", self.ch)
		
		#print("readChar() pos1: ", self.position, self.readPosition)
		
		if self.readPosition == 0:
			self.posotion = self.readPosition
		else:
			self.position += 1
		#self.posotion = self.readPosition
		#self.position += 1
		self.readPosition += 1
		#print("readChar() pos2: ", self.position, self.readPosition)
		
	def skipWhitespace(self):
		#print("call skipwhitespace")
		while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
			self.readChar()
			#self.position += 1 ###

	def NextToken(self):
		tok = token.Token("", '')
		
		self.skipWhitespace()
		
		#print("in NextToken: ", self.ch)
		
		if self.ch == '-':
			tok = token.Token(token.MINUS, self.ch)
		elif self.ch == '!':
			if self.peekChar() == '=':
				ch = self.ch
				self.readChar()
				literal = str(ch) + str(self.ch)
				tok = token.Token(token.NOT_EQ, literal)
			else:
				tok = newToken(token.BANG, self.ch)
		elif self.ch == '/':
			tok = newToken(token.SLASH, self.ch)
		elif self.ch == '*':
			tok = newToken(token.ASTERISK, self.ch)
		elif self.ch == '<':
			tok = newToken(token.LT, self.ch)
		elif self.ch == '>':
			tok = newToken(token.GT, self.ch)
		elif self.ch == '=':
			if self.peekChar() == '=':
				ch = self.ch
				self.readChar()
				literal = str(ch) + str(self.ch)
				tok = token.Token(token.EQ, literal)
			else:
				tok = newToken(token.ASSIGN, self.ch)
		elif self.ch == ';':
			tok = newToken(token.SEMICOLON, self.ch)
		elif self.ch == '(':
			tok = newToken(token.LPAREN, self.ch)
		elif self.ch == ')':
			tok = newToken(token.RPAREN, self.ch)
		elif self.ch == ',':
			tok = newToken(token.COMMA, self.ch)
		elif self.ch == '+':
			tok = newToken(token.PLUS, self.ch)
		elif self.ch == '{':
			tok = newToken(token.LBRACE, self.ch)
		elif self.ch == '}':
			tok = newToken(token.RBRACE, self.ch)
		#elif self.ch == 0:
		elif self.ch == '':
			"""
			tok.Literal == ""
			tok.Type = token.EOF
			"""
			tok = newToken(token.EOF, self.ch)
		elif self.ch == '"':
			"""
			tok.Type = token.STRING
			tok.Literal = self.readString()
			"""
			tok = newToken(token.STRING, self.readString())
		elif self.ch == '[':
			tok = newToken(token.LBRACKET, self.ch)
		elif self.ch == ']':
			tok = newToken(token.RBRACKET, self.ch)
		elif self.ch == ':':
			tok = newToken(token.COLON, self.ch)
		else:
			if isLetter(self.ch):
				
				Literal = self.readIdentifier()
				Type = token.LookupIdent(Literal)
				
				
				tok = token.Token(Type, Literal)
				#print("pass isLetter()")
				#tok.printout()
				
				return tok
			elif isDigit(self.ch):
				#print("isDisit()")
				#tok.Type = token.INT
				#tok.Literal = self.readNumber()
				
				tok = token.Token(token.INT, self.readNumber())
				return tok
			else:
				tok = token.Token(token.ILLEGAL, self.ch)
		
		self.readChar()
		
		return tok

	def readNumber(self):
		self.p = self.position
		while isDigit(self.ch):
			self.readChar()
			#print("readNumber() pos", ":", self.p, ":", self.position)
			
		#print("readNumber(): ", self.input[self.p:self.position])
		return self.input[self.p:self.position]
		
	def readIdentifier(self):
		self.p = self.position
		while isLetter(self.ch):
			self.readChar()
			#print("readIdentifier() pos: ", self.p, ":", self.position)
		#print("readIdentifier(): ", self.input[self.p:self.position])
		
		return self.input[self.p:self.position]
	
	def peekChar(self):
		if self.readPosition >= len(self.input):
			return ''
			#return 0
		else:
			return self.input[self.readPosition]
	
	def readString(self):
		self.p = self.position + 1
		while True:
			self.readChar()
			if self.ch == '"' or self.ch == '':
				break
		
		#print("readString(): ", self.p, self.position)
		
		return self.input[self.p:self.position]
		
		
def New(input):
	ret = Lexer()
	ret.input = input
	ret.readChar()
	return ret

def isDigit(ch):
	return '0' <= str(ch) and str(ch) <= '9'

def isLetter(ch):
	#return 'a' <= ch and ch <= 'z' or 'A' <= ch and ch < 'Z' or ch == '_'
	return 'a' <= str(ch) and str(ch) <= 'z' or 'A' <= str(ch) and str(ch) < 'Z' or str(ch) == '_'

def newToken(tokenType, ch):
	#return token.Token(tokenType, ch)
	return token.Token(tokenType, str(ch))

def testlex(lex):
	print(lex.input)
	
	while True:
		tok = lex.NextToken()
		tok.printout()
		if lex.ch == "":
			break
	
		
if __name__ == "__main__":
	#l = Lexer()
	#l.input = (""   H   e   l   l   o w   orld"")
	
	lex1 = New("let five = 53;")
	testlex(lex1)
	
	l = Lexer()
	l.input = "let five = 53;"
	testlex(l)
	
	"""
	line = input()
	lex2 = Lexer()
	lex2.input = line
	testlex(lex2)
	"""
	"""
	lex3 = New("let add = fn (x, y) {x + y;};")
	testlex(lex3)
	"""
	"""
	lex4 = New("1234")
	testlex(lex4)
	"""
	"""
	lex5 = New("fn")
	testlex(lex5)
	"""
	"""
	lex6 = New("hello world")
	testlex(lex6)
	"""
	
	lex7 = New("\"hello\"")
	testlex(lex7)
	