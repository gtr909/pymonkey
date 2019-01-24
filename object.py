# -*- coding: utf-8 -*-

import hashlib

INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VALUE"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"
STRING_OBJ = "STRING"
BUILTIN_OBJ = "BUILTIN"
ARRAY_OBJ = "ARRAY"
HASH_OBJ = "HASH"

class Object:
	def Type(self):
		pass
	
	def Inspect(self):
		pass

	def HashKey_method(self):
		pass
"""
class Hashable:
	def HashKey_method(self):
		pass
"""
		
class Integer(Object):
	def __init__(self):
		self.Value = 0
	
	def Inspect(self):
		return str(self.Value)
	
	def Type(self):
		return INTEGER_OBJ
	
	def HashKey_method(self):
		ret = HashKey()
		ret.Type = self.Type()
		ret.Value = int(self.Value)
		
		return ret

class Boolean(Object):
	def __init__(self, v):
		self.Value = v
	
	def Type(self):
		return BOOLEAN_OBJ
	
	def Inspect(self):
		return str(self.Value)

	def HashKey_method(self):
		value = 0
		if self.Value:
			value = 1
		else:
			value = 0
		
		ret = HashKey()
		ret.Type = self.Type()
		ret.Value = value
		
		return ret

class Null(Object):
	def __init__(self):
		self.Value = None
	
	def Type(self):
		return NULL_OBJ
	
	def Inspect(self):
		return "null"

class ReturnValue(Object):
	def __init__(self):
		self.Value = None
	def Type(self):
		return RETURN_VALUE_OBJ
	def Inspect(self):
		return self.Value.Inspect()

class Error(object):
	def __init__(self):
		self.Message = ""
	
	def Type(self):
		return ERROR_OBJ
	
	def Inspect(self):
		return "ERROR: " + self.Message

class Function(object):
	def __init__(self):
		self.Parameters = []
		self.Body = None
		self.Env = None
	
	def Type(self):
		return FUNCTION_OBJ
	
	def Inspect(self):
		out = ""
		params = []
		
		for p in self.Parameters:
			params.append(p.String())
		
		out += "fn"
		out += "("
		out += ", ".join(params)
		out += ") {\n"
		out += self.Body.String()
		out += "\n}"
		
		return out

class String(object):
	def __init__(self):
		self.Value = ""
	
	def Type(self):
		return STRING_OBJ
	
	def Inspect(self):
		return self.Value

	def HashKey_method(self):
		msg = hashlib.md5((self.Value).encode('utf-8')).hexdigest() # ネットで検索し流用
		ret = HashKey()
		ret.Type = self.Type()
		ret.Value = msg
		return ret
		
class Builtin(object):
	def __init__(self):
		self.Fn = None
		
	def Type(self):
		return BUILTIN_OBJ
	
	def Inspect(self):
		return "builtin function"

class Array(object):
	def __init__(self):
		self.Elements = []
	
	def Type(self):
		return ARRAY_OBJ
	
	def Inspect(self):
		out = ""
		elements = []
		for e in self.Elements:
			elements.append(e.Inspect())
		out += "["
		out += ", ".join(elements)
		out += "]"
		
		return out

class HashKey:
	def __init__(self):
		self.Type = None
		self.Value = 0
	

class HashPair:
	def __init__(self):
		self.Key = None
		self.Value = None

class Hash(object):
	def __init__(self):
		self.Pairs = {}
	
	def Type(self):
		return HASH_OBJ
	
	def Inspect(self):
		out = ""
		pairs = []
		
		for key, pair in self.Pairs.items():
			print("object.Hash()::Inspect1", key, type(key))
			print("object.Hash()::Inspect2", self.Pairs, type(self.Pairs))
			print("object.Hash()::Inspect3", pair, type(pair))
			
			pairs.append(str(pair.Key.Inspect()) + ":" + str(pair.Value.Inspect()))
		
		out += "{"
		out += ", ".join(pairs)
		out += "}"
		
		return out



if __name__ == "__main__":
	a = Boolean(True)