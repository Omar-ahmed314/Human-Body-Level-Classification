import pandas as pd
from sklearn.preprocessing import StandardScaler

categorial_columns = ['Alcohol_Consump', 'Food_Between_Meals','Transport']

labelsMap = {'Body Level 1': 0, 
             'Body Level 2': 1,
             'Body Level 3': 2,
             'Body Level 4': 3}

normalizeColumns = ['BMI', 'Age', 'Weight', 'Height', 'Veg_Consump', 'Water_Consump', 'Meal_Count', 'Phys_Act', 'Time_E_Dev']

#Map categorical features to 1 and 0
genderMapping = {"Male": 1, "Female": 0}
YesNoMapping = {"yes": 1, "no": 0} #For cal consump, smoking, fam hist, cal burn

#Fuction that applies same processing on test data as training data
def performInference():
    df_train = pd.read_csv('body_level_classification_train.csv')
    df_test = pd.read_csv('test.csv')

    df_train["Gender"] = df_train["Gender"].map(genderMapping)
    df_train["H_Cal_Consump"] = df_train["H_Cal_Consump"].map(YesNoMapping)
    df_train["Smoking"] = df_train["Smoking"].map(YesNoMapping)
    df_train["Fam_Hist"] = df_train["Fam_Hist"].map(YesNoMapping)
    df_train["H_Cal_Burn"] = df_train["H_Cal_Burn"].map(YesNoMapping)

    df_test["Gender"] = df_test["Gender"].map(genderMapping)
    df_test["H_Cal_Consump"] = df_test["H_Cal_Consump"].map(YesNoMapping)
    df_test["Smoking"] = df_test["Smoking"].map(YesNoMapping)
    df_test["Fam_Hist"] = df_test["Fam_Hist"].map(YesNoMapping)
    df_test["H_Cal_Burn"] = df_test["H_Cal_Burn"].map(YesNoMapping)

    #combine x_train and df_test to get all possible values for categorical features
    x_train = df_train.drop(['Body_Level'], axis=1)
    y_train = df_train['Body_Level']
    combined = pd.concat([x_train, df_test], axis=0)

    #apply one hot encoding on categorical features
    combined = pd.get_dummies(combined, columns=categorial_columns, dtype=int)

    #split combined back into x_train and df_test
    x_train = combined.iloc[:len(x_train), :]
    df_test = combined.iloc[len(x_train):, :]

    #combine x_train and y_train
    df_train = pd.concat([x_train, y_train], axis=1)

    #calculate BMI Column for both datasets
    df_train['BMI'] = df_train['Weight'] / (df_train['Height']*df_train['Height'])
    df_test['BMI'] = df_test['Weight'] / (df_test['Height']*df_test['Height'])

    #standardize continuous columns
    scaler = StandardScaler()   
    scaler = scaler.fit(df_train[normalizeColumns])

    df_train[normalizeColumns] = scaler.transform(df_train[normalizeColumns])
    df_test[normalizeColumns] = scaler.transform(df_test[normalizeColumns])

    #Encode labels
    df_train['Body_Level'] = df_train['Body_Level'].map(labelsMap)

    #Write to csv
    df_train.to_csv('train_processed.csv', index=False)
    df_test.to_csv('test_processed.csv', index=False)


if __name__ == "__main__":
    performInference()