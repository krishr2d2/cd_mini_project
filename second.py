from cd_miniproj_v2 import Mylexerparser

m = Mylexerparser()
m.build_parser()
ply_input=open('ply_input.txt','r').read()

def bubbleSort(L):
    swaps = 0
    for i in range(len(L) - 1, 0, -1): 
        for j in xrange(i):
            if L[j] > L[j+1]:
				L[j],L[j+1] = L[j+1],L[j]
				swaps +=1
				
				k={'data':data,'i':i,'j':j}
				m.driver(k,ply_input)# to display the updated list...
 
from random import sample
data = sample(range(10), 10)
print data
bubbleSort(data)
print data
#m.test_parser(ply_input)


