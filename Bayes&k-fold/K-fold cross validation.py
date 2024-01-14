import random
import numpy as np
from xgboost import XGBClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


def get_splits(n, k, seed):
  splits = []
  # Implement your code to construct the splits here
  np.random.seed(seed)  # set random seed
  indices = np.arange(n)  # create an array
  np.random.shuffle(indices)  #

  # size of the group(not counting extra element)
  split_size = n // k
  # index of the group that has extra element
  change_mark = n % k

  start = 0  # start index
  for i in range(k):
    if (i < change_mark):
      offset = 1
    else:
      offset = 0
    end = start + split_size + offset
    splits.append(list(indices[start:end]))  # add to current list
    start = end  # update next group index

  return splits

def my_cross_val(method, X, y, splits):
  errors = []
  # Implement your code to calculate the errors here
  # choose the correct model
  if method == 'LinearSVC':
    model = LinearSVC(max_iter=2000, random_state=412)
  if method == 'SVC':
    model = SVC(gamma='scale', C=10, random_state=412)
  if method == 'LogisticRegression':
    model = LogisticRegression(penalty='l2', solver='lbfgs', random_state=412, multi_class='multinomial')
  if method == 'RandomForestClassifier':
    model = RandomForestClassifier(max_depth=20, n_estimators=500, random_state=412)
  if method == 'XGBClassifier':
    model = XGBClassifier(max_depth=5, random_state=412)

  for test_split in splits:
    # np.concatenate to create training set
    train_list = []
    test_list = test_split
    #create test and training set
    for i in range(len(splits)):
      if(splits[i]==test_split):
        continue
      #add to training set if it is not test dataset
      train_list.extend(splits[i])

    train_list.sort()
    test_list.sort()
    # train and test set
    x_train = X[train_list]
    x_test = X[test_list]
    y_train = y[train_list]
    y_test = y[test_list]


    # init model
    model.fit(x_train, y_train)  # train
    y_pred = model.predict(x_test)  # pred
    #calculate error rate
    # total=0
    # for i in len(y_pred):
    #   if(y_pred[i] != y_test_set[i]):
    #     total +=1
    # error = total/len(y_pred)
    error = np.mean(y_pred != y_test)  # error
    errors.append(error)  # error rate for each fold
  return np.array(errors)