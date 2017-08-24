
import pickle
import operator
import copy
import sys
sys.path.append('../tools/')
from feature_format import featureFormat,targetFeatureSplit
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split,StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.linear_model import  LogisticRegression
from sklearn.preprocessing import  StandardScaler
from matplotlib import pyplot as plt
import seaborn as sns


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".# You will need to use more features

features_list = ['poi',
                 'salary',
                 'bonus',
                 'to_messages',
                 'deferral_payments',
                 'total_payments',
                 'loan_advances',
                 'restricted_stock_deferred',
                 'deferred_income',
                 'total_stock_value',
                 'expenses',
                 'from_poi_to_this_person',
                 'exercised_stock_options',
                 'from_messages',
                 'from_this_person_to_poi',
                 'long_term_incentive',
                 'shared_receipt_with_poi',
                 'restricted_stock',
                 'director_fees']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)



### Task 2: Remove outliers

Outliers_List=['TOTAL','THE TRAVEL AGENCY IN THE PARK','LOCKHART EUGENE E']

def outlier_remover(dit,List_Outliers):
    new_dit=copy.deepcopy(dit)
    for i in List_Outliers:
        del new_dit[i]
    return new_dit

new_dict=outlier_remover(data_dict,Outliers_List)

### Task 3: Create new feature(s)


def new_features_creator(dit,new_feature_name):
    for i in new_feature_name:
        if i == 'to_and_from_poi':

            for name in dit.keys():
                a,b = dit[name]['from_this_person_to_poi'],dit[name]['from_poi_to_this_person']
                if type(a)==str:
                    val1=float(0)
                else:
                    val1=float(a)
                if type(b)==str:
                    val2=float(0)
                else:
                    val2=float(b)

                sum=val1+val2
                dit[name]['to_and_from_poi']=sum


        elif i=='total_wealth':
            for name in dit.keys():
                a,b,c,d = dit[name]['salary'],dit[name]['bonus'],\
                          dit[name]['total_stock_value'],dit[name]['exercised_stock_options']

                if type(a)==str:
                    val1=float(0)
                else:
                    val1=float(a)

                if type(b)==str:
                    val2=float(0)
                else:
                    val2=float(b)

                if type(c)==str:
                    val3=float(0)
                else:
                    val3=float(c)

                if type(d)==str:
                    val4=float(0)
                else:
                    val4=float(d)

                sum=val1+val2+val3+val4
                dit[name]['total_wealth']=sum

    return dit


new_dict=new_features_creator(new_dict,['to_and_from_poi','total_wealth'])

#Update list of feature list

features_list+=['to_and_from_poi','total_wealth']





### Store to my_dataset for easy export below.
my_dataset = new_dict




# select best 10 features
# We will use SelectKbest from sklearn

def selector():
    data = featureFormat(my_dataset, features_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)
    selector=SelectKBest(f_classif)
    selector.fit(features,labels)
    list_=list(zip(features_list[1:],selector.scores_))
    list_.sort(key=operator.itemgetter(1),reverse=True)
    #print(list_)
    a,b=(zip(*list_))
    palette=sns.color_palette(palette='Blues_d',n_colors=20)
    plt.figure(figsize=(8,8))
    plt.title('Score Distribution')
    sns.barplot(list(b),list(a),palette=palette)
    plt.xlabel('Scores')
    plt.ylabel('Features')
    plt.tight_layout()
    plt.show()
    l=list(a[:9])
    return ['poi']+l

features_new=selector()
#print(features_new)

'''
Best 10 features:['poi', 
                  'total_wealth',
                  'exercised_stock_options',
                  'total_stock_value', 
                  'bonus',
                  'salary',
                  'deferred_income',
                  'long_term_incentive',
                  'restricted_stock',
                  'total_payments']
'''

'''Create features and labels from the dataset'''

data = featureFormat(my_dataset, features_new, sort_keys = True)
labels, features = targetFeatureSplit(data)

#Number of POIs in dataset

print(sum(labels))


'''Split the features and labels for training and testing'''

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)






### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html



'''
Firstly I will perform feature scaling,then dimensionality reduction using principle component 
analysis.I have choosen three machine learning algorithms; logistic regression,support vector machine,
decision trees and kneighborsclassifier.For this , we will write a function which gives 
best classifier for the given data along with its best parameters.
'''

list_classifier=['svc','dtc','knn']

def best_estimator(classifier,features_train,labels_train,features_test):

    param_mapping={

         'lor':{
             'reduce_dim__n_components':list(range(1,10)),
             'lor__C':[0.00000001,0.00001,1.0],
             'lor__tol':[1e-3,1e-1],
             'lor__penalty':['l1','l2'],
             'lor__random_state':[42]
              },

         'svc':{
                'svc__kernel':['rbf'],
                'svc__C':[10000,100000,1000],
                'svc__gamma':[0.001,0.0001,'auto'],
                'svc__random_state':[68]},

         'dtc':{

                'dtc__criterion':['entropy','gini'],
                'dtc__min_samples_split':[5,10,8,10,12],
                'dtc__random_state':[68],
                'dtc__min_samples_leaf':[4,6,8,10,12],
                },

         'knn':{
                'reduce_dim__n_components':list(range(1,10)),
                'knn__n_neighbors':[5,7,11],
                'knn__algorithm':['ball_tree','kd_tree','brute','auto'],
                'knn__leaf_size':[2,3,5,10,12]}

         }


    steps={
            'svc':[(),('scale',StandardScaler()),('svc',SVC())],
            'dtc':[('scale',StandardScaler()),('dtc',DecisionTreeClassifier())],
            'knn':[('scale',StandardScaler()),('reduce_dim',PCA()),('knn',KNeighborsClassifier())],
            'lor':[('scale',StandardScaler()),('reduce_dim',PCA()),('lor',LogisticRegression())]
           }


    pipe = Pipeline(steps[classifier])
    tune_params=param_mapping[classifier]
    sss = StratifiedShuffleSplit(n_splits=50, test_size=0.1, random_state=42)

    grid_search = GridSearchCV(estimator=pipe,
                               param_grid=tune_params,
                               scoring='f1',
                               error_score=0,
                               cv=sss
                               )
    grid_search.fit(features_train, labels_train)
    predictions = grid_search.predict(features_test)

    clf1 = grid_search.best_estimator_
    clf1_parm=grid_search.best_params_

    return clf1,clf1_parm



'''
Trying different classifiers

svc:Support Vector Machine
dtc:Decision Tree Classifier
knn:KNeighbors Classifier
lor:Logistic Regression

'''


'''                       Uncomment to run  '''

'''Support vector machine'''
#clf1,clf1_parm= best_estimator('svc',features_train,labels_train,features_test)


'''Decision Tree classifier'''
#clf2,clf2_parm= best_estimator('dtc',features_train,labels_train,features_test)


'''KNeighbors Classifier'''
#clf3,clf3_parm= best_estimator('knn',features_train,labels_train,features_test)




'''Logistic Regression (Selected Classifier)'''
clf4,clf4_parm= best_estimator('lor',features_train,labels_train,features_test)


'''
Getting the classification report of these classifiers using score_cal function.

'''
def score_cal(clf1,title,param1,features_test=features_test,labels_test=labels_test):
    print(" ")
    print(title)
    print("Best Parameters")
    print(param1)
    print(classification_report(clf1.predict(features_test),labels_test))
    print("\n")







'''                 Uncomment To calculate              '''



'''Support vector machine'''
#score_cal(clf1,'Support Vector Machine',clf1_parm)


'''Decision Tree classifier'''
#score_cal(clf2,'Decision Tree Classifier',clf2_parm)


'''KNeighbors Classifier'''
#score_cal(clf3,'KNeighborsClassifier',clf3_parm)



'''Logistic Regression'''
score_cal(clf4,'LogisticRegression',clf4_parm)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.


'''
Out of these classifiers, Logistic Regression gives better precision and 
recall values. Hence I have choosen this classifier as my final classifier and
 I will test the classifier using the tester.py script provided to me.
Then I will dump this classifier, dataset and features  used to three pickle files.

'''




'''Dumping the best classifier,dataset and features used into pickle files compatible in python 2 and 3'''

CLF_PICKLE_FILENAME = "my_classifier.pkl"
DATASET_PICKLE_FILENAME = "my_dataset.pkl"
FEATURE_LIST_FILENAME = "my_feature_list.pkl"

def dump_classifier_and_data(clf, dataset, feature_list):
    with open(CLF_PICKLE_FILENAME, "wb") as clf_outfile:
        pickle.dump(clf, clf_outfile,protocol=2)
    with open(DATASET_PICKLE_FILENAME, "wb") as dataset_outfile:
        pickle.dump(dataset, dataset_outfile,protocol=2)
    with open(FEATURE_LIST_FILENAME, "wb") as featurelist_outfile:
        pickle.dump(feature_list, featurelist_outfile,protocol=2)


'''Dumping the best classifier,dataset and features used'''

dump_classifier_and_data(clf4, my_dataset, features_new)
