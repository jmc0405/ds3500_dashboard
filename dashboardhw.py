import pandas as pd

def read_csv(filename):
    """

    :param filename: filename of csv file
    :return: the file content as a dataframe
    """
    df = pd.read_csv(filename)
    return df

def change_var_name(df):
    """

    :param df: The dataframe
    :return: The dataframe with changed variable names(in this case
    yes is replaced with smoker and no is replaced with nonsmoker for the smoker
    calumns
    """
    df["smoker"] = df["smoker"].replace({"yes": 'smoker', "no": 'nonsmoker'})
    return df



def main():

    read_data = read_csv("insurance.csv")
    change_var_name(read_data)
    print(change_var_name(read_data))

if __name__ == '__main__':
    main()
