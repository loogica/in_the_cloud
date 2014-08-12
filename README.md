# My ML Cloud

The main idea is to make it easy to run heavy cpu processing on the cloud. 

* AWS support only

```python
from my_ml_cloud import process_unit

with process_unit() as instance:
    instance.send_run('ml.py')
```

## Install dependencies

```
$ pip install -r requirements.txt
```

## First Step

Configure a `.env` file in the root dir

```
KEY_NAME=seu_key_name
AWS_ACCESS_KEY=sua_access_key
AWS_SECRET_KEY=sua_secret_key

KEY_PASS=pass_chave

REGION=us-west-2
DEFAULT_INSTANCE_ID=ami-e7b8c0d7
INSTANCE_SIZE=m3.medium
DEFAULT_SECURITY_GROUP=default

SSH_USER=ubuntu
PARAMIKO_DEBUG=True
```

## Second step

Code your ML script. Here's our little example using scikit

```python
import json

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[:-1])

result = dict(result=float(clf.predict(digits.data[-1])),
              algo=repr(clf).replace('\n', ''))
print(json.dumps(result, indent=4))
```

## Last step

Call `compute.py`

```
$ python compute.py
```

## Terminate ALL cloud instances

```
$ python terminate.py
```

## Contact

`felipecruz@loogica.net`
