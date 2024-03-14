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
        minCol = upperbound
        for a in range(self.size):
            coloring, colors = self.greedyColorUpperbound(upperbound)
            self.ants[a] = coloring
            if colors > maxCol:
                maxCol = colors
            if colors < maxCol:
                minCol = colors
            # print(colors, coloring)
        self.Q = 1
        for i in range(1, maxCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
            for v in self.graph.keys():
                self.trail[(v,i)] = 1
                # self.trail[(v,i)] = 1
                
                # deltat = 0
                # for a in self.ants:
                #     if self.ants[a][v] == i:
                #         deltat += self.Q/self.getColors(self.ants[a])

                # self.trail[(v,i)] = self.gamma * self.trail[(v,i)] + deltat
                
                # if deltat != 0:
                #     print(deltat)
                # self.trail[(v,i)] = 0.000002 * self.trail[(v,i)] + deltat
        
        for i in range(1,maxCol+1):
        # for i in range(1,minCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
        # for i in range(1,minCol+2):
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
            # print(colors, coloring)
        self.Q = 1
        for i in range(1, maxCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
            for v in self.graph.keys():
                self.trail[(v,i)] = 1
                # self.trail[(v,i)] = 1
                
                # deltat = 0
                # for a in self.ants:
                #     if self.ants[a][v] == i:
                #         deltat += self.Q/self.getColors(self.ants[a])

                # self.trail[(v,i)] = self.gamma * self.trail[(v,i)] + deltat
                
                # if deltat != 0:
                #     print(deltat)
                # self.trail[(v,i)] = 0.000002 * self.trail[(v,i)] + deltat
        
        for i in range(1,maxCol+1):
        # for i in range(1,minCol+1):
        # for i in range(1,len(list(self.graph.keys()))+1):
        # for i in range(1,minCol+2):
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
                        # if j not in neighborColors:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                            # if i not in neighborColors:
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
                    # if a == 1 and v == 0:
                    #     prob = probabilities
            Assignment = []
            grundy = math.inf
            for a in self.ants:
                col = self.getColors(self.ants[a])  
                if col <= grundy:
                    grundy = col
                    Assignment = self.ants[a]      
            print("Best number of colors use:", grundy)
            print("Average fitness:", self.getAvg())
            # print(prob)
            # if k == 10:
            #     for t in self.trail:
            #         print(t,":",self.trail[t])
            # print("Assignment:",Assignment)
        
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
            # prob = []
            for a in self.ants:
                random.shuffle(vertices)
                
                for v in vertices:
                    neighborColors = self.getNeighborColors(self.ants[a],v)
                    
                    #compute probabilities
                    sigmaT = 0
                    for j in self.colors:
                        if j not in neighborColors and j in self.ants[a]:
                        # if j not in neighborColors:
                            assignment = self.ants[a].copy()
                            assignment[v] = j
                            n = x/self.getColors(assignment)
                            sigmaT += (self.trail[(v,j)])**self.alpha * n**self.beta
                    if sigmaT != 0: #if can change
                        probabilities = []
                        for i in self.colors:
                            p = 0
                            if i not in neighborColors and i in self.ants[a]:
                            # if i not in neighborColors:
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
                            # if self.getColors(og) == 17:
                            #     print("min")
                            #     for y in self.graph:
                            #         for h in self.colors:
                            #             a = og.copy()
                            #             if h not in self.getNeighborColors(a,y):
                            #                 a[y] = h
                            #                 if  self.getColors(a) < 17:
                            #                     print(a)
                            #                     print("omg")
                            for u in self.graph[v]:
                                sigmaT = 0
                                for j in self.colors:
                                    if j not in neighborColors and j in self.ants[a]:
                                    # if j not in neighborColors:
                                        assignment = self.ants[a].copy()
                                        assignment[u] = j
                                        n = x/self.getColors(assignment)
                                        sigmaT += (self.trail[(u,j)])**self.alpha * n**self.beta
                                if sigmaT != 0: #if can change
                                    probabilities = []
                                    for i in self.colors:
                                        p = 0
                                        if i not in neighborColors and i in self.ants[a]:
                                        # if i not in neighborColors:
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
                    # if a == 1 and v == 0:
                    #     prob = probabilities
            Assignment = []
            grundy = math.inf
            for a in self.ants:
                col = self.getColors(self.ants[a])  
                if col <= grundy:
                    grundy = col
                    Assignment = self.ants[a]      
            print("Best number of colors use:", grundy)
            print("Average fitness:", self.getAvg())
            # print(prob)
            # if k == 10:
            #     for t in self.trail:
            #         print(t,":",self.trail[t])
            # print("Assignment:",Assignment)
        
        return grundy, Assignment
            

    def test(self,k):
        l = k+1
        fitprop = []
        fitprop_average = []
        for i in range(self.generation):
            r = []
            r1 = []
            for j in range(k+1):
                r.append(0)
                r1.append(0)
            fitprop.append(r)
            fitprop_average.append(r1)
        
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_fitness_proportional()

                self.survivers_fitness_proportional()
                
                b = self.best()[1]
                fitprop[g][i] = b
                fitprop[g][k] += b
                
                a = self.average_fitness()
                fitprop_average[g][i] = a
                fitprop_average[g][k] += a
        for g in range(self.generation):
            fitprop[g][k] = fitprop[g][k]/k
            fitprop_average[g][k] = fitprop_average[g][k]/k
        
        fitprop_x = []
        y = []
        for i in range(self.generation):
            y.append(i+1)
            fitprop_x.append(fitprop[i][k])
            
            
        ranked = []
        ranked_average = []
        for i in range(self.generation):
            r = []
            r1 = []
            for j in range(k+1):
                r.append(0)
                r1.append(0)
            ranked.append(r)
            ranked_average.append(r1)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_ranked()

                self.survivers_ranked()
                
                b = self.best()[1]
                ranked[g][i] = b
                ranked[g][k] += b
                a = self.average_fitness()
                ranked_average[g][i] = a
                ranked_average[g][k] += a
        for g in range(self.generation):
            ranked[g][k] = ranked[g][k]/k
            ranked_average[g][k] = ranked_average[g][k]/k
        
        ranked_x = []
        for i in range(self.generation):
            ranked_x.append(ranked[i][k])
            
        tournament = []
        tournament_average = []
        for i in range(self.generation):
            r = []
            r1 = []
            for j in range(k+1):
                r.append(0)
                r1.append(0)
            tournament.append(r)
            tournament_average.append(r1)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_tournament(self.tournament_size)

                self.survivers_tournament(self.tournament_size)
                
                b = self.best()[1]
                tournament[g][i] = b
                tournament[g][k] += b
                
                a = self.average_fitness()
                tournament_average[g][i] = a
                tournament_average[g][k] += a
        for g in range(self.generation):
            tournament[g][k] = tournament[g][k]/k
            tournament_average[g][k] = tournament_average[g][k]/k
        
        tournament_x = []
        for i in range(self.generation):
            tournament_x.append(tournament[i][k])
            
            
            
        truncation = []
        truncation_average = []
        for i in range(self.generation):
            r = []
            r1 = []
            for j in range(k+1):
                r.append(0)
                r1.append(0)
            truncation.append(r)
            truncation_average.append(r1)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_truncation()

                self.survivers_truncation()
                
                b = self.best()[1]
                truncation[g][i] = b
                truncation[g][k] += b
                
                a = self.average_fitness()
                truncation_average[g][i] = a
                truncation_average[g][k] += a
        for g in range(self.generation):
            truncation[g][k] = truncation[g][k]/k
            truncation_average[g][k] = truncation_average[g][k]/k
        
        truncation_x = []
        for i in range(self.generation):
            truncation_x.append(truncation[i][k])
            
            
            
        random = []
        random_average = []
        for i in range(self.generation):
            r = []
            r1 = []
            for j in range(k+1):
                r.append(0)
                r1.append(0)
            random.append(r)
            random_average.append(r1)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_random_selection()

                self.survivers_random_selection()
                
                b = self.best()[1]
                random[g][i] = b
                random[g][k] += b
                
                a = self.average_fitness()
                random_average[g][i] = a
                random_average[g][k] += a
        for g in range(self.generation):
            random[g][k] = random[g][k]/k
            random_average[g][k] = random_average[g][k]/k
        
        random_x = []
        for i in range(self.generation):
            random_x.append(random[i][k])
        
        print("Fitness propotional best fitness table")
        for i in range(len(random)):
            print(fitprop[i])
            
        print("Fitness propotional average fitness table")
        for i in range(len(random)):
            print(fitprop_average[i])
            
            
        print("Ranked best fitness table")
        for i in range(len(random)):
            print(ranked[i])
            
        print("Ranked average fitness table")
        for i in range(len(random)):
            print(ranked_average[i])
            
            
        print("Tournament best fitness table")
        for i in range(len(random)):
            print(tournament[i])
            
        print("Tournament average fitness table")
        for i in range(len(random)):
            print(tournament_average[i])
            
            
        print("Truncation best fitness table")
        for i in range(len(random)):
            print(truncation[i])
            
        print("Truncation average fitness table")
        for i in range(len(random)):
            print(truncation_average[i])
            
            
        print("Random best fitness table")
        for i in range(len(random)):
            print(random[i])   
            
        print("Random average fitness table")
        for i in range(len(random)):
            print(random_average[i])    
        
        # print(truncation_x)
        ypoints_1 = np.array(fitprop_x)
        ypoints_2 = np.array(ranked_x)
        ypoints_3 = np.array(tournament_x)
        ypoints_4 = np.array(truncation_x)
        ypoints_5 = np.array(random_x)
        xpoints = np.array(y)
        
        # plt.plot(X, y, color='r', label='sin') 
        # plt.plot(X, z, color='g', label='cos')

        plt.plot(xpoints, ypoints_1, color='r', label='fitness proportional')
        plt.plot(xpoints, ypoints_2, color='b', label='ranked')
        plt.plot(xpoints, ypoints_3, color='g', label='tournament')
        plt.plot(xpoints, ypoints_4, color='y', label='truncation')
        plt.plot(xpoints, ypoints_5, color='k', label='random')
        plt.show()
                


# G = {0:[1,2,3,4],
#      1:[0,2,3,4],
#      2:[0,1,3,4],
#      3:[0,1,2],
#      4:[0,1,2],
#      5:[6],
#      6:[5,7],
#      7:[6]  
# } 
# test = ACO(graph= G, gamma = 0.8 ,alpha = 2, beta = 1, size = 100,tours=500)
# test = ACO(graph= G, gamma = 0.5 ,alpha = 1, beta = 2, size = 100, tours=1000)
test = ACO(graph= G, gamma = 0.8 ,alpha = 1.5, beta = 3, size = 100, tours=1000)
# test = ACO(graph= G, gamma = 0.8 ,alpha = 1.5, beta = 0.8, size = 100,tours=500)
# test = ACO()
test.getData("queen11_11_formated.col")
# test.getData("le450-15b_formated.col")
# print(test.graph)
# print(test.getMAD())

# test.initialize()
test.initialize_random()
# test.optimize()
test.optimizeHeuristic()

    
#88