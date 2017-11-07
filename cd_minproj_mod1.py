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
	'LSQRBRC',
	'RSQRBRC',
	'COMMA',
	'SEMICOLON'
)
t_LPAR = r'\('
t_RPAR = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='
t_LSQRBRC = r'\['
t_RSQRBRC = r'\]'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_STRING(t):
    r"'([^\\']+|\\'|\\\\)*'"  # I think this is right ...
    t.value=t.value.decode("string-escape") # .swapcase() # for fun
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
	# #yacc.parse(ply_input)
#except IOError:
#	print 'File not found...'
####################End of Tokenization...###############################
####################Implementing Parsing...##############################
#root  = tk.Tk()
#root.title('Algovizu_v1')
#root.geometry("900x500")

# dictionary of names
ids = { }
	
def p_statement(p) :
	'''
	statement : expression
	'''
	if p[1]:
		print p[1]
	
def p_expression(p):
	'''
	expression 	: expression TEXT LPAR text_param RPAR SEMICOLON
				| expression RECT LPAR rect_param RPAR SEMICOLON
				| expression LINE LPAR line_param RPAR SEMICOLON
				| expression BARCHART LPAR bacha_param RPAR SEMICOLON
				| expression id_assign
				| empty
	'''
	if len(p) > 4 :
		p[0] = p[4]

def p_num_or_id(p):
	'''
	id_or_num	:	NUMBER
				|	ID
	'''
	if type(p[1]) == int :
		p[0] = p[1]
	else :
		try:
			assert type(ids[p[1]]) == int
			p[0] = ids[p[1]]
		except LookupError:
			print("Undefined id '%s'" % p[1])
		except AssertionError:
			print 'Expected an integer but got something else...!!'
			
def p_string_or_id(p):
	'''
	id_or_string	:	STRING
					|	ID
	'''
	try : 
		p[0] = ids[p[1]]
	except LookupError:
		p[0] = p[1]

def p_list_or_id(p):
	'''
	id_or_list	:	listing
				|	ID
	'''
	if type(p[1]) == list :
		p[0] = p[1]
	else:
		try :
			p[0] = ids[p[1]]
		except :
			print "Error in (list_or_id) : id not found"

def p_listings(p):
	'''
	listing	:	LSQRBRC	list_parameters RSQRBRC
	'''
	p[0] = p[2]

def p_list_param(p):
	'''
	list_parameters	:	list_parameters COMMA id_or_num 
					|	id_or_num
					|	empty
	'''
	if len(p) == 2 :
		p[0] = [p[1]]
	else :
		p[0]=p[1]
		p[0].append(p[3])

def p_rect_statement(p) :
	'''
	rect_param : id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_string
	'''
	# p[1],p[3],p[5],p[7],p[9] --> x,y,width,height,color
	print 'Rectangle with : ',p[1],p[3],p[5],p[7],p[9]
	p[0] = 'true2'
	print 'RECT PRINTED...'
	
def p_text_param(p):
	'''
	text_param : id_or_num COMMA id_or_num COMMA id_or_string COMMA id_or_string COMMA id_or_num
	'''
	# p[1],p[3],p[5],p[7],p[9] --> x,y,text,colour,size
	print 'Text with : ', p[1],p[3],p[5],p[7],p[9]
	p[0] = 'true1'
	print 'TEXT PRINTED...'

def p_line_statement(p):
	'''
	line_param	:	id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_string COMMA id_or_num
	'''
	print 'Line with : ',p[1],p[3],p[5],p[7],p[9],p[11]
	p[0] = 'true3'
	print 'LINE PRINTED...'

def p_bacha_statement(p):
	'''
	bacha_param	:	id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_list COMMA id_or_num COMMA id_or_num COMMA id_or_string
	'''
	print 'Barchart with : ', p[1],p[3],p[5],p[7],p[9],p[11],p[13],p[15]
	p[0] = 'true4'
	print 'BARCHART PRINTED...'
	
def p_id_assign(p):
	'''
	id_assign	:	ID EQUAL NUMBER SEMICOLON
				|	ID EQUAL STRING SEMICOLON
				|	ID EQUAL listing SEMICOLON
				|	ID EQUAL ID SEMICOLON
	'''
	try :
		if p[3] in ids :
			ids[p[1]]=ids[p[3]]
		else :
			ids[p[1]] = p[3]
	except :
		ids[p[1]] = p[3]
	#print ids
	
def p_empty(p):
	'''
	empty : 
	'''
	pass

	
def p_error(p):
	print "Syntax error in input @ ",p.type

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
