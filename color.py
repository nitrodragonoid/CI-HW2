from dsd import *
# from datetime import datetime
import math
from numpy.random import choice   
import random
import matplotlib.pyplot as plt
import numpy as np


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
        self.file = ""
        
        
    def getData(self,file):
        self.file = file
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
        minCol = upperbound
        for a in range(self.size):
            coloring, colors = self.greedyColorUpperbound(upperbound)
            self.ants[a] = coloring
            if colors > maxCol:
                maxCol = colors
            if colors < maxCol:
                minCol = colors
        self.Q = 1
        for i in range(1, maxCol+1):
            for v in self.graph.keys():
                self.trail[(v,i)] = 1
        
        for i in range(1,maxCol+1):
            self.colors.append(i)
            
    def randomColorUpperbound(self, upperbound):
        repeat = True
        count = 0
        while repeat == True and count <= 10:
            repeat = False
            vertices = list(self.graph.keys()).copy()
            random.shuffle(vertices)
            colorsUsed = set({})
            colors = []
            for i in range(upperbound):
                colors.append(i+1)
            assignment = ['N'] * len(vertices)
            for v in vertices:
                assign = False
                random.shuffle(colors)
                for c in colors:
                    conflict = False
                    for n in self.graph[v]:
                        if assignment[n] == c:
                            conflict = True
                    if conflict == False:
                        assignment[v] = c
                        assign = True
                        colorsUsed.add(c)
                if assign == False:
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
        return assignment, len(list(colorsUsed))
    
            
    def initialize_random(self):
        upperbound = math.floor(self.getMAD() + 1)
        
        maxCol = upperbound
        minCol = upperbound
        for a in range(self.size):
            coloring, colors = self.randomColorUpperbound(upperbound)
            self.ants[a] = coloring
            if colors > maxCol:
                maxCol = colors
            if colors < maxCol:
                minCol = colors

        self.Q = 1
        for i in range(1, maxCol+1):
            for v in self.graph.keys():
                self.trail[(v,i)] = 1
        
        for i in range(1,maxCol+1):
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
    
    def getAvg(self):
        total = 0
        for a in self.ants:
            total+= self.getColors(self.ants[a])
        return total/ len(list(self.ants.keys()))
        
    def optimize(self):
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]      
        print("Best number of colors use:", grundy)
        print("Average fitness:", self.getAvg())
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
            prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
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
            print("Average fitness:", self.getAvg())

        return grundy, Assignment
    
    def optimizeHeuristic(self):
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]      
        print("Best number of colors use:", grundy)
        print("Average fitness:", self.getAvg())
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
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
                        c = choice(self.colors, 1, p=probabilities)
                        og = self.ants[a]
                        self.ants[a][v] = c[0]
                        if self.getColors(og) < self.getColors(self.ants[a]):
                            for u in self.graph[v]:
                                sigmaT = 0
                                for j in self.colors:
                                    if j not in neighborColors and j in self.ants[a]:
                                        assignment = self.ants[a].copy()
                                        assignment[u] = j
                                        n = x/self.getColors(assignment)
                                        sigmaT += (self.trail[(u,j)])**self.alpha * n**self.beta
                                if sigmaT != 0: #if can change
                                    probabilities = []
                                    for i in self.colors:
                                        p = 0
                                        if i not in neighborColors and i in self.ants[a]:
                                            assignment = self.ants[a].copy()
                                            assignment[u] = i
                                            n = x/self.getColors(assignment)
                                            p = ((self.trail[(u,i)])**self.alpha * n**self.beta)/sigmaT
                                        probabilities.append(p)
                                    c = choice(self.colors, 1, p=probabilities)
                                    og = self.ants[a]
                                    self.ants[a][u] = c[0]
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
            print("Average fitness:", self.getAvg())
        
        return grundy, Assignment
            

    def test(self):
        
        #classic
        self.initialize()
        self.alpha = 1
        self.beta = 2
        self.gamma = 0.5
        
        avgs = []
        tours = []
        bests = []
        
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]     
        bests.append(grundy) 
        avgs.append(self.getAvg())
        tours.append(0)
        for k in range(self.tours):
            tours.append(k+1)
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
            prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
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
            bests.append(grundy) 
            avgs.append(self.getAvg())

        ypoints_1 = np.array(avgs)
        ypoints_2 = np.array(bests)
        xpoints = np.array(tours)
        

        plt.plot(xpoints, ypoints_1, color='r', label='Average colors used')
        plt.plot(xpoints, ypoints_2, color='b', label='Best colors used')
        plt.title(self.file, "Heuristic with greedy initialization, alpha = 1, beta = 2, gamma = 0.5")
        plt.show()
                
                
        self.initialize_random()
        self.alpha = 1.5
        self.beta = 3
        self.gamma = 0.8
        
        avgs = []
        tours = []
        bests = []
        
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]     
        bests.append(grundy) 
        avgs.append(self.getAvg())
        tours.append(0)
        for k in range(self.tours):
            tours.append(k+1)
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
            prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
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
            bests.append(grundy) 
            avgs.append(self.getAvg())

        # print(truncation_x)
        ypoints_1 = np.array(avgs)
        ypoints_2 = np.array(bests)
        xpoints = np.array(tours)
        

        plt.plot(xpoints, ypoints_1, color='r', label='Average colors used')
        plt.plot(xpoints, ypoints_2, color='b', label='Best colors used')
        plt.title(self.file, "Heuristic with random initialization, alpha = 1.5, beta = 3, gamma = 0.8")
        plt.show()
        
        
        
        
        # heurestic 
        
        self.initialize()
        self.alpha = 1
        self.beta = 2
        self.gamma = 0.5
        
        avgs = []
        tours = []
        bests = []
        
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]     
        bests.append(grundy) 
        avgs.append(self.getAvg())
        tours.append(0)
        for k in range(self.tours):
            tours.append(k+1)
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
            prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
                        c = choice(self.colors, 1, p=probabilities)
                        og = self.ants[a]
                        self.ants[a][v] = c[0]
                        if self.getColors(og) < self.getColors(self.ants[a]):
                            for u in self.graph[v]:
                                sigmaT = 0
                                for j in self.colors:
                                    if j not in neighborColors and j in self.ants[a]:
                                        assignment = self.ants[a].copy()
                                        assignment[u] = j
                                        n = x/self.getColors(assignment)
                                        sigmaT += (self.trail[(u,j)])**self.alpha * n**self.beta
                                if sigmaT != 0: #if can change
                                    probabilities = []
                                    for i in self.colors:
                                        p = 0
                                        if i not in neighborColors and i in self.ants[a]:
                                            assignment = self.ants[a].copy()
                                            assignment[u] = i
                                            n = x/self.getColors(assignment)
                                            p = ((self.trail[(u,i)])**self.alpha * n**self.beta)/sigmaT
                                        probabilities.append(p)
                                    c = choice(self.colors, 1, p=probabilities)
                                    og = self.ants[a]
                                    self.ants[a][u] = c[0]
                    else:
                        continue

            Assignment = []
            grundy = math.inf
            for a in self.ants:
                col = self.getColors(self.ants[a])  
                if col <= grundy:
                    grundy = col
                    Assignment = self.ants[a]      
            bests.append(grundy) 
            avgs.append(self.getAvg())

        ypoints_1 = np.array(avgs)
        ypoints_2 = np.array(bests)
        xpoints = np.array(tours)

        plt.plot(xpoints, ypoints_1, color='r', label='Average colors used')
        plt.plot(xpoints, ypoints_2, color='b', label='Best colors used')
        plt.title(self.file, "Classic with greedy initialization, alpha = 1, beta = 2, gamma = 0.5")
        plt.show()
                
                
        self.initialize_random()
        self.alpha = 1.5
        self.beta = 3
        self.gamma = 0.8
        
        avgs = []
        tours = []
        bests = []
        
        vertices = list(self.graph.keys())
        
        grundy = math.inf
        for a in self.ants:
            col = self.getColors(self.ants[a])  
            if col <= grundy:
                grundy = col
                Assignment = self.ants[a]     
        bests.append(grundy) 
        avgs.append(self.getAvg())
        tours.append(0)
        for k in range(self.tours):
            tours.append(k+1)
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
            prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                                assignment = self.ants[a].copy()
                                assignment[v] = i
                                n = x/self.getColors(assignment)
                                p = ((self.trail[(v,i)])**self.alpha * n**self.beta)/sigmaT
                            probabilities.append(p)
                        # transition
                        c = choice(self.colors, 1, p=probabilities)
                        og = self.ants[a]
                        self.ants[a][v] = c[0]
                        if self.getColors(og) < self.getColors(self.ants[a]):
                            for u in self.graph[v]:
                                sigmaT = 0
                                for j in self.colors:
                                    if j not in neighborColors and j in self.ants[a]:
                                        assignment = self.ants[a].copy()
                                        assignment[u] = j
                                        n = x/self.getColors(assignment)
                                        sigmaT += (self.trail[(u,j)])**self.alpha * n**self.beta
                                if sigmaT != 0: #if can change
                                    probabilities = []
                                    for i in self.colors:
                                        p = 0
                                        if i not in neighborColors and i in self.ants[a]:
                                            assignment = self.ants[a].copy()
                                            assignment[u] = i
                                            n = x/self.getColors(assignment)
                                            p = ((self.trail[(u,i)])**self.alpha * n**self.beta)/sigmaT
                                        probabilities.append(p)
                                    c = choice(self.colors, 1, p=probabilities)
                                    og = self.ants[a]
                                    self.ants[a][u] = c[0]
                    else:
                        continue

            Assignment = []
            grundy = math.inf
            for a in self.ants:
                col = self.getColors(self.ants[a])  
                if col <= grundy:
                    grundy = col
                    Assignment = self.ants[a]      
            bests.append(grundy) 
            avgs.append(self.getAvg())

        ypoints_1 = np.array(avgs)
        ypoints_2 = np.array(bests)
        xpoints = np.array(tours)

        plt.plot(xpoints, ypoints_1, color='r', label='Average colors used')
        plt.plot(xpoints, ypoints_2, color='b', label='Best colors used')
        plt.title(self.file, "Classic with random initialization, alpha = 1.5, beta = 3, gamma = 0.8")
        plt.show()
                


G = {0:[1,2,3,4],
     1:[0,2,3,4],
     2:[0,1,3,4],
     3:[0,1,2],
     4:[0,1,2],
     5:[6],
     6:[5,7],
     7:[6]  
} 
aco = ACO(graph= G, gamma = 0.5 ,alpha = 1, beta = 2, size = 100, tours=500)
aco.getData("queen11_11_formated.col")
aco.test()

aco = ACO(graph= G, gamma = 0.5 ,alpha = 1, beta = 2, size = 100, tours=500)
aco.getData("le450-15b_formated.col")
aco.test()


# aco = ACO(graph= G, gamma = 0.8 ,alpha = 1, beta = 2, size = 100, tours=1000)
# aco = ACO(graph= G, gamma = 0.8 ,alpha = 1.5, beta = 3, size = 100,tours=1000)
# aco = ACO()

# aco.getData("le450-15b_formated.col")
# aco.getData("queen11_11_formated.col")
# aco.initialize()
# aco.initialize_random()
# aco.optimize()
# aco.optimizeHeuristic()

    
#88