
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from datetime import datetime
import seaborn as sns
from sklearn.metrics import confusion_matrix

sns.set_style('darkgrid')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

# Any results you write to the current directory are saved as output.
df_codes = pd.read_csv('offense_codes.csv', encoding='ISO-8859-1')
df_codes.head()
df = pd.read_csv('crime.csv', encoding='ISO-8859-1')
df.head()
df.isnull().sum()
df.drop(['DISTRICT', 'SHOOTING', 'UCR_PART', 'STREET', 'Lat', 'Long'], axis=1, inplace=True)
sorted(df['REPORTING_AREA'].unique())[:10]
## replace empty reporting areas with '-1'
df['REPORTING_AREA'] = df['REPORTING_AREA'].str.replace(' ', '-1')
sorted(df['REPORTING_AREA'].unique())
df['REPORTING_AREA'] = df['REPORTING_AREA'].astype(int)
# code day of week to ints
df['OCCURRED_ON_DATE'] = pd.to_datetime(df['OCCURRED_ON_DATE'])
df['DAY_OF_WEEK'] = df['OCCURRED_ON_DATE'].dt.dayofweek
df['OFFENSE_CODE_GROUP'].value_counts().plot(kind='bar', figsize=(20,5), title='Offense Code Group Counts')
df_new = df.copy(deep=True)
df_new['MV'] = np.where(df_new['OFFENSE_CODE_GROUP'] == 'Motor Vehicle Accident Response', 1, 0)
df_new.head()
df_mv = df_new[['MV', 'REPORTING_AREA', 'YEAR', 'MONTH', 'DAY_OF_WEEK', 'HOUR']]
df_mv.head()

# LogisticRegression

print("Logistic Regression")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
# shuffle the data if you want
df_mv = df_mv.sample(frac=1).reset_index(drop=True)
X = df_mv[df_mv.columns[1:]]
y = df_mv['MV']
X_train, X_test, y_train, y_test = train_test_split(X,y)
reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
y_pred = reg.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, f1_score

print("ACCURACY")
print(accuracy_score(y_test, y_pred) * 100)
print("CLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))
print("CONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))


# SVM Model
print("SVM")
from sklearn import svm
lin_clf = svm.LinearSVC()
lin_clf.fit(X_train, y_train)
predict_svm = lin_clf.predict(X_test)
svm_acc = accuracy_score(y_test, predict_svm) * 100
print(svm_acc)
print("CLASSIFICATION REPORT")
print(classification_report(y_test, predict_svm))
print("CONFUSION MATRIX")
print(confusion_matrix(y_test, predict_svm))

## To get more output about coefficients of logistic regression use statsmodels to perform same logistic regression

import statsmodels.discrete.discrete_model as sm
from statsmodels.tools.tools import add_constant

# statsmodels doesn't include a constant by default
# sklearn.linear_model DOES include a constant by default
X_ols = add_constant(X)

sm.Logit(y,X_ols).fit().summary()
df_knn = df[df['OFFENSE_CODE_GROUP'].isin(list(df['OFFENSE_CODE_GROUP'].value_counts()[:3].index))].copy(deep=True)



# KNeighborsClassifier

print("KNeighbors Classifier::")

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

lb_make = LabelEncoder()
df_knn['office_code_lbl'] = lb_make.fit_transform(df_knn['OFFENSE_CODE_GROUP'])

df_knn = df_knn[['office_code_lbl', 'REPORTING_AREA', 'YEAR', 'MONTH', 'DAY_OF_WEEK', 'HOUR']]

X = df_knn[['REPORTING_AREA', 'YEAR', 'MONTH', 'DAY_OF_WEEK', 'HOUR']]
y = df_knn['office_code_lbl']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
neighbors_list = np.arange(1,5)
scores = []
for n_neighbors in neighbors_list:
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    knn_pred = knn.predict(X_test)
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix, f1_score
    if(n_neighbors==1):
        print("Accuracy::")
        print(accuracy_score(y_test, knn_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knn_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knn_pred))


