import re
from typing import *
from copy import deepcopy, copy
from functools import cache
from math import inf
import networkx as nx
import matplotlib.pyplot as plt
import heapq

class Graph():
    def __init__(self, nodes = None):
        if not nodes:
            nodes = []
        self.nodes = dict((key, value) for key, value in [(node.n, node) for node in nodes])
        self.same_dir = 0

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node.n] = node
    
    def add_neigh(self, node_1, node_2, reciprocal = True):
        n1, n2 = self.get_node(node_1), self.get_node(node_2)
        if n2.n not in n1.neighbours:
            n1.neighbours.append(n2.n)
        if reciprocal and n1.n not in n2.neighbours:
            n2.neighbours.append(n1.n)
    
    def get_dir(self, node_1, node_2):
        if node_1 == "start" or node_2 == "end":
            return (0,1)
        if node_2 == "start" or node_1 == "end" :
            return (0,-1)
            
        n1 = (int(node_1.split("_")[0]),int(node_1.split("_")[1]))
        n2 = (int(node_2.split("_")[0]),int(node_2.split("_")[1]))
        return (n2[0]-n1[0],n2[1]-n1[1])
        
    def calculate_distances(self, end, minc, maxc):
        f = open("log.txt",'w+')
        distances = set()
        pq = [(self.get_node("0_1").v, 1, (0,1), "0_1"),(self.get_node("1_0").v, 1, (1,0), "1_0")]
        heapq.heapify(pq)
        
        while pq:
            current_distance, combo, direction, current_node  = heapq.heappop(pq)
            key = (current_node, combo, direction)
      
            #If node already treated with same direction and combo
            if key in distances:
                continue

            #If end node found, return its current_distance
            if end == current_node and combo >= minc:
                return current_distance
                
            distances.add(key)
            
            for neighbour in self.get_node(current_node).possible_neighbours(direction):
                val = self.get_node(neighbour).v
                distance = current_distance + val
                f.write(f"\n\nCurrently at {current_node} evaluating {neighbour} (val = {val}).\nDistance to reach {neighbour} would be {distance}. Last movement used to reach: {direction}\nsame_dir : {combo}")
                _direction = self.get_dir(current_node, neighbour)
                
                if combo < minc and direction != _direction and direction != (0,0):
                    continue
                if combo > maxc: 
                    continue
                    
                if direction == _direction or direction == (0,0): #Same direction
                    _combo = combo + 1
                   
                else: #Changed directions
                    _combo = 1

    
                heapq.heappush(pq,(distance, _combo, _direction,neighbour))
                f.write(f"\nAdded {neighbour} to heap. Combo is now {_combo}, and direction is {_direction}")


        f.close()
            
    def get_node(self, label):
        return self.nodes[label]
    
    def __str__(self):
        s = ""
        line = 0
        for n in self.nodes.keys():
            if int(n.split("_")[0]) == line+1:
                line += 1
                s += "\n"
            s += n
            if n.split("_")[0] + "_" + str(int(n.split("_")[1])+1) in self.nodes.keys():
                s += ' - '
            else:
                s += '   '
        return s
    
class Node():
    def __init__(self, label, value):
        self.n = label
        self.neighbours = []
        self.v = value
        
    def __str__(self):
        return self.n
        
    def __repr__(self):
        return str(self.v)
    
    def possible_neighbours(self, d):
        if self.n == "start":
            return ["0_0"]
        elif self.n == "end":
            return [en]
        
        dx = -d[0]
        dy = -d[1]
        x = int(self.n.split("_")[0])
        y = int(self.n.split("_")[1])
        
        return [n for n in self.neighbours if n != f"{x+dx}_{y+dy}"]
                
    
def get_2d_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        t = f.read().splitlines()
        t = [re.findall(r'\d', line) for line in t]
        return [[int(x) for x in line]for line in t]
   

def part1(input_name: str) -> int:
    matrix = get_2d_array(input_name)
    size = (len(matrix),len(matrix[0]))
    G = Graph()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            G.add_node(Node(f"{i}_{j}", matrix[i][j]))

    G.add_node(Node("end",0))
    
    for i in range(size[0]):
        for j in range(size[1]):
            if i > 0:
                G.add_neigh(f"{i}_{j}",f"{i-1}_{j}")
            if i < size[0]-1:
                G.add_neigh(f"{i}_{j}",f"{i+1}_{j}")
            if j > 0:
                G.add_neigh(f"{i}_{j}",f"{i}_{j-1}")
            if j < size[1]-1:
                G.add_neigh(f"{i}_{j}",f"{i}_{j+1}")
    global st, en
    
    st = "0_0"
    en = f"{size[0]-1}_{size[1]-1}"
    
    G.add_neigh(en, "end")

    
    p = G.calculate_distances(en, 1, 3)
    print(p)

part1("sample.txt")
