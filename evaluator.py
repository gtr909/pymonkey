# -*- coding: utf-8 -*-

import ast
import object
import environment
#import builtins
import copy

NULL = object.Null()
TRUE = object.Boolean(True)   
FALSE = object.Boolean(False) 

def funcname_puts(args):
	print("funcname_puts(): ", args, type(args))
	for arg in args:
		print(arg.Inspect())
	
	return NULL

def funcname_push(args):
	print("funcname_push()1: ", args, type(args))
	print("funcname_push()2: ", args[0], type(args[0]))
	print("funcname_push()3: ", args[1], type(args[1]))
	
	if len(args) != 2:
		return newError("wrong number of arguments ", len(args))
	if args[0].Type() != object.ARRAY_OBJ:
		return newError("argument to first must be ARRAY, got ", args[0].Type())
	
	arr = args[0]
	length = len(arr.Elements)
	
	newElements = []
	newElements = copy.copy(arr.Elements)
	newElements.append(args[1])
	
	ret = object.Array()
	ret.Elements = newElements
	
	return ret


def funcname_rest(args):
	if len(args) != 1:
		return newError("wrong number of arguments ", len(args))
	if args[0].Type() != object.ARRAY_OBJ:
		return newError("argument to first must be ARRAY, got ", args[0].Type())
	
	arr = args[0]
	length = len(arr.Elements)
	if length > 0:
		newElements = []
		
		#newElements = arr.Elements[1:length] #参照してるだけになる
		newElements = copy.copy(arr.Elements[1:length])
		
		ret = object.Array()
		ret.Elements = newElements
		
		return ret
	
	return NULL


def funcname_last(args):
	if len(args) != 1:
		return newError("wrong number of arguments ", len(args))
	if args[0].Type() != object.ARRAY_OBJ:
		return newError("argument to first must be ARRAY, got ", args[0].Type())
	
	arr = args[0]
	length = len(arr.Elements)
	if length > 0:
		return arr.Elements[length - 1]
	
	return NULL



def funcname_first(args):
	print("funcname_first()1: ", args, type(args))
	print("funcname_first()2: ", args[0], type(args[0]))
	
	if len(args) != 1:
		return newError("wrong number of arguments ", len(args))
	if args[0].Type() != object.ARRAY_OBJ:
		return newError("argument to first must be ARRAY, got ", args[0].Type())
	
	arr = args[0]
	if len(arr.Elements) > 0:
		return arr.Elements[0]
	
	return NULL

def funcname_len(args):
	print("funcname_len()1: ", args, type(args))
	#print("funcname_len()2: ", args[0], type(args[0]))
	
	if len(args) != 1:
		return newError("wrong number of arguments ", len(args))
	
	arg = type(args[0])
	
	print("funcname_len()3: ", arg, type(arg))
	print("funcname_len()4: ", args[0], type(args[0]))
	
	if arg == object.String:
		ret = object.Integer()
		ret.Value = int(len(args[0].Value))
		return ret
	elif arg == object.Array:
		ret = object.Integer()
		ret.Value = int(len(args[0].Elements))
		return ret
	elif arg == list:
		print("funcname_len()5: ", args, type(args))
		print("funcname_len()6: ", args[0], type(args[0]))
		
		ret = object.Integer()
		ret.Value = int(len(args[0]))
		return ret
	###############################################################
	# len関数に未束縛の引数を渡したときのエラー処理
	elif arg == object.Error:
		return newError("funcname_len()7: ", str(args[0].Message))
	###############################################################
	else:
		return newError("argument to len not supported ", type(args[0]))


ret0 = object.Builtin()
ret0.Fn = funcname_len

ret1 = object.Builtin()
ret1.Fn = funcname_first

ret2 = object.Builtin()
ret2.Fn = funcname_last

ret3 = object.Builtin()
ret3.Fn = funcname_rest

ret4 = object.Builtin()
ret4.Fn = funcname_push

ret5 = object.Builtin()
ret5.Fn = funcname_puts

BUILTINS = {"len":ret0, "first":ret1, "last":ret2, "rest":ret3, "push":ret4, "puts":ret5,}


def Eval(node, env):
	print("Eval(): ", type(node))
	#print("Eval(): ", ast.IntegerLiteral)

	typenode = type(node)
	if typenode == ast.Program:
		#return evalStatements(node.Statements)
		return evalProgram(node, env)
	elif typenode == ast.ExpressionStatement:
		return Eval(node.Expression, env)
	elif typenode == ast.IntegerLiteral:
		ret = object.Integer()
		ret.Value = node.Value
		return ret
	elif typenode == ast.Boolean:
		"""
		ret = object.Boolean()
		ret.Value = node.Value
		return ret
		"""
		return nativeBoolToBooleanObject(node.Value)
	elif typenode == ast.PrefixExpression:
		right = Eval(node.Right, env)
		
		if isError(right):
			return right
		
		return evalPrefixExpression(node.Operator, right)
	elif typenode == ast.InfixExpression:
		left = Eval(node.Left, env)
		
		if isError(left):
			return left
		
		right = Eval(node.Right, env)
		
		if isError(right):
			return right
			
		return evalInfixExpression(node.Operator, left, right)
	elif typenode == ast.BlockStatement:
		#return evalStatements(node.Statements)
		return evalBlockStatement(node, env)
	elif typenode == ast.IfExpression:
		return evalIfExpression(node, env)
	elif typenode == ast.ReturnStatement:
		val = Eval(node.ReturnValue, env)
		
		if isError(val):
			return val
		
		ret = object.ReturnValue()
		ret.Value = val
		return ret
	elif typenode == ast.LetStatement:
		val = Eval(node.Value, env)
		if isError(val):
			return val
		
		###
		#ここで何をする
		env.Set(node.Name.Value, val)
		###
		
	elif typenode == ast.Identifier:
		return evalIdentifier(node, env)
	elif typenode == ast.FunctionLiteral:
		params = node.Parameters
		body = node.Body
		ret = object.Function()
		ret.Parameters = params
		ret.Env = env
		ret.Body = body
		
		return ret
	elif typenode == ast.CallExpression:
		function = Eval(node.Function, env)
		if isError(function):
			return function
		args = evalExpressions(node.Arguments, env)
		
		print("Eval():ast.CallExpression:1 ", args, type(args))
		#print("Eval():ast.CallExpression:2 ", args[0])
		
		###############################################
		# len(letで束縛してない変数)のエラーを補足
		# e.g. len(ghy) 2019/01/22 21:44
		#if type(args) == object.Error:
		#	return newError("identifier not found: ")
		###############################################
		
		if len(args) == 1 and isError(args[0]):
			return args[0]
		
		return applyFunction(function, args)
	elif typenode == ast.StringLiteral:
		ret = object.String()
		ret.Value = node.Value
		return ret
	elif typenode == ast.ArrayLiteral:
		elements = evalExpressions(node.Elements, env)
		
		print("Eval():ast.ArrayLiteral:", elements, type(elements))
		
		if len(elements) == 1 and isError(elements[0]):
			return elements[0]
		ret = object.Array()
		ret.Elements = elements
		
		return ret
	elif typenode == ast.IndexExpression:
		left = Eval(node.Left, env)
		if isError(left):
			return left
		index = Eval(node.Index, env)
		if isError(index):
			return index
		
		return evalIndexExpression(left, index)
	elif typenode == ast.HashLiteral:
		return evalHashLiteral(node, env)
	else:
		#return None # NULL?
		return NULL
	
def nativeBoolToBooleanObject(input):
	if input:
		return TRUE
	else:
		return FALSE

def evalStatements(stmts): # env引数をいつ扱う？
	result = None
	
	for statement in stmts:
		result = Eval(statement)
		
		print("evalStatements(): ", statement)
		print("evalStatements(): ", result)
		
		returnValue = result.object.ReturnValue #######???
		print("evalStatements(): ", returnValue)
		#if returnValue != None:#############
		if returnValue != NULL:
			return returnValue.Value
			
	return result

def evalPrefixExpression(operator, right):
	if operator == "!":
		return evalBangOperatorExpression(right)
	elif operator == "-":
		return evalMinusPrefixOperatorExpression(right)
	else:
		return newError("unknown operator: ", str(operator), right.Type())
		#return NULL

def evalBangOperatorExpression(right):
	if right == TRUE:
		return FALSE
	elif right == FALSE:
		return TRUE
	elif right == NULL:
		return TRUE
	else:
		return FALSE

def evalMinusPrefixOperatorExpression(right):
	if right.Type() != object.INTEGER_OBJ:
		return newError("unknown operator: -", right.Type())
		#return NULL
	
	print("evalMinusPrefixOperatorExpression(): ", right)
	
	value = right.Value
	
	print("evalMinusPrefixOperatorExpression(): ", value)
	
	ret = object.Integer()
	ret.Value = -value
	return ret
	
def evalInfixExpression(operator, left, right):
	print("evalInfixExpression()1: ", left)
	print("evalInfixExpression()2: ", right)
	if type(left) == int or type(right) == int: # or type(left) == bool or type(right) == bool:
		print("evalInfixExpression()3: pass")
		return evalIntegerInfixExpression(operator, left, right)
	else:
		if left.Type() == object.INTEGER_OBJ and right.Type() == object.INTEGER_OBJ:
			return evalIntegerInfixExpression(operator, left, right)
		elif operator == "==":
			return nativeBoolToBooleanObject(left == right)
		elif operator == "!=":
			return nativeBoolToBooleanObject(left != right)
		elif left.Type() != right.Type():
			return newError("type mismatch: ", left.Type(), str(operator), right.Type())
		elif left.Type() == object.STRING_OBJ and right.Type() == object.STRING_OBJ:
			return evalStringInfixExpression(operator, left, right)
		else:
			return newError("unknown operator: ", left.Type(), str(operator), right.Type())
			#return NULL
	
def evalIntegerInfixExpression(operator, left, right):
	print("evalIntegerInfixExpression(): ", left, right)
	
	leftVal = 0
	rightVal = 0
	
	if type(left) == int:
		leftVal = left
	elif type(right) == int:
		rightVal = right
	else:
		leftVal = left.Value
		#leftVal = left.object.Integer.Value
		rightVal = right.Value
		#rightVal = right.object.Integer.Value
	
	if operator == "+":
		ret = object.Integer()
		ret.Value = leftVal + rightVal
		return ret
	elif operator == "-":
		ret = object.Integer()
		ret.Value = leftVal - rightVal
		return ret
	elif operator == "*":
		ret = object.Integer()
		ret.Value = leftVal * rightVal
		return ret
	elif operator == "/":
		if rightVal == 0:
			return newError("0 divide: ", left.Type(), str(operator), right.Type())
		ret = object.Integer()
		ret.Value = leftVal // rightVal
		return ret
	elif operator == "<":
		return nativeBoolToBooleanObject(leftVal < rightVal)
	elif operator == ">":
		return nativeBoolToBooleanObject(leftVal > rightVal)
	elif operator == "==":
		return nativeBoolToBooleanObject(leftVal == rightVal)
	elif operator == "!=":
		return nativeBoolToBooleanObject(leftVal != rightVal)
	else:
		return newError("unknown operator: ", left.Type(), str(operator), right.Type())
		#return NULL

def evalIfExpression(ie, env):
	condition = Eval(ie.Condition, env)
	
	if isError(condition):
		return condition
	
	if isTruthy(condition):
		return Eval(ie.Consequence, env)
	#elif ie.Alternative != None: #########
	elif ie.Alternative != NULL: #########
		return Eval(ie.Alternative, env)
	else:
		return NULL

# Trueかtrueか
def isTruthy(obj):
	if obj == NULL:
		return False
	elif obj == TRUE:
		return True
	elif obj == FALSE:
		return False
	else:
		return True

def evalProgram(program, env):
	result = None
	for statement in program.Statements:
		result = Eval(statement, env)
		
		print("evalProgram(): ", statement)
		print("evalProgram(): ", result)
		
		#returnValue = result.Value
		"""
		returnValue = result
		if returnValue != None:
			return returnValue.Value
		"""
		typeresult = type(result)
		if typeresult == object.ReturnValue:
			return result.Value
		elif typeresult == object.Error:
			return result
			
	return result

def evalBlockStatement(block, env):
	result = None
	for statement in block.Statements:	
		result = Eval(statement, env)
		"""
		if result != None and result.Type() == object.RETURN_VALUE_OBJ:
			return result
		"""
		#if result != None:###
		if result != NULL:###
			rt = result.Type()
			if rt == object.RETURN_VALUE_OBJ or rt == object.ERROR_OBJ:
				return result
	
	return result

def newError(format, *arg):
	ret = object.Error()
	
	errmsg = format
	for m in arg:
		errmsg += str(m)
	
	ret.Message = errmsg
	
	return ret
	
def isError(obj):
	print("isError(): ", obj)
	if type(obj) == int:
		return False
	elif type(obj) == bool:
		return False
	###############################################
	# len(abc)束縛してない変数をエラー処理するため
	elif type(obj) == object.Error:
		return False
	###############################################
	#elif obj != None:
	elif obj != NULL:
		return obj.Type() == object.ERROR_OBJ
	
	return False

def evalIdentifier(node, env):
	# Page187まではOK
	"""
	print("evalIdentifier():1 ", node, type(node))
	val = env.Get(node.Value)
	print("evalIdentifier():2 ", node.Value, type(node.Value))
	print("evalIdentifier():3 ", val, type(val))
	#if val == None:
	if val == NULL:
		print("evalIdentifier():4 ", "pass")
		return newError("identifier not found: " + str(node.Value))
	else:
		return val
	"""
	
	print("evalIdentifier():1 ", node, type(node))
	print("evalIdentifier():2 ", node.Value, type(node.Value))
	val = env.Get(node.Value)
	print("evalIdentifier():3 ", val, type(val))
	
	if val != NULL:
		return val
	elif node.Value in BUILTINS:
		builtin = BUILTINS[node.Value]
		print("evalIdentifier():4 ", builtin, type(builtin))
		return builtin
	else:
		print("evalIdentifier():5 ", val, type(val))
		return newError("identifier not found: " + str(node.Value))
	

def evalExpressions(exps, env):
	result = []
	
	for e in exps:
		print("evalExpressions():1 ", e, type(e))
		evaluated = Eval(e, env)
		print("evalExpressions():2 ", evaluated, type(evaluated))
		if isError(evaluated):
			print("evalExpressions():3 ", evaluated)
			#return []object.Object{evaluated}##
			# result.append(evaluated) ####???
			# return result            ####???
			return evaluated ###
			
		result.append(evaluated)
		
	print("evalExpressions():4 ", result, type(result))
	return result

def applyFunction(fn, args):
	# 組み込み関数が動かない
	# let関数定義が動く
	"""
	print("applyFunction(): ", fn)
	function = fn ########
	if function == NULL:
		return newError("not a function: ", fn.Type())
	extendedEnv = extendFunctionEnv(function, args)
	evaluated = Eval(function.Body, extendedEnv)
	return unwrapReturnValue(evaluated)
	"""
	##########################################################
	
	# 組み込み関数len()が動く
	# let 関数定義が動かない
	# 2018/12/21 5:40修正 functionでなくfnを渡す
	
	print("applyFunction():1 ", fn, type(fn))
	function = type(fn)
	print("applyFunction():2 ", function, type(function))
	if function == object.Function:
		#extendedEnv = extendFunctionEnv(function, args)
		extendedEnv = extendFunctionEnv(fn, args)
		evaluated = Eval(fn.Body, extendedEnv)
		
		return unwrapReturnValue(evaluated)
	elif function == object.Builtin:
		print("applyFunction():3 ", fn, args, type(args))
		return fn.Fn(args) ########
	else:
		print("applyFunction():4 ", fn)
		return newError("not a function: ", fn.Type())
	

def extendFunctionEnv(fn, args):
	print("extendFunctionEnv()1: ", fn, type(fn))
	print("extendFunctionEnv()2: ", args, type(args))
	print("extendFunctionEnv()3: ", fn.Env, type(fn.Env)) ##ここで失敗fnはEnvを持たない
	
	env = environment.NewEnclosedEnvironment(fn.Env) ##
	#for paramIdx, param in fn.Parameters:
	paramIdx = 0
	while paramIdx < len(fn.Parameters):
		env.Set(fn.Parameters[paramIdx].Value, args[paramIdx])
		paramIdx += 1
	
	return env

def unwrapReturnValue(obj):
	print("unwrapReturnValue()1: ", obj)
	print("unwrapReturnValue()2: ", obj)
	print("unwrapReturnValue()3: ", type(obj))
	#returnValue = obj.ReturnValue #########
	"""
	if type(obj) == object.Function:
		#returnValue = obj.Value #########
		#return obj.Value
		return obj
	else:
		return obj.Value ####
	"""
	"""
	returnValue = obj.Value
	if returnValue != None:
		return returnValue
	"""
	return obj

def evalStringInfixExpression(operator, left, right):
	if operator != "+":
		return newError("unknown operator: ", left.Type(), str(operator), right.Type())
	
	print("evalStringInfixExpression(): ", left, right, type(left), type(right))
	
	leftVal = left.Value
	rightVal = right.Value
	
	print("evalStringInfixExpression(): ", leftVal, rightVal, type(leftVal), type(rightVal))
	
	ret = object.String()
	ret.Value = leftVal + rightVal
	
	return ret

def evalIndexExpression(left, index):
	if left.Type() == object.ARRAY_OBJ and index.Type() == object.INTEGER_OBJ:
		return evalArrayIndexExpression(left, index)
	elif left.Type() == object.HASH_OBJ:
		return evalHashIndexExpression(left, index)
	else:
		return newError("index operator not supported: ", left.Type())

def evalArrayIndexExpression(array, index):
	print("evalArrayIndexExpression()1: ", array, type(array))
	print("evalArrayIndexExpression()2: ", index, type(index))
	
	arrayObject = array ###
	idx = index.Value
	max = int(len(arrayObject.Elements) - 1)
	
	print("evalArrayIndexExpression()3: ", idx, type(idx))
	print("evalArrayIndexExpression()4: ", max, type(max))
	
	if idx < 0 or idx > max:
		return NULL
	
	return arrayObject.Elements[idx]

def evalHashLiteral(node, env):
	pairs = {}
	
	for keyNode in node.Pairs:
		key = Eval(keyNode, env)
		if isError(key):
			return key
		
		hashKey = key
		
		if hashKey == NULL:
			return newError("unusable as hash key: ", key.Type())
		
		value = Eval(node.Pairs[keyNode], env)
		if isError(value):
			return value
		
		hashed = hashKey.HashKey_method()
		ret = object.HashPair()
		ret.Key = key
		ret.Value = value
		#pairs[hashed] = ret
		pairs[hashed.Value] = ret
	
	retobj = object.Hash()
	retobj.Pairs = pairs
	return retobj
	
def evalHashIndexExpression(hash, index):
	print("evalHashIndexExpression()1: ", hash, type(hash))
	print("evalHashIndexExpression()2: ", index, type(index))
	
	hashObject = hash
	key = index
	if key == None or key == NULL:
		return newError("unusable as hash key: " + index.Type())
	
	print("evalHashIndexExpression()3: ", key.HashKey_method().Value, type(key.HashKey_method().Value))
	print("evalHashIndexExpression()4: ", key.HashKey_method(), type(key.HashKey_method()))
	if key.HashKey_method().Value in hashObject.Pairs:
		pair = hashObject.Pairs[key.HashKey_method().Value]
		#pair = hashObject.Pairs[key.HashKey_method()]
	else:
		print("evalHashIndexExpression()5: ")
		return NULL
	
	return pair.Value

if __name__ == "__main__":
	a = 1