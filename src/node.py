# Node class for use in KD tree
class Node:
    def __init__(self, point=None, axis=None, median_val=None, left=None, right=None):
        self.point = point
        self.axis = axis
        self.median_val = median_val
        self.left = left
        self.right = right