# -*- coding: utf-8 -*-

import token

class Node:
	def TokenLiteral(self):
		pass
		
	def String(self):
		pass

class Statement(Node):
	def TokenLiteral(self):
		pass
		
	def statementNode(self):
		pass

class Expression(Node):
	def TokenLiteral(self):
		pass

	def expressionNode(self):
		pass
	"""
	def String(self):
		out = ""
		out += "call Expression::String()"
		
		return out
	"""
	
class Program:
	def __init__(self):
		self.Statements = []
	
	def TokenLiteral(self):
		if len(self.Statements) > 0:
			return self.Statements[0].TokenLiteral()
		else:
			return ""

	def String(self):
		self.out = ""
		
		i = 0
		while i < len(self.Statements):
			self.out += self.Statements[i].String()
			i += 1
		
		return self.out

class LetStatement:
	def __init__(self):
		self.Token = None		# token.pyのTokenクラス
		self.Name = None
		self.Value = None
	
	def statementNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def printout(self):
		print("LetSatement: ", self.Token, ":", self.Name, ":", self.Value)
	
	def String(self):
		self.out = ""
		self.out += self.TokenLiteral()
		self.out += " "
		self.out += self.Name.String()
		self.out += " = "
		
		if self.Value != None:
			self.out += self.Value.String()
		
		
		self.out += ";"
		
		return self.out
	
class Identifier:
	def __init__(self):
		self.Token = None
		self.Value = None		# self.Value = ""
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
		
	def String(self):
		return self.Value

class ReturnStatement:
	def __init__(self):
		self.Token = None
		self.ReturnValue = None
	
	def statementNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def printout(self):
		print("ReturnSatement: ", self.Token, ":", self.ReturnValue)
	
	def String(self):
		self.out = ""
		self.out += self.TokenLiteral()
		self.out += " "
		
		if self.ReturnValue != None:
			self.out += self.ReturnValue.String()
		
		self.out += ";"
	
		return self.out
		
class ExpressionStatement:
	def __init__(self):
		self.Token = None
		self.Expression = None
	
	def statementNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal

	def String(self):
		if self.Expression != None:
			return self.Expression.String()
		
		return ""
		
class IntegerLiteral:
	def __init__(self):
		self.Token = None
		self.Value = None
		# self.Value = 0
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		return self.Token.Literal

class PrefixExpression:
	def __init__(self):
		self.Token = None
		self.Operator = ""
		self.Right = None
	
	def expressionNode(self):
		pass
		
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		self.out = ""
		self.out += "("
		self.out += self.Operator
		self.out += self.Right.String()
		self.out += ")"
		
		return self.out
	
class InfixExpression:
	def __init__(self):
		self.Token = None
		self.Left = None
		self.Operator = ""
		self.Right = None
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		print("InfixExpression::String(): ", self.Left, self.Right)
		
		self.out = ""
		self.out += "("
		self.out += self.Left.String()
		self.out += " " + self.Operator + " "
		self.out += self.Right.String()
		self.out += ")"
		
		return self.out
	
class Boolean:
	def __init__(self):
		self.Token = None
		self.Value = None
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		return self.Token.Literal

class IfExpression:
	def __init__(self):
		self.Token = None
		self.Condition = None
		self.Consequence = None
		self.Alternative = None
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		
		out += "if"
		out += self.Condition.String()
		out += " "
		out += self.Consequence.String()
	
		if self.Alternative != None:
			out += "else "
			out += self.Alternative.String()
		
		return out

class BlockStatement:
	def __init__(self):
		self.Token = None
		self.Statements = []
	
	def statementNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		
		i = 0
		while i < len(self.Statements):
			out += self.Statements[i].String()
			i += 1
		
		return out

class FunctionLiteral:
	def __init__(self):
		self.Token = None
		self.Parameters = []
		self.Body = None
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		
		i = 0
		params = []
		while i < len(self.Parameters):
			params.append(self.Parameters[i].String())
			i += 1
		
		out += self.TokenLiteral()
		out += "("
		out += ",".join(params)
		out += ") "
		out += self.Body.String()
		
		return out
	
class CallExpression:
	def __init__(self):
		self.Token = None
		self.Function = None
		self.Arguments = []
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		args = []
		
		i = 0
		while i < len(self.Arguments):
			args.append(self.Arguments[i].String())
			i += 1
		
		out += self.Function.String()
		out += "("
		out += ", ".join(args)
		out += ")"
		
		return out


class StringLiteral:
	def __init__(self):
		self.Token = None
		self.Value = ""
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		return self.Token.Literal

	
class ArrayLiteral:
	def __init__(self):
		self.Token = None
		self.Elements = []
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		elements = []
		for el in self.Elements:
			elements.append(el.String())
		out += "["
		out += ", ".join.elements
		out += "]"
		return out

class IndexExpression:
	def __init__(self):
		self.Token = None
		self.Left = None
		self.Index = None
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		out += "("
		out += self.Left.String()
		out += "["
		out += self.Index.String()
		out += "])"
		
		return out
	
class HashLiteral:
	def __init__(self):
		self.Token = None
		self.Pairs = {}
	
	def expressionNode(self):
		pass
	
	def TokenLiteral(self):
		return self.Token.Literal
	
	def String(self):
		out = ""
		pairs = []
		
		for key in self.Pairs:
			pairs.append(str(key) + ":" + str(self.Pairs[key]))
		
		out += "{"
		out += ", ".join(pairs)
		out += "}"
		
		return out
		
if __name__ == "__main__":
	n = Node()
	