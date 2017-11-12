import ply.lex as lex
import ply.yacc as yacc

class Mylexerparser(object):
	tokens = (
	'NUMBER',
	'STRING',
	'ID',
	'LPAR',
	'RPAR',
	'LSQRBRC',
	'RSQRBRC',
	'LCURL',
	'RCURL',
	'COMMA',
	'SEMICOLON',
	'PLUS',
	'MINUS',
	'MULT',
	'DIV',
	'EQUAL',
	'GRT',
	'LST',
	'GRE',
	'LSE',
	'DOUBEQ',
	'NOTEQ',
	'AND',
	'OR'
	)
	#OPERATORS
	t_PLUS = r'\+'
	t_MINUS = r'-'
	t_MULT = r'\*'	
	t_DIV = r'/'
	t_EQUAL = r'='
	t_GRT = r'>'
	t_LST = r'<'
	t_GRE = r'>='
	t_LSE = r'<='
	t_DOUBEQ = r'=='
	t_NOTEQ = r'!='
	t_AND = r'&'
	t_OR = r'\|' 
	t_LPAR = r'\('
	t_RPAR = r'\)'
	t_COMMA = r','
	t_SEMICOLON = r';'
	t_LSQRBRC = r'\['
	t_RSQRBRC = r'\]'
	t_LCURL = r'\{'
	t_RCURL = r'\}'
	
	def t_NUMBER(self,t):
		r'\d+'
		t.value = int(t.value)
		return t

	def t_STRING(self,t):
		r"'([^\\']+|\\'|\\\\)*'"  # I think this is right ...
		t.value=t.value.decode("string-escape") # .swapcase() # for fun
		return t

	def t_newline(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)
	
	t_ignore = ' \t'

	def t_error(self,t):
		raise TypeError("Unknown text '%s'" % (t.value,))

	RESERVED = {
		'text' : 'TEXT',
		'rect' : 'RECT',
		'line' : 'LINE',
		'bacha' : 'BARCHART',
		'if' : 'IF',
		'else' : 'ELSE',
		'while' : 'WHILE'
	}

	tokens = tokens + tuple(RESERVED.values())

	def t_ID(self,t):
		r'[a-zA-Z_][a-zA-Z0-9_]*'
		t.type = self.RESERVED.get(t.value, "ID")
		return t
	
	t_ignore_COMMENT = r'(/\#(.|\n)*?\#/)|(//.*)'
	
	def build_lexer(self,**kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
	
	def test_lexer(self,data):
		
		self.lexer.input(data)
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)
	
	ids = { }
	
	precedence = (
    ('nonassoc','IF'),
    ('nonassoc','ELSE'),
    ('nonassoc','EQUAL'),
    ('nonassoc','AND','OR'),
    ('nonassoc','DOUBEQ','NOTEQ','LSE','LST','GRT','GRE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIV','MULT')
	)
	
	def send_params(self,k={}):
		self.ids = dict(k)
	
	def p_statement(self,p) :
		'''
		statement	:	expression
		'''
		if p[1]:
			print p[1]
	
	def p_expression(self,p):
		'''
		expression	:	expression TEXT LPAR text_param RPAR SEMICOLON
					|	expression RECT LPAR rect_param RPAR SEMICOLON
					|	expression LINE LPAR line_param RPAR SEMICOLON
					|	expression BARCHART LPAR bacha_param RPAR SEMICOLON
					|	expression id_assign
					|	expression IF LPAR boolean_exp RPAR LCURL expression RCURL else_term
					|	empty
		'''
		if len(p) > 4 :
			if p[2] == 'if' and p[4] == True :
				if p[1] :
					p[0] = p[1]
				else :
					p[0] = []
				p[0] = p[0] + p[7]
			
			elif p[2] == 'if' and p[4] == False :
				if p[1] : 
					p[0] = p[1]
				else :
					p[0] = []
				p[0] = p[0] + p[9]
				
			else :
				if p[1] :
					p[1].append(p[4])
					p[0] = list(p[1])
				else :
					p[0] = [p[4]]
			#p[0] = p[4]

	def p_num_or_id(self,p):
		'''
		id_or_num	:	exp_eval
		'''
		#if p[1] :
		p[0] = p[1]

	# def p_num_exp_eval(p):
		# '''
		# exp_eval	:	expression2
		# '''
		# if (p[1]):
			# p[0]=p[1]

	def p_fun_for_exp2(self,p):
		'''
		exp_eval	:	exp_eval PLUS term
					|	exp_eval MINUS term
					|	term
		'''
		if len(p) > 2 :
			if p[2] == '+' : p[0] = p[1] + p[3]
			elif p[2] == '-' : p[0] = p[1] - p[3]
		else :
			p[0] = p[1]
		
	def p_expression2_term(self,p):
		'''
		term	:	term MULT func
				|	term DIV func
				|	func
		'''
		if len(p) > 2 :
			if p[2] == '*' : p[0] = p[1] * p[3]
			elif p[2] == '/' : p[0] = p[1] / p[3]
		else : 
			p[0] = p[1]

	def p_term_func(self,p):
		'''
		func	:	LPAR exp_eval RPAR
				|	NUMBER
				|	ID
		'''
		if len(p)==4 :
			p[0] = p[2]
		else :
			if type(p[1]) == int :
				p[0] = p[1]
			else :
				try:
					assert type(self.ids[p[1]]) == int
					p[0] = self.ids[p[1]]
				except LookupError:
					print("Undefined id '%s'" % p[1])
				except AssertionError:
					print 'Expected an integer but got something else...!!'
	
	def p_string_or_id(self,p):
		'''
		id_or_string	:	STRING
						|	ID
		'''
		try : 
			assert p[1][0] == "'"
			p[0] = p[1]
		except AssertionError:
			try :
				if type(self.ids[p[1]]) == str :
					p[0] = self.ids[p[1]]
				else :
					print 'Expected a string but got %s' % type(self.ids[p[1]])
			except LookupError :
				print 'Undefined element %s' % p[1]

	def p_list_or_id(self,p):
		'''
		id_or_list	:	listing
					|	ID
		'''
		if type(p[1]) == list :
			p[0] = p[1]
		else:
			try :
				p[0] = self.ids[p[1]]
			except :
				print "Error in (list_or_id) : id not found"

	def p_listings(self,p):
		'''
		listing	:	LSQRBRC	list_parameters RSQRBRC
		'''
		p[0] = p[2]

	def p_list_param(self,p):
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

	def p_rect_statement(self,p) :
		'''
		rect_param : id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_string
		'''
		# p[1],p[3],p[5],p[7],p[9] --> x,y,width,height,color
		#print 'Rectangle with : ',p[1],p[3],p[5],p[7],p[9]
		p[0] = ['rect',p[1],p[3],p[5],p[7],p[9]]
		#print 'RECT PRINTED...'
	
	def p_text_param(self,p):
		'''
		text_param : id_or_num COMMA id_or_num COMMA id_or_string COMMA id_or_string COMMA id_or_num
		'''
		# p[1],p[3],p[5],p[7],p[9] --> x,y,text,colour,size
		#print 'Text with : ', p[1],p[3],p[5],p[7],p[9]
		p[0] = ['text',p[1],p[3],p[5],p[7],p[9]]
		#print 'TEXT PRINTED...'

	def p_line_statement(self,p):
		'''
		line_param	:	id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_string COMMA id_or_num
		'''
		#print 'Line with : ',p[1],p[3],p[5],p[7],p[9],p[11]
		p[0] = ['line',p[1],p[3],p[5],p[7],p[9],p[11]]
		#print 'LINE PRINTED...'

	def p_bacha_statement(self,p):
		'''
		bacha_param	:	id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_num COMMA id_or_list COMMA id_or_list COMMA id_or_num COMMA id_or_string
		'''
		#print 'Barchart with : ', p[1],p[3],p[5],p[7],p[9],p[11],p[13],p[15]
		p[0] = ['Barchart',p[1],p[3],p[5],p[7],p[9],p[11],p[13],p[15]]
		#print 'BARCHART PRINTED...'
	
	def p_id_assign(self,p):
		'''
		id_assign	:	ID EQUAL id_or_num SEMICOLON
					|	ID EQUAL STRING SEMICOLON
					|	ID EQUAL listing SEMICOLON
					|	ID EQUAL ID SEMICOLON
		'''
		try :
			if p[3] in self.ids :
				self.ids[p[1]]=self.ids[p[3]]
			else :
				self.ids[p[1]] = p[3]
		except :
			self.ids[p[1]] = p[3]
		#print ids
	
	def p_boolean_func(self,p):
		'''
		boolean_exp	:	bool_term AND boolean_exp
					|	bool_term OR boolean_exp
					|	boolean_exp AND boolean_exp
					|	boolean_exp OR boolean_exp
					|	id_or_num GRT id_or_num
					|	id_or_num GRE id_or_num
					|	id_or_num LST id_or_num
					|	id_or_num LSE id_or_num
					|	id_or_num DOUBEQ id_or_num
					|	id_or_num NOTEQ id_or_num
		'''
		if p[2] == '&' : p[0] = p[1] and p[3]
		elif p[2] == '|': p[0] = p[1] or p[3]
		elif p[2] == '>': p[0] = p[1] > p[3]
		elif p[2] == '<': p[0] = p[1] < p[3]
		elif p[2] == '>=': p[0] = p[1] >= p[3]
		elif p[2] == '<=': p[0] = p[1] <= p[3]
		elif p[2] == '==': p[0] = p[1] == p[3]
		elif p[2] == '!=': p[0] = p[1] != p[3]
		elif p[1] == '\(' : p[0] = p[2]
		else :	print 'Unknown Production encountered...'
	
	def p_boolean_term(self, p):
		'''
		bool_term	:	LPAR boolean_exp RPAR
					|	empty
		'''
		if len(p) > 2 :
			p[0] = p[2]
		else :
			p[0] = True
	
	def p_else_statement(self,p):
		'''
		else_term	:	ELSE LCURL expression RCURL
					|	empty
		'''
		#pass
		if len(p) > 2 :
			p[0] = p[3]
		else :
			p[0] = []
	
	def p_empty(self, p):
		'''
		empty : 
		'''
		pass

	def p_error(self,p):
		print "Syntax error in input @ %s = %s" % (p.type,p.value)
	
	def build_parser(self,**kwargs):
		self.build_lexer()
		self.parser = yacc.yacc(module=self, **kwargs)
		
	def test_parser(self,data):
		yacc.parse(data)
	
	def driver(self,k={},ply_input=''):
		self.send_params(k)
		self.test_parser(ply_input)
	
# Build the lexer and try it out
#m = Mylexerparser()
#m.build_lexer()    	# Build the lexer
#m.test_lexer("text(10,10,'Hello master', b,13);")  # Test it
#m.build_parser()
#m.test_parser("text(10,10,'Hello master', b,13);")