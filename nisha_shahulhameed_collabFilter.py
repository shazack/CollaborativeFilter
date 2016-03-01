# -*- coding: utf-8 -*- 
import csv
import sys
#from collections import defaultdict
import itertools
import math

class Colab:
	def __init__(self):
		self.l=[]
		self.umat={}
		self.weights=[]


	def execute(self,inp,activeuser,item,k):
		#print inp
		#print activeuser
		#print item
		#print "k"
		#print k
		klist=[]
		pre=0.0
		def getdata(inp):
			with open("ratings-dataset.tsv") as tsvfile:
				umat={}
				elist=[]
				movies={}
				dict2={}
				tsvreader = csv.reader(tsvfile, delimiter="\t")
				for line in tsvreader:
					user=line[0].lower()
					movie=line[2].lower()
					#print user,movie
					rating=line[1]
					self.umat.setdefault(user,[])
					self.umat[user].append([movie,rating])
					#print self.umat
				
		def pearson_correlation(activeuser, user2):
			#calculate avg
			r1=0.0
			r2=0.0
			sum1=0.0
			sum2=0.0
			temp=0.0
			multiu=1
			multiv=1
			subu=0.0
			subv=0.0
			squ=0.0
			sqv=0.0
			multi=0
			pred=0.0
			for key,value in self.umat.iteritems():
				#calculate average for both users
				if key==activeuser:
					sum1= sum(float(i[1]) for i in value)
					r1=sum1/len(value)
					#print "avg for active user"
					#print r1
				elif key==user2:
					sum2= sum(float(i[1]) for i in value)
					r2=sum2/len(value)
					#print "avg for user2"
					#print r2
				#print "------"
				#print "------activeuser-------"
				#print activeuser
				#print self.umat[activeuser]
				#print "--------"
				#print "-------user2------"
				#print user2
				#print self.umat[user2]

			for i in self.umat[activeuser]:
				for j in self.umat[user2]:
					if i[0]==j[0]:
						subu=float(i[1])-r1
						subv=float(j[1])-r2
						squ+=pow(subu,2)
						sqv+=pow(subv, 2)
						multi+=subu*subv
			#print squ,sqv,multi
			#print r1,r2
			pred=multi/((math.sqrt(squ))*(math.sqrt(sqv)))
			self.weights.append([user2,pred])
			#print self.weights
		
		def K_nearest_neighbors(user1, k):
			#print "k nearest ----------"
			self.weights.sort(key=lambda row:row[0])
			self.weights.sort(key=lambda row:row[1],reverse=True)
			#print "k"
			#print k
			k=int(k)
			for i in xrange(k):
				klist.append(self.weights[i])
			for i,j in klist:
				print i,j 
			return klist

		def Predict(activeuser, item, k_nearest_neighbors):
			#print"predict========"
			nw=0.0
			nd=0.0
			pred=0.0
			for i in k_nearest_neighbors:
				for j in self.umat[i[0]]:
					if j[0]==item: 
						nw+=float(i[1])*float(j[1])
						nd+=float(i[1])
			if nd!=0:
				pred=float(nw/nd)
			elif nd==0:
				pred=0
			return pred
				#for i in value:
				#		useru.setdefault(i[0],[])
				#		useru[i[0]].append(float(i[1])-r1)
				#	for k,v in useru.iteritems():
				#		print k,v


					#subtract each value from average

		getdata(input)
		for key,value in self.umat.iteritems():
			if key!=activeuser:
				pearson_correlation(activeuser,key)
		#pearson_correlation(activeuser,"terveen")	
		klist=K_nearest_neighbors(activeuser, k)
		pre=Predict(activeuser, item, klist)
		print pre


				

if __name__ == '__main__':
	cl = Colab()
	cl.execute(sys.argv[1],sys.argv[2].lower(),sys.argv[3].lower(),sys.argv[4])
