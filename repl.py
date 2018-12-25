# -*- coding: utf-8 -*-
import sys
import parse
import lexer
import token
import evaluator
import object
import environment

PROMPT = ">> "

def Start():
	env = environment.NewEnvironment() ##???
	while True:
		print(PROMPT, end="")
		sys.stdout.flush()
		scanner = sys.stdin.readline()
		#env = environment.NewEnvironment()
		
		#print(scanner)
		
		if scanner == "":
			return
		lex = lexer.New(scanner)
		par = parse.New(lex)
		#par = parse.Parser("")
		#par.l = lex
		program = par.ParseProgram()
		
		if len(par.Errors()) != 0:
			printParseErrors(par.Errors())
			continue
		
		evaluated = evaluator.Eval(program, env)
		
		print("Start()1: ", evaluated, type(evaluated))
		
		if evaluated != None:
			if type(evaluated) == int:
				print("Start()2: type int")
				sys.stdout.write(str(evaluated))
				sys.stdout.write("\n")
			elif type(evaluated) == bool:
				sys.stdout.write(str(evaluated))
				sys.stdout.write("\n")
			elif type(evaluated) == float:
				sys.stdout.write(str(evaluated))
				sys.stdout.write("\n")
			else:
				print("Start()3: type intobj")
				sys.stdout.write(evaluated.Inspect())
				sys.stdout.write("\n")

def printParseErrors(e):
	sys.stdout.write("早川巌根\n")
	sys.stdout.write(" parser errors:\n")
	for msg in e:
		sys.stdout.write("\t" + msg + "\n")

if __name__ == "__main__":
	Start()
	