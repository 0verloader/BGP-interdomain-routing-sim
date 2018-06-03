import csv
import sys

class As(object):

	Ases = []

	def __init__(self, ASN):
		self.ASN = ASN
		self.prefixes = []
		self.peers = []
		self.flag = True
		self.Ases.append(self)
		return


	def add_prefix(self, prefix):
		self.prefixes.append({'prefix':prefix,'AS-PATH':[]})

	def add_peer(self, peer):
		if peer not in self.peers:
			self.peers.append(peer)

	def print_(self):
		print " _____________________________"
		print "/                  "
		print "|  ASN: "+str(self.ASN)
		print "|"
		print "|  Known prefixes:"
		count = 1
		if type(self.prefixes) is str:
			print "|   ",count,self.prefixes
		elif type(self.prefixes) is list:
			for prefix in self.prefixes:
				print '|   ',str(count)+".",prefix['prefix'],'\tAS-PATH:', 
				for i in prefix['AS-PATH']:
					print i.ASN,"   ",
				print '\n',
				count+=1
		print "|  Peers:"
		count = 1
		if type(self.peers) is str:
			print "|   ",count,self.peers
		elif type(self.peers) is list:
			for peer in self.peers:
				print "|   ",str(count)+".",peer.ASN
				count+=1
		print "|_____________________________"


	def install(self,prefix):
		k = 0
		for i in self.prefixes:
			num = prefixes_cmp(i, prefix)
			if num == 3:
				i = prefix
			elif num == 2:
				k +=1
		if k == 0:
			self.prefixes.append(prefix)
		pass	

	def announce_to_peer(self,peer,prefix):
		temp = []
		for i in prefix['AS-PATH']:
			temp.append(i)

		temp.append(self)
		temp_prefix = {'prefix':prefix['prefix'],'AS-PATH':temp}
		peer.install(temp_prefix)


	def announce(self):
		for i in self.prefixes:
			for y in self.peers:
				self.announce_to_peer(y,i)


def connect(as1, as2):
	as1.add_peer(as2)
	as2.add_peer(as1)


def prefixes_cmp(pr1 , pr2): #1 ok #2 not ok #3 remove pr2 and install pr1 # pr2 the one to install
	prefix = pr1['prefix'].split('/')[0]
	prefix = prefix.split('.')
	prefix_bits = ''
	for i in prefix:
		prefix_bits = prefix_bits + '{0:08b}'.format(int(i)) 

	prefix1 = pr2['prefix'].split('/')[0]
	prefix1 = prefix1.split('.')
	prefix_bits1 = ''
	for i in prefix1:
		prefix_bits1 = prefix_bits1 + '{0:08b}'.format(int(i)) 
	
	min_ = min([int(pr1['prefix'].split('/')[1]),int(pr2['prefix'].split('/')[1])])


	for i in range(0,min_):
		if(prefix_bits[i] is not prefix_bits1[i]):
			return 1

	if(int(pr1['prefix'].split('/')[1])==int(pr2['prefix'].split('/')[1])):
		pass
	elif(int(pr2['prefix'].split('/')[1])==min_):
		return 3
	else:
		return 2

	if(len(pr1['AS-PATH'])<=len(pr2['AS-PATH'])):
		return 2
	else:
		return 3



def prefannounce(as_):
	from random import randint
	import time
	while as_.flag:
		as_.announce()
		print '\n',as_.ASN,"announced"
		wait = randint(20,40)
		time.sleep(wait)



def announce_all(list):
	import threading
	threads = []
	for i in list:
		t = threading.Thread(target=prefannounce, args=[i])
		threads.append(t)
		t.start()


ases={}
f = open(sys.argv[1],'r')
r=csv.reader(f,delimiter=',')
for row in r:  
	as_ =As(ASN = int(row[0]))
	for k in row[1].split(','):
		as_.add_prefix(k)
	ases[int(row[0])]=as_
for row in r:  
	for k in row[2].split(','):
		connect(ases[int(row[0])],int(k))
f.close()



announce_all(As.Ases)