# Import the Sklearn libraries
from sklearn.datasets import load_iris
from sklearn import tree

# Graphviz importing error on Windows was resolved like this
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
import graphviz 


# Load in our dataset
iris_data = load_iris()

# Initialize our decision tree object
classification_tree = tree.DecisionTreeClassifier()

# Train our decision tree (tree induction + pruning)
classification_tree = classification_tree.fit(iris_data.data, iris_data.target)

all_graph_data = tree.export_graphviz(classification_tree, out_file=None, 
                     feature_names=iris_data.feature_names,  
                     class_names=iris_data.target_names,  
                     filled=True, rounded=True,  
                     special_characters=True)  
graph = graphviz.Source(all_graph_data)  
graph.render("iris")
