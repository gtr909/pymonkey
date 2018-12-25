# -*- coding: utf-8 -*-

import ast
import lexer
import token
import evaluator

LOWEST		= 1
EQUALS		= 2
LESSGREATER = 3
SUM			= 4
PRODUCT		= 5
PREFIX		= 6
CALL		= 7
INDEX		= 8

precedences = {
	token.EQ:		EQUALS,
	token.NOT_EQ:	EQUALS,
	token.LT:		LESSGREATER,
	token.GT:		LESSGREATER,
	token.PLUS:		SUM,
	token.MINUS:	SUM,
	token.SLASH:	PRODUCT,
	token.ASTERISK:	PRODUCT,
	token.LPAREN:	CALL,
	token.LBRACKET:	INDEX,
}


	
class Parser:
	def  __init__(self, inputstr):
		#self.l = lexer.Lexer()
		#self.l.input = inputstr
		#self.l.readChar() # lexer.New()の中で1回readCharを呼んでいる
		
		self.l = lexer.New(inputstr)
		self.curToken = None # token.Token("", "")
		self.peekToken = None # token.Token("", "")
		
		#self.nextToken()
		#self.nextToken()
		
		#self.errors = []
		
		print("Parser.__init__():", self.l.input)
		print("Parser.__init__():", self.l)
		"""
		self.prefixParseFns = {}
		self.registerPrefix(token.IDENT, self.parseIdentifier)
		self.registerPrefix(token.INT, self.parseIntegerLiteral)
		self.registerPrefix(token.BANG, self.parsePrefixExpression)
		self.registerPrefix(token.MINUS, self.parsePrefixExpression)
		self.registerPrefix(token.TRUE, self.parseBoolean)
		self.registerPrefix(token.FALSE, self.parseBoolean)
		self.registerPrefix(token.LPAREN, self.parseGroupedExpression)
		self.registerPrefix(token.IF, self.parseIfExpression)
		self.registerPrefix(token.FUNCTION, self.parseFunctionLiteral)
		self.registerPrefix(token.STRING, self.parseStringLiteral)
		self.registerPrefix(token.LBRACKET, self.parseArrayLiteral)
		self.registerPrefix(token.LBRACE, self.parseHashLiteral)
		
		
		self.infixParseFns = {}
		self.registerInfix(token.PLUS, self.parseInfixExpression)
		self.registerInfix(token.MINUS, self.parseInfixExpression)
		self.registerInfix(token.SLASH, self.parseInfixExpression)
		self.registerInfix(token.ASTERISK, self.parseInfixExpression)
		self.registerInfix(token.EQ, self.parseInfixExpression)
		self.registerInfix(token.NOT_EQ, self.parseInfixExpression)
		self.registerInfix(token.LT, self.parseInfixExpression)
		self.registerInfix(token.GT, self.parseInfixExpression)
		self.registerInfix(token.LPAREN, self.parseCallExpression)
		self.registerInfix(token.LBRACKET, self.parseIndexExpression)
		"""
		
	def nextToken(self):
		self.curToken = self.peekToken
		self.peekToken = self.l.NextToken()
		
		print("nextToken(): ", self.curToken, " : ", self.peekToken)
	
	def ParseProgram(self):
		program = ast.Program()
		program.Statements = []
		
		self.curToken.printout()
		
		print("ParseProgram(): ", self.curToken.Type)
		
		while self.curToken.Type != token.EOF:
			stmt = self.parseStatement()
			print("ParseProgram(): ", stmt)
			if stmt != None:
				program.Statements.append(stmt)
			self.nextToken()
		
		print("ParseProgram(): ", program)
		
		return program
	
	def parseStatement(self):
		if self.curToken.Type == token.LET:
			return self.parseLetStatement()
		elif self.curToken.Type == token.RETURN:
			return self.parseReturnStatement()
		else:
			return self.parseExpressionStatement()
	
	def parseLetStatement(self):
	
		print("parseLetStatement(): ", self.curToken)
		
		stmt = ast.LetStatement()
		stmt.Token = self.curToken
		
		print("parseLetStatement(): ", stmt)
		stmt.printout()
		
		if not self.expectPeek(token.IDENT):
			return None
		
		stmt.Name = ast.Identifier()
		stmt.Name.Token = self.curToken
		stmt.Name.Value = self.curToken.Literal
		stmt.printout()
		
		if not self.expectPeek(token.ASSIGN):
			return None
		"""
		while not self.curTokenIs(token.SEMICOLON):
			self.nextToken()
		"""
		self.nextToken()
		
		stmt.Value = self.parseExpression(LOWEST)
		
		if self.peekTokenIs(token.SEMICOLON):
			self.nextToken()
		
		return stmt
	
	def parseReturnStatement(self):
		stmt = ast.ReturnStatement()
		stmt.Token = self.curToken
		
		self.nextToken()
		
		"""
		while not self.curTokenIs(token.SEMICOLON):
			self.nextToken()
		"""
		
		stmt.ReturnValue = self.parseExpression(LOWEST)
		
		if self.peekTokenIs(token.SEMICOLON):
			self.nextToken()
		
		return stmt
		
	
	def parseExpressionStatement(self):
		stmt = ast.ExpressionStatement()
		stmt.Token = self.curToken
		stmt.Expression = self.parseExpression(LOWEST)
		if self.peekTokenIs(token.SEMICOLON):
			self.nextToken()
		
		return stmt
		
	def parseExpression(self, precedence):
		print("parseExpression(): ", precedence)
		print("parseExpression(): ", self.curToken.Type)
		
		prefix = self.prefixParseFns[self.curToken.Type]
		print("parseExpression(): ", prefix)
		
		if prefix == None:
			self.noPrefixParseFnError(self.curToken.Type)
			return None
		
		leftExp = prefix()
		print("parseExpression(): ", leftExp)
		
		while not self.peekTokenIs(token.SEMICOLON) and precedence < self.peekPrecedence():
			infix = self.infixParseFns[self.peekToken.Type]
			if infix == None:
				return leftExp
			self.nextToken()
			
			leftExp = infix(leftExp)
		
		return leftExp
		
	def curTokenIs(self, t):
		return self.curToken.Type == t
	
	def peekTokenIs(self, t):
		return self.peekToken.Type == t
	
	def expectPeek(self, t):
		if self.peekTokenIs(t) == True:
			self.nextToken()
			return True
		else:
			self.peekError(t)
			return False
	
	def Errors(self):
		return self.errors
	
	def peekError(self, t):
		msg = "expected next token to be " + str(t) + " , got " + str(self.peekToken.Type) + " instead"
		print(msg)
		self.errors.append(msg)
	
	def registerPrefix(self, tokenType, fn):
		self.prefixParseFns[tokenType] = fn
		#self.prefixParseFns = {tokenType:fn}
	
	def registerInfix(self, tokenType, fn):
		self.infixParseFns[tokenType] = fn
	
	def parseIdentifier(self): 
		ret = ast.Identifier()
		ret.Token = self.curToken
		ret.Value = self.curToken.Literal
		
		return ret
	
	def parseIntegerLiteral(self):
		lit = ast.IntegerLiteral()
		lit.Token = self.curToken
		
		lit.Value = int(self.curToken.Literal)
		
		return lit
		
	def noPrefixParseFnError(self, t):
		msg = "no prefix parse function for " + t + " found"
		self.errors.append(msg)
	
	def parsePrefixExpression(self):
		expression = ast.PrefixExpression()
		expression.Token = self.curToken
		expression.Operator = self.curToken.Literal
		
		self.nextToken()
		
		expression.Right = self.parseExpression(PREFIX)
		
		return expression
	
	def peekPrecedence(self):
		print("peekPrecedence(): ", self.peekToken.Type)
		
		#if self.peekToken.Type != token.EOF:
		if self.peekToken.Type in precedences:
			return precedences[self.peekToken.Type]
		return LOWEST
	
	def curPrecedence(self):
		#if precedences[self.curToken.Type] != None:
		#if self.curToken.Type != token.EOF:
		if self.curToken.Type in precedences:
			return precedences[self.curToken.Type]
		return LOWEST
	
	def parseInfixExpression(self, left):
		expression = ast.InfixExpression()
		expression.Token = self.curToken
		expression.Operator = self.curToken.Literal
		expression.Left = left
		
		precedence = self.curPrecedence()
		self.nextToken()
		expression.Right = self.parseExpression(precedence)
		
		return expression
	
	def parseBoolean(self):
		b = ast.Boolean()
		b.Token = self.curToken
		b.Value = self.curTokenIs(token.TRUE)
		
		return b
		
	def parseGroupedExpression(self):
		self.nextToken()
		exp = self.parseExpression(LOWEST)
		if not self.expectPeek(token.RPAREN):
			return None
		
		return exp
	
	def parseIfExpression(self):
		expression = ast.IfExpression()
		expression.Token = self.curToken
		
		if not self.expectPeek(token.LPAREN):
			return None
		
		self.nextToken()
		expression.Condition = self.parseExpression(LOWEST)
		
		if not self.expectPeek(token.RPAREN):
			return None
		
		if not self.expectPeek(token.LBRACE):
			return None
		
		expression.Consequence = self.parseBlockStatement()
		
		if self.peekTokenIs(token.ELSE):
			self.nextToken()
			if not self.expectPeek(token.LBRACE):
				return None
			
			expression.Alternative = self.parseBlockStatement()
		
		return expression
	
	def parseBlockStatement(self):
		block = ast.BlockStatement()
		block.Statements = []
		
		self.nextToken()
		
		while not self.curTokenIs(token.RBRACE) and not self.curTokenIs(token.EOF):
			stmt = self.parseStatement()
			if stmt != None:
				block.Statements.append(stmt)
			self.nextToken()
		
		return block
	
	def parseFunctionLiteral(self):
		lit = ast.FunctionLiteral()
		lit.Token = self.curToken
		
		if not self.expectPeek(token.LPAREN):
			return None
		
		lit.Parameters = self.parseFunctionParameters()
		
		if not self.expectPeek(token.LBRACE):
			return None
		
		lit.Body = self.parseBlockStatement()
		
		return lit
	
	def parseFunctionParameters(self):
		identifiers = []
		
		if self.peekTokenIs(token.RPAREN):
			self.nextToken()
			return identifiers
		
		self.nextToken()
		
		ident = ast.Identifier()
		ident.Token = self.curToken
		ident.Value = self.curToken.Literal
		identifiers.append(ident)
		
		while self.peekTokenIs(token.COMMA):
			self.nextToken()
			self.nextToken()
			ident = ast.Identifier()
			ident.Token = self.curToken
			ident.Value = self.curToken.Literal
			identifiers.append(ident)
		
		if not self.expectPeek(token.RPAREN):
			return None
		
		return identifiers
	
	def parseCallExpression(self, function):
		exp = ast.CallExpression()
		exp.Token = self.curToken
		exp.Function = function
		#exp.Arguments = self.parseCallArguments()
		exp.Arguments = self.parseExpressionList(token.RPAREN)
		
		return exp
	
	def parseCallArguments(self):
		args = []
		
		if self.peekTokenIs(token.RPAREN):
			self.nextToken()
			return args
		
		self.nextToken()
		args.append(self.parseExpression(LOWEST))
		
		while self.peekTokenIs(token.COMMA):
			self.nextToken()
			self.nextToken()
			args.append(self.parseExpression(LOWEST))
		
		if not self.expectPeek(token.RPAREN):
			return None
		
		
		return args
	
	def parseStringLiteral(self):
		ret = ast.StringLiteral()
		ret.Token = self.curToken
		ret.Value = self.curToken.Literal
		return ret
	
	def parseArrayLiteral(self):
		ret = ast.ArrayLiteral()
		ret.Token = self.curToken
		ret.Elements = self.parseExpressionList(token.RBRACKET)
		
		return ret
	
	def parseExpressionList(self, end):
		lst = []
		
		if self.peekTokenIs(end):
			self.nextToken()
			return lst
		
		self.nextToken()
		lst.append(self.parseExpression(LOWEST))
		
		while self.peekTokenIs(token.COMMA):
			self.nextToken()
			self.nextToken()
			lst.append(self.parseExpression(LOWEST))
		
		if not self.expectPeek(end):
			#return None #? NULL
			return evaluator.NULL
		
		return lst
	
	def parseIndexExpression(self, left):
		exp = ast.IndexExpression()
		exp.Token = self.curToken
		exp.Left = left
		
		self.nextToken()
		exp.Index = self.parseExpression(LOWEST)
		
		if not self.expectPeek(token.RBRACKET):
			#return None
			return evaluator.NULL ## ?
		
		return exp
	
	def parseHashLiteral(self):
		hash = ast.HashLiteral()
		hash.Token = self.curToken
		hash.Pairs = {}
		
		while not self.peekTokenIs(token.RBRACE):
			self.nextToken()
			key = self.parseExpression(LOWEST)
			if not self.expectPeek(token.COLON):
				return evaluator.NULL
			
			self.nextToken()
			value = self.parseExpression(LOWEST)
			
			hash.Pairs[key] = value
			
			if not self.peekTokenIs(token.RBRACE) and not self.expectPeek(token.COMMA):
				return evaluator.NULL
		
		if not self.expectPeek(token.RBRACE):
			return evaluator.NULL
		
		return hash
		
def New(l):
	p = Parser("")
	p.l = l
	p.errors = []
	p.prefixParseFns = {}
	p.registerPrefix(token.IDENT, p.parseIdentifier)
	p.registerPrefix(token.INT, p.parseIntegerLiteral)
	p.registerPrefix(token.BANG, p.parsePrefixExpression)
	p.registerPrefix(token.MINUS, p.parsePrefixExpression)
	p.registerPrefix(token.TRUE, p.parseBoolean)
	p.registerPrefix(token.FALSE, p.parseBoolean)
	p.registerPrefix(token.LPAREN, p.parseGroupedExpression)
	p.registerPrefix(token.IF, p.parseIfExpression)
	p.registerPrefix(token.FUNCTION, p.parseFunctionLiteral)
	p.registerPrefix(token.STRING, p.parseStringLiteral)
	p.registerPrefix(token.LBRACKET, p.parseArrayLiteral)
	p.registerPrefix(token.LBRACE, p.parseHashLiteral)
		
	p.infixParseFns = {}
	p.registerInfix(token.PLUS, p.parseInfixExpression)
	p.registerInfix(token.MINUS, p.parseInfixExpression)
	p.registerInfix(token.SLASH, p.parseInfixExpression)
	p.registerInfix(token.ASTERISK, p.parseInfixExpression)
	p.registerInfix(token.EQ, p.parseInfixExpression)
	p.registerInfix(token.NOT_EQ, p.parseInfixExpression)
	p.registerInfix(token.LT, p.parseInfixExpression)
	p.registerInfix(token.GT, p.parseInfixExpression)
	p.registerInfix(token.LPAREN, p.parseCallExpression)
	p.registerInfix(token.LBRACKET, p.parseIndexExpression)
	
	p.nextToken()
	p.nextToken()
	
	return p

if __name__ == "__main__":
	p1 = Parser("foobar")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	
	p1 = Parser("let five = 5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("return 5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("1235;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("-5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("!5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("5 + 5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("false;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("(5 + 5) * 2;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("if (x < y) {x} else {y};")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("fn(x, y) {return x + y;};")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("a + add(b * c) + d;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	
	p1 = Parser("true == false;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	"""
	print("---------------------------------")
	
	p1 = Parser("\"hello\"")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	"""
	
	"""
	test2 = p1.parseStatement()
	print("test2: ", test2)
	"""
	"""
	test1 = p1.parseLetStatement()
	print("test1: ", test1)
	"""
	"""
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	"""
	"""
	test4 = p1.nextToken()
	print("test4: ", test4)
	"""
	"""
	lex1 = lexer.New("let five = 53;")
	lexer.testlex(lex1)
	"""
	"""
	print("---------------------------------")
	p1 = Parser("let x 5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	p1 = Parser("let = 5;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	
	print("---------------------------------")
	p1 = Parser("let 123;")
	test3 = p1.ParseProgram()
	print("test3: ", test3)
	"""