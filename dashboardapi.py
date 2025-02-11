"""
Author: Shrey Sahni
Date: February 11th, 2025

Description: This script (dashboardapi.py) serves as the backend API for an interactive dashboard.
It loads an insurance dataset (CSV), processes the data, and prepares it for visualization.
"""


# importing modules
import pandas as pd


class insuranceAPI:
    """A class to load, process, and manage insurance data for visualization."""

    def load_insurance(self, filename):
        """

        :param filename(str)
        :return: None - Stores the dataset in the 'self.insurance' attribute.

        Loads insurance data from a CSV file into a pandas DataFrame
        """
        self.insurance = pd.read_csv(filename)


    def change_smoker(self):
        """
        Updates the 'smoker' column values in the dataset.

        - Replaces "yes" with "smoker".
        - Replaces "no" with "nonsmoker".

        :return: None
            Modifies the DataFrame in place
        """

        self.insurance["smoker"] = self.insurance["smoker"].replace({"yes": 'smoker', "no": 'nonsmoker'}).reset_index(drop=True)

    def get_data(self):
        """
        Retrieves the current state of the DataFrame.

        :return: pd.DataFrame
            Returns the processed insurance dataset.
        """
        return self.insurance

# defining the main method
def main():

    # creates an instance of the InsuranceAPI class
    insurance_api = insuranceAPI()

    # Load the dataset
    insurance_api.load_insurance("insurance.csv")

    # Transform the 'smoker' column
    insurance_api.change_smoker()

    # Check the updated DataFrame
    print(insurance_api.get_data())

if __name__ == '__main__':
    main()
