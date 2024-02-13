#import relevant libraries needed
import sys
import numpy as np
import pandas as pd
from node import Node

# implement function buildKdTree
def buildKdTree(points, depth = 0):
    rows = len(points)
    if rows == 0:
        return None
    elif rows == 1:
        columns = len(points[0])
        # only one point left so val = current dimension of only point
        return Node(points[0], depth % columns, points[0][depth % columns])
    columns = len(points[0])-1 # -1 to handle indexing
    axis = (depth) % columns
    # sort points based on axis value so we can find median
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
    if closest is None or distance(point, node.point[:11,]) < distance(point, closest[:11,]):
        closest = node.point
    if point[node.axis] <= node.median_val:
        next_node = node.left
        opposite_node = node.right
    else:
        next_node = node.right
        opposite_node = node.left
    # update closest
    closest = nnSearch(next_node, point, closest)
    if opposite_node is not None and (closest is None or distance_lb(point, opposite_node.point[:11,], node.axis) < distance(point, closest[:11,])):
        closest = nn_search(opposite_node, point, closest)

    return closest

# lowerbound distance function
def distance_lb(query_point, point, axis):
    distance = abs(point[axis]-query_point[axis])
    return distance

# function for distance
def distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2))**2))

# main function to read in trainning data to build tree 
if __name__ == '__main__':
    # for now the test data can be recived be given as a file 
    # we need to connect it to the rest of the system so the users data can be calculated
    trainingData_file_path = 'assets/TrainingData.xlsx'
    User_Metric_Data = 'assets/ExampleUserEntry.xlsx'

    # read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # test that data is correctly extracted
    print(df.head())

    # extract training points and build kd_tree from the chosen dimension
    training_points = train_df.values[:, :]
    Kd_tree = buildKdTree(training_points, 0) # 0 represents our starting dimension

    # some sort of loop which runs search with given querry when request is recived

        # use User_Metric_Data as a querry point and run a NN Search
        
        # display / send result 
    
    
    
