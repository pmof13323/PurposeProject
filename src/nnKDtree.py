#import relevant libraries needed
import sys
import numpy as np
import pandas as pd
from node import Node

# implement function to build Kd Tree
def buildKdTree(points, depth = 0):
    rows = len(points)
    if rows == 0:
        return None
    elif rows == 1: # only one point left so val = current dimension of only point
        columns = len(points[0])
        return Node(points[0], depth % columns, points[0][depth % columns])
    columns = len(points[0])-1 # -1 to handle indexing
    axis = (depth) % columns
    sorted_points = sorted(points, key=lambda point: point[axis])
    median_index = rows // 2
    median_value = sorted_points[median_index][axis]
    median_point = sorted_points[median_index]
    # create nodes for left and right subtrees
    left = buildKdTree(sorted_points[:median_index], depth + 1)
    right = buildKdTree(sorted_points[median_index+1:], depth + 1)
    # create node for current point
    return Node(median_point, axis, median_value, left, right)

# function for searching the Kd-tree
def nnSearch(node, point, closest=None):
    if node is None:
        return closest
    # check if current distance is smaller then closest distance
    if closest is None or distance(point, node.point[:35,]) < distance(point, closest[:35,]):
        closest = node.point
    if point[node.axis] <= node.median_val:
        next_node = node.left
        opposite_node = node.right
    else:
        next_node = node.right
        opposite_node = node.left
    # update closest
    closest = nnSearch(next_node, point, closest)
    if opposite_node is not None and (closest is None or distance_lb(point, opposite_node.point[:35,], node.axis) < distance(point, closest[:35,])):
        closest = nnSearch(opposite_node, point, closest)

    return closest

# lowerbound distance function
def distance_lb(query_point, point, axis):
    return abs(point[axis] - query_point[axis])

# function for distance
def distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2))**2))

# main function to read in trainning data to build tree 
if __name__ == '__main__':
    # for now the test data can be recived be given as a file 
    # we need to connect it to the rest of the system so the users data can be calculated
    trainingData_file_path = 'assets/TrainingData.xlsx'
    User_Metric_Data = 'assets/ExampleUserEntry.xlsx'
    # -> to test working data set
    # user_metric_data_file_path = '../assets/UserScores.csv'

    # read the Excel file into a pandas DataFrame
    cols_to_use = list(range(35))
    train_df = pd.read_excel(trainingData_file_path, usecols=cols_to_use)
    training_points = train_df.values[:, 1:]  # Exclude the occupation column
    labels = train_df.iloc[:, 0].values  # Extract the labels

    Kd_tree = buildKdTree(training_points, 0) # 0 represents our starting dimension

    # Read user metrics data
    user_df = pd.read_excel(User_Metric_Data, usecols=cols_to_use)
    user_point = user_df.values[0, 1:] 

    # Perform nearest neighbor search
    closest_point = nnSearch(Kd_tree, user_point)

    # brain dead tempoary solution -> search the data set for the label that matches the node
    closest_label = labels[np.where((training_points == closest_point).all(axis=1))[0][0]]

    print(closest_label)
    
    
    
