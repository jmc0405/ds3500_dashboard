import pandas as pd

def read_csv(filename):
    df = pd.read_csv(filename)
    return df

def main():

    read_data = read_csv("insurance.csv")
    print(read_data)


if __name__ == '__main__':
    main()