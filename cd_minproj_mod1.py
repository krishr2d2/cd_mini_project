# A grammar for chemical equations like "H2O", "CH3COOH" and "H2SO4"
# Uses David Beazley's PLY parser.
# Implements two functions: count the total number of atoms in the equation and
#   count the number of times each element occurs in the equation.
import sys
import ply.lex as lex
import ply.yacc as yacc
import Tkinter as tk

tokens = (
	'NUMBER',
	'STRING',
	'ID',
	'EQUAL',
	'LPAR',
	'RPAR',
	'COMMA',
	'SEMICOLON'
)
t_LPAR = r'\('
t_RPAR = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_STRING(t):
    r"'([^\\']+|\\'|\\\\)*'"  # I think this is right ...
    t.value=t.value[1:-1].decode("string-escape") # .swapcase() # for fun
    return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	
t_ignore = ' \t'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

RESERVED = {
	'text' : 'TEXT',
	'rect' : 'RECT',
	'line' : 'LINE',
	'bacha' : 'BARCHART',
	'if' : 'IF',
	'else' : 'ELSE',
	'then' : 'THEN',
	'while' : 'WHILE'
}

tokens = tokens + tuple(RESERVED.values())

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = RESERVED.get(t.value, "ID")
	return t
	
t_ignore_COMMENT = r'(/\#(.|\n)*?\#/)|(//.*)'
	
lex.lex()

############## testing the lex tokenizing ############ 
#try : 
#	ply_input = open(str(sys.argv[1]),'r').read()
#	lex.input(ply_input)
#	for tok in iter(lex.token, None):
#		print repr(tok)
	#yacc.parse(ply_input)
#except IOError:
#	print 'File not found...'
####################End of Tokenization...###############################
####################Implementing Parsing...##############################
#root  = tk.Tk()
#root.title('Algovizu_v1')
#root.geometry("900x500")

def p_statement(p) :
	'''
	statement : expression
	'''
	if p[1]:
		print p[1]
	
def p_expression(p):
	'''
	expression : TEXT LPAR text_param RPAR SEMICOLON expression
				| RECT LPAR rect_param RPAR SEMICOLON expression
				| empty
	'''
	if len(p) > 4 :
		p[0] = p[3]
	
def p_rect_statement(p) :
	'''
	rect_param : NUMBER COMMA NUMBER COMMA NUMBER COMMA NUMBER COMMA STRING
	'''
	print 'Rectangle with : ',p[1],p[3],p[5],p[7],p[9]
	p[0] = 'rectangle printed'
	print 'RECT PRINTED...'
	
def p_text_param(p):
	'''
	text_param : NUMBER COMMA NUMBER COMMA STRING COMMA STRING
	'''
	print 'Text with : ', p[1],p[3],p[5],p[7]
	p[0] = 'text printed'
	print 'TEXT PRINTED...'
	
def p_empty(p):
	'''
	empty : 
	'''
	pass
	
def p_error(p):
	print "Syntax error in input!"

#root.mainloop()
#######################testing of the parser##########
yacc.yacc()
try : 
	ply_input = open(str(sys.argv[1]),'r').read()
	#ply_input = ply_input.split(';')
	#for line in ply_input :
	#	yacc.parse(line)
#	print '\n',ply_input,'\n'
	yacc.parse(ply_input)
except IOError:
	print 'File not found...'
########################################################