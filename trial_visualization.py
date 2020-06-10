import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
dataframe1= pd.read_csv("./7000607_9_days_Normal.csv") 
dataframe2= pd.read_csv("./7000607_9days_abnormal.csv")
raw_correct_idx = [1,2,3,4,5,6,7,8,9,20,23,31,33,34,39,40,41,43,44,45,55,60,69,70,71,72,73,74,75,76,79,80,81,82,83]


correct_idx=[]
correct_idx_labels=[]
problem_idx=[]
problem_idx_labels=[]
useless= [56,57,58,59,64,65,66,67,84,85,86,87,88]
useles=[]

for i in raw_correct_idx:
    correct_idx.append(i-1)
    correct_idx_labels.append(dataframe1.columns.values[i-1])
for i in useless:
    useles.append(i-1)
for i in range(dataframe2.shape[1]):
    if (i not in correct_idx) and (i not in useles):
        problem_idx.append(i)     
        problem_idx_labels.append(dataframe1.columns.values[i])      
    
normal_data_correct = dataframe1.loc[:,correct_idx_labels]
normal_data_faulty = dataframe1.loc[:,problem_idx_labels]
abnormal_data_correct = dataframe2.loc[:,correct_idx_labels]
abnormal_data_faulty = dataframe2.loc[:,problem_idx_labels]
xfaulty = list(normal_data_faulty.columns.values)


faulty_sensor=[]    
r = defaultdict(list)
def train_and_predict(traindata,traindatafaulty,testdata,testdatafaulty):
    for i in range(len(xfaulty)):
            dataset = pd.concat([traindata,traindatafaulty.loc[:,xfaulty[i]]],axis=1)    
            testdataset = pd.concat([testdata,testdatafaulty.loc[:,xfaulty[i]]],axis=1) 
            lr = LinearRegression()
            lr.fit(dataset.iloc[:,:-1],dataset.iloc[:,-1])    
            accuracy = lr.score(testdataset.iloc[:,:-1],testdataset.iloc[:,-1])
            predictions = lr.predict(testdataset.iloc[:,:-1])
            #print(predictions)
            r[xfaulty[i]]=predictions
            loss=np.sqrt(np.mean((predictions - testdatafaulty.loc[:,xfaulty[i]])**2))
            if(loss>50):
                #threshold=200
                faulty_sensor.append(xfaulty[i])        
    return accuracy,r,faulty_sensor
acc,predictions,faulty_sensor = train_and_predict(normal_data_correct,normal_data_faulty,abnormal_data_correct,abnormal_data_faulty) 
final_result = pd.concat([abnormal_data_correct,pd.DataFrame(predictions)],axis=1)
sns.set_style("whitegrid")

for i in range(len(faulty_sensor)):
    x = np.linspace(0, 1000,len(abnormal_data_faulty[faulty_sensor[i]]))
    fig, ax = plt.subplots()
    ax.plot(x,predictions[faulty_sensor[i]], '-b', label='Predicted')
    plt.xlabel('Samples', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    ax.plot(x, abnormal_data_faulty.loc[:,faulty_sensor[i]], '-r', label='Actual data')
    plt.title('The graph for sensor:'+faulty_sensor[i]);
    ax.legend();
    plt.savefig(r'.\static\SensorsPlots\sensor'+str(i)+'.png')
       