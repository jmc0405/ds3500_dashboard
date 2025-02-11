import pandas as pd

class insuranceAPI:

    def load_insurance(self, filename):
        self.insurance = pd.read_csv(filename)


    def change_smoker(self):


        self.insurance["smoker"] = self.insurance["smoker"].replace({"yes": 'smoker', "no": 'nonsmoker'}).reset_index(drop=True)

    def get_data(self):
        """Return the current state of the DataFrame."""
        return self.insurance
#
def main():

    insurance_api = insuranceAPI()

    # Load the dataset
    insurance_api.load_insurance("insurance.csv")  # Ensure the file name matches your dataset

    # Transform the 'smoker' column
    insurance_api.change_smoker()

    # Check the updated DataFrame
    print(insurance_api.get_data())

if __name__ == '__main__':
    main()
