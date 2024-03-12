from dsd import *
# from datetime import datetime
import math
from numpy.random import choice   
import random


class ACO:
    
    def __init__(self, graph = {0:[1],1:[0]}, size  = 20, alpha = 0.8, beta = 0.8, gamma = 0.8, tours = 10, Q = 1):
        self.graph = dict(graph)
        self.trail = {}
        self.ants = {}
        self.size  = 20
        self.alpha = 0.8
        self.beta = 0.8
        self.gamma = 0.8
        self.tours = tours
        self.Q = Q
        self.colors = []
        
    def getData(self,file):
        self.graph = dict({})
        f = open(file, "r")
        l = 0
        for x in f:
            l+=1
            if x == "EOF":
                break
            info = x.split(" ")
            if l == 1:
                vertices = int(info[1])
                for v in range(vertices):
                    self.graph[v] = []
            if l == 2:
                continue
            # print(l)
            if l > 2:
                # print("here")
                v = int(info[1]) - 1
                u = int(info[2]) - 1
                self.graph[v].append(u)
                self.graph[u].append(v)
        return self.graph

    def greedyColorUpperbound(self, upperbound):
        repeat = True
        count = 0
        while repeat == True and count <= 10:
            repeat = False
            vertices = list(self.graph.keys()).copy()
            random.shuffle(vertices)
            colors = [1]
            assignment = ['N'] * len(vertices)
            for v in vertices:
                assign = False
                for c in colors:
                    conflict = False
                    for n in self.graph[v]:
                        if assignment[n] == c:
                            conflict = True
                    if conflict == False:
                        assignment[v] = c
                        assign = True
                if assign == False:
                    if colors[-1] < upperbound:
                        assignment[v] = colors[-1]+1
                        colors.append(colors[-1]+1)
                    else:
                        repeat = True
                        count += 1
                        break
                    
        if count > 10:
            vertices = self.permutation(list(self.graph.keys()))
            colors = [1]
            assignment = ['N'] * len(vertices)
            for v in vertices:
                assign = False
                for c in colors:
                    conflict = False
                    for n in self.graph[v]:
                        if assignment[n] == c:
                            conflict = True
                    if conflict == False:
                        assignment[v] = c
                        assign = True
                if assign == False:
                    assignment[v] = colors[-1]+1
                    colors.append(colors[-1]+1)
        return assignment, colors[-1]

                
    def initialize(self):
        upperbound = math.floor(self.getMAD() + 1)
        
        maxCol = upperbound
        for a in range(self.size):
            coloring, colors = self.greedyColorUpperbound(upperbound)
            self.ants[a] = coloring
            if colors > maxCol:
                maxCol = colors
        self.Q = 1
        for i in range(1, maxCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
            for v in self.graph.keys():
                self.trail[(v,i)] = 1
                # self.trail[(v,i)] = 1
                deltat = 0
                for a in self.ants:
                    if self.ants[a][v] == i:
                        deltat += self.Q/self.getColors(self.ants[a])

                # self.trail[(v,i)] = self.gamma * self.trail[(v,i)] + deltat
                # if deltat != 0:
                #     print(deltat)
                self.trail[(v,i)] = 0.000002 * self.trail[(v,i)] + deltat
        
        for i in range(1,maxCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
            self.colors.append(i)
            
    def getNeighborColors(self,assignment, v):
        colors = set({})
        for u in self.graph[v]:
            colors.add(assignment[u])
        return list(colors)
         
    def getColors(self,assignment):
        colors = []
        for i in assignment:
            if i not in colors:
                colors.append(i)
        return len(colors)
        

    def getEdges(self, G):
        E = []
        for v in G.keys():
            for u in G[v]:
                if (u,v) not in E:
                    E.append([v,u])
        return E
    
    def getMAD(self):
        exact_R = exact_densest(self.getEdges(self.graph))  
        MAD = exact_R[1]
        H = exact_R[0]
        return MAD
        
    def optimize(self):
        
        for k in range(self.tours):
            print("tour:", k)
            # update trail intensities
            for t in self.trail:
                deltat = 0
                for a in self.ants:
                    if self.ants[a][t[0]] == t[1]:
                        deltat += self.Q/self.getColors(self.ants[a])
                
                self.trail[t] = self.gamma * self.trail[t] + deltat
            
            
            # compute probabilities and transition
            x = 1
            for a in self.ants:
                for v in self.graph.keys():
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
                        # print(probabilities)
                        c = choice(self.colors, 1, p=probabilities)
                        self.ants[a][v] = c[0]
                    else:
                        continue
            Assignment = []
            grundy = math.inf
            for a in self.ants:
                col = self.getColors(self.ants[a])  
                if col <= grundy:
                    grundy = col
                    Assignment = self.ants[a]      
            print("Best number of colors use:", grundy)
            # if k == 10:
            #     for t in self.trail:
            #         print(t,":",self.trail[t])
            # print("Assignment:",Assignment)
        
        return grundy, Assignment
            


G = {0:[1,2,3,4],
     1:[0,2,3,4],
     2:[0,1,3,4],
     3:[0,1,2],
     4:[0,1,2],
     5:[6],
     6:[5,7],
     7:[6]  
} 
test = ACO(graph= G, gamma = 0.5 ,alpha = 0.8, beta = 2, size = 20,tours=500)
# test = ACO()
test.getData("queen11_11_formated.col")
# test.getData("le450-15b_formated.col")
# print(test.graph)
# print(test.getMAD())

test.initialize()
test.optimize()

    
