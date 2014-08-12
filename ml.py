import json

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[:-1])

result = dict(result=float(clf.predict(digits.data[-1])),
              algo=repr(clf).replace('\n', ''))
print(json.dumps(result, indent=4))
