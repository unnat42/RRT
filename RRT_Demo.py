# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:11:17 2020

@author: Unnat Antani

RRT Demonstration
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import time
from matplotlib.path import Path
import matplotlib.patches as patches 

#Let our workspace span from 0-100 in both axes






def node_select(new_node,Nodes):
    dist = []
    for i in range(len(Nodes)):
        d = math.sqrt((Nodes[i][0]-new_node[0])**2 + (Nodes[i][1]-new_node[1])**2)
        dist.append(d)
    idx = dist.index(min(dist))
    # print(dist)
    if idx != (len(Nodes)-1):
        return(Nodes[idx],2)# 2 refers to the no. of codes to add i.e., Path.MOVETO(Nodes[i]) and Path.LINETO(new_node)
    else:
        return(Nodes[idx],1)# 1 refers to the no. of codes to add i.e., Path.LINETO(new_node)
        
unit_step = 10
Nodes = []
init_node = [10,10] #Define an initial node inside the workspace
goal_node = [60,60] #Defina a goal node inside the workspace
current_node = []
rand_point = [[0,0]]
plot_points = [[init_node[0],init_node[0]],[init_node[1],init_node[1]]]
verts = []
verts.append(init_node)
n = 100 #Define the number of iteratioins you want to perform 

tree_x = []
tree_y = []
Nodes.append(init_node)
current_node.append(init_node[0])
current_node.append(init_node[1])

# print(current_node)

codes = [Path.MOVETO]
# plt.title("Vanilla RRT")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
time.sleep(10)
 
axes = plt.gca()

axes.set_xlim(0, 100)
axes.set_ylim(0, 100)


init, = axes.plot(init_node[0], init_node[1], 'bo', markersize = 10, label = "Start")
goal, = axes.plot(goal_node[0], goal_node[1], 'ro', markersize = 10, label = "Finish")
rand_plot, = axes.plot(rand_point[0][0], rand_point[0][1], 'yo', label = "Random")
tree_node, = axes.plot(tree_x, tree_y, 'go', label = "Tree")
edge, = axes.plot(plot_points[0],plot_points[1], label = "Edge")
chartBox = axes.get_position()
axes.set_position([chartBox.x0,chartBox.y0,chartBox.width*0.6,chartBox.height])
axes.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

rand_point.pop()


for _ in range(n):
    # print("Iteration no: {}".format(i+1))
    plot_points.pop()
    plot_points.pop()

    # rand_point.pop()

    rand_x = random.randrange(0,100)
    rand_y = random.randrange(0,100)
    # print(rand_x,rand_y)
    # rand_point.append([rand_x,rand_y])
    angle = math.atan2((rand_y-current_node[1]), (rand_x-current_node[0]))#Maybe wrong
    new_node = [current_node[0]+(unit_step*np.cos(angle)), current_node[1]+(unit_step*np.sin(angle))]
    d = math.sqrt((new_node[0]-goal_node[0])**2 + (new_node[1]-goal_node[1])**2)
    
    if (d)<=(unit_step):
        Nodes.append(new_node)
        Nodes.append(goal_node)
        verts.append(new_node)
        verts.append(goal_node)
        codes.append(Path.LINETO)
        codes.append(Path.LINETO)
        path = Path(verts,codes)
        patch = patches.PathPatch(path, facecolor = 'None')
        axes.add_patch(patch)
        
        plot_points.append([Nodes[_][0],new_node[0]])
        plot_points.append([Nodes[_][1],new_node[1]])    
        
        for i in Nodes:
            tree_x.append(i[0])
            tree_y.append(i[1])
        tree_node.set_xdata(tree_x)
        tree_node.set_ydata(tree_y)
        
        rand_plot.set_xdata(rand_x)
        rand_plot.set_ydata(rand_y)
        plt.title("RRT iter = {}".format(_+1))
        plt.draw()
        # print("Completed in {} steps".format(_+1))
        
        plt.pause(0.05)
        time.sleep(0.1)
        break
    else:
        node, cd = node_select(new_node, Nodes)
    
        Nodes.append(new_node)
        
        
        # print("New node = {}".format(new_node))
        # print("Nearest node = {}".format(node))
        # print("Second last = {}".format(Nodes[len(Nodes)-2]))
        # # print(node)
        if cd==1:
            verts.append(new_node) 
            codes.append(Path.LINETO) 
        else:
            verts.append(node)
            verts.append(new_node)
            codes.append(Path.MOVETO)
            codes.append(Path.LINETO)
   
        path = Path(verts,codes)
        patch = patches.PathPatch(path, facecolor = 'None')
        axes.add_patch(patch)
        
        plot_points.append([Nodes[_][0],new_node[0]])
        plot_points.append([Nodes[_][1],new_node[1]])    
        
        for i in Nodes:
            tree_x.append(i[0])
            tree_y.append(i[1])
        tree_node.set_xdata(tree_x)
        tree_node.set_ydata(tree_y)
        
        rand_plot.set_xdata(rand_x)
        rand_plot.set_ydata(rand_y)
        
        # edge.set_xdata(plot_points[0])
        # edge.set_ydata(plot_points[1])
        
        
        # init.set_xdata(init_node[0])
        # init.set_ydata(init_node[1])
        plt.title("RRT iter = {}".format(_+1))
        plt.draw()
        plt.pause(0.05)
        time.sleep(0.1)
        
        current_node[0]= new_node[0]
        current_node[1]= new_node[1]
        # if(_==(n-1)):
        #     print("Could not form a complete graph !")
    
plt.show()