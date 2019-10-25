# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import numpy as np
from sklearn import tree


col_names = ['obj1','obj2','obj3','obj4','obj5','obj6','obj7','subcat1','asin']
# load dataset
pima = pd.read_csv("/home/ademir/Documents/without_person_second___.csv", header=None, names=col_names)

#split dataset in features and target variable
feature_cols = ['obj1','obj2','obj3','obj4','obj5','obj6','obj7']
X = pima[feature_cols] # Features
y = pima.subcat1 # Target variable


from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')
X_enc = enc.fit_transform(X)



# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X_enc, y, test_size=0.3, random_state=1) # 70% training and 30% test


# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


'''
import hmc
from sklearn.impute import MissingIndicator
from sklearn.impute import SimpleImputer


#X_train = pd.DataFrame(X_train.toarray()).fillna(0)
X_train = pd.DataFrame(X_train).fillna(0)
X_train = pd.Series(X_train)
print X_train
ch = hmc.load_shades_class_hierachy()
dth = hmc.DecisionTreeHierarchicalClassifier(ch)
dth = dth.fit(X_train, y_train)
dth_predicted = dth.predict(X_test)
dth_accuracy = dth.score(X_test, y_test)'''


'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer

from sklearn import tree
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn import tree

import hmc
ch = hmc.ClassHierarchy("colors")
ch.add_node("light", "colors")
ch.add_node("dark", "colors")
ch.add_node("white", "light")
ch.add_node("black", "dark")
ch.add_node("gray", "dark")
ch.add_node("slate", "gray")
ch.add_node("ash", "gray")

ch.print_()


ch = hmc.load_shades_class_hierachy()
X, y = hmc.load_shades_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.50)

dt = tree.DecisionTreeClassifier()
dt = dt.fit(X_train, y_train)
dt_predicted = dt.predict(X_test)
dt_accuracy = dt.score(X_test, y_test)

dth = hmc.DecisionTreeHierarchicalClassifier(ch)
dth = dth.fit(X_train, y_train)
dth_predicted = dth.predict(X_test)
dth_accuracy = dth.score(X_test, y_test)'''
'''

df_books = pd.read_csv('/home/ademir/Documents/without_person_second___.csv', encoding='utf-8')
grouped_labels = df_books.groupby("subcat1", sort='count').size().reset_index(name='count')
fig = plt.figure(figsize=(12,10))
grouped_labels.plot(figsize=(12,7), title="Tag frequency")
#plt.show()

multilabel_binarizer = MultiLabelBinarizer()
multilabel_binarizer.fit(df_books.subcat1)
Y = multilabel_binarizer.transform(df_books.subcat1)
print (Y)
count_vect = CountVectorizer()
X_counts = count_vect.fit_transform(df_books.obj1)

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=9000)
X_tfidf_resampled, Y_tfidf_resampled = ros.fit_sample(X_counts, Y)

x_train_tfidf, x_test_tfidf, y_train_tfidf, y_test_tfidf = train_test_split(X_tfidf_resampled, Y_tfidf_resampled, test_size=0.2, random_state=9000)

fig = plt.figure(figsize=(20,20))
(ax_test, ax_train) = fig.subplots(ncols=2, nrows=1)
g1 = sns.barplot(x=Y.sum(axis=0), y=multilabel_binarizer.classes_, ax=ax_test)
#g2 = sns.barplot(x=y_train_tfidf.sum(axis=0), y=multilabel_binarizer.classes_, ax=ax_train)
g1.set_title("class distribution before resampling")
#g2.set_title("class distribution in training set after resampling")
#plt.show()'''