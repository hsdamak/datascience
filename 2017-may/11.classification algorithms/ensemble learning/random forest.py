import os
import pandas as pd
from sklearn import ensemble
from sklearn import tree
from sklearn import model_selection
import pydot
import io

#returns current working directory
os.getcwd()
#changes working directory
os.chdir("E:/")

titanic_train = pd.read_csv("train.csv")

#EDA
titanic_train.shape
titanic_train.info()

titanic_train1 = pd.get_dummies(titanic_train, columns=['Pclass', 'Sex', 'Embarked'])
titanic_train1.shape
titanic_train1.info()
titanic_train1.head(6)

X_train = titanic_train1.drop(['PassengerId','Age','Cabin','Ticket', 'Name','Survived'], 1)
y_train = titanic_train['Survived']

#cv accuracy for bagged tree ensemble
rf_estimator1 = ensemble.RandomForestClassifier(n_estimators=5, max_features=4)
scores = model_selection.cross_val_score(rf_estimator1, X_train, y_train, cv = 10)
print(scores.mean())
rf_estimator1.fit(X_train, y_train)

#oob accuracy for bagged tree ensemble
rf_estimator2 = ensemble.RandomForestClassifier(n_estimators=5, max_features=4, oob_score=True)
rf_estimator2.fit(X_train, y_train)
rf_estimator2.oob_score_

rf_estimator1.estimators_

#extracting all the trees build by random forest algorithm
n_tree = 0
for est in rf_estimator1.estimators_: 
    dot_data = io.StringIO()
    tmp = est.tree_
    tree.export_graphviz(tmp, out_file = dot_data, feature_names = X_train.columns)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())[0] 
    graph.write_pdf("rftree" + str(n_tree) + ".pdf")
    n_tree = n_tree + 1