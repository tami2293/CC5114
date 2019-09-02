import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def normalize(df, col_name, high, low):
    """
    Returns a normalized dataframe with high and low defined values
    :param df:
    :param col_name:
    :param high:
    :param low:
    :return: Dataframe
    """
    maximum = df[col_name].max()
    minimum = df[col_name].min()
    return ((df[col_name] - minimum)/(maximum - minimum))*(high - low) + low


def is_not_numerical(df, col_name):
    """
    Returns false if the values type of a certain column is numerical (int64) and true otherwise
    :param df:
    :param col_name:
    :return: boolean
    """
    return df[col_name].dtypes != 'int64'


def encode_data(df, col_name):
    """
    Applies 1-hot encoding to a categorical column of a dataframe.
    :param df:
    :param col_name:
    :return: Dataframe
    """
    unique_values = df[col_name].unique()
    unique_values_len = len(unique_values)

    # Create a dictionary to assign numerical values
    dic = dict()
    for value in unique_values:
        dic.update({value: np.where(unique_values == value)[0][0]})

    # Create temp dataframe to store transformed values
    temp_df = df.replace({col_name: dic})[col_name]
    matrix = np.eye(temp_df.max() + 1)
    # Create one column per bit
    encoded = [matrix[value] for value in temp_df.data]
    bits_df = pd.DataFrame(encoded, dtype=int)
    bits_num = matrix.shape[0]
    bits_df.columns = [col_name + str(i) for i in range(bits_num)]

    return bits_df


# Original data columns
data_cols = ["Age", "Workclass", "Final Weight", "Education", "Education-num", "Marital Status",
             "Occupation", "Relationship", "Race", "Sex", "Capital Gain", "Capital Loss",
             "Hours Per Week", "Native Country", "Class"]

# Education column deleted (useless)
final_data_cols = ["Age", "Workclass", "Final Weight", "Education-num",
                   "Marital Status", "Occupation", "Relationship", "Race", "Sex", "Capital Gain",
                   "Capital Loss", "Hours Per Week", "Native Country", "Class"]

# Reading and concatenating data
data1 = pd.read_csv("adultdata.txt", sep=", ", header=None, names=data_cols, na_values='?')
data2 = pd.read_csv("adulttest.txt", sep=", ", header=None, skiprows=1, names=data_cols, na_values='?')
data = pd.concat([data1, data2], ignore_index=True)

# Deleting Education column from the dataset
data = data.filter(items=final_data_cols)

# Filtering
data = data.dropna(axis=0)

# Normalization and 1-hot encoding

# For each column, normalizes its numerical values and maps its non-numerical values to numerical values
# numeric_col = 0
aux_data = []
df_to_remove = []

for col in data.columns:
    if is_not_numerical(data, col):
        # numeric_col += 1
        aux_data.append(encode_data(data, col))
        df_to_remove.append(col)
    else:
        data[col] = normalize(data, col, 1, 0)
data = data.drop(columns=df_to_remove)

#Reset indexes
data = data.reset_index(drop=True)
for aux_df in aux_data:
    aux_df = aux_df.reset_index(drop=True)
aux_data.append(data)
data = pd.concat(aux_data, axis=1)

#Data frame to numpy array
data = data.reset_index(drop=True)
final_class_list = []
final_data_list = []
for attrib in data.columns:
    # Add columns that belong to Class (expected result)
    if 'Class' in attrib:
        final_class_list.append(attrib)
    # Add columns that belong to data
    else:
        final_data_list.append(attrib)

final_data = data.drop(columns=final_class_list)
final_class = data.drop(columns=final_data_list)
final_data = final_data.values
final_class = final_class.values

X_train, X_test, y_train, y_test = train_test_split(final_data, final_class, test_size=0.2, random_state=42)
X_train = X_train.transpose()
X_test = X_test.transpose()
y_train = y_train.transpose()
y_test = y_test.transpose()



