# -*- coding: utf-8 -*-

import evaluator

def NewEnvironment():
	s = {}
	
	ret = Environment()
	ret.store = s
	ret.outer = None #? or evaluator.NULL
	return ret

class Environment:
	def __init__(self):
		self.store = {}
		self.outer = None
	
	def Get(self, name):
		obj = None
		
		if name in self.store:
			obj = self.store[name]
			return obj
		elif self.outer != None:
			obj = self.outer.Get(name)
			return obj
		else:
			return evaluator.NULL

		########
		#elif obj == None and self.outer != None:
		#	obj = self.outer.Get(name)
		########
		#return obj

	def Set(self, name, val):
		#if not name in self.store:
		self.store[name] = val
		return val
		"""
		else:
			print("Environment::Get(): exist name key return None")
			return None
		"""
def NewEnclosedEnvironment(outer):
	env = NewEnvironment()
	env.outer = outer
	
	return env
	
if __name__ == "__main__":
	e = Environment()
	e.Get("aaa")
	print(e.Set("aaa", 1234))
	e.Get("aaa")
	
	