"""
Author: Shrey Sahni
Date: February 11th, 2025

Description:
This script sets up an interactive health insurance dashboard using Panel, hvPlot, and Holoviews.
It allows users to filter data based on region, smoker status, and age range.
The dashboard visualizes BMI vs. Charges in a scatter plot and shows average charges by region in a bar chart.
"""


# importing modules and libraries
import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv

# Load dataset
df = pd.read_csv("insurance.csv")

"""Defining interactive widgets"""
smoker_label = pn.pane.Markdown("**Smoker Status:**")  # Add label for smoker toggle
region_selector = pn.widgets.Select(name="Region", options=list(df["region"].unique()), value="southeast")
smoker_selector = pn.widgets.ToggleGroup(name="Smoker", options=["yes", "no"], behavior="radio")

# Slider for selecting an age range (by default it's from 20 to 50)
age_slider = pn.widgets.IntRangeSlider(name="Age Range", start=df["age"].min(), end=df["age"].max(), value=(20, 50))

# Define filtering and visualization functions
@pn.depends(region_selector, smoker_selector, age_slider)
def update_plot(region, smoker, age_range):
    """

    :param region: str
        The selected region from the dropdown.
    :param smoker: str
        The smoker status ("yes" or "no").
    :param age_range: int tuple
        The selected age range
    :return:Panel layout containing scatter plot and bar chart.
    """
    # Filter data based on selected inputs
    filtered_df = df[(df["region"] == region) &
                     (df["smoker"] == smoker) &
                     (df["age"].between(age_range[0], age_range[1]))].copy()

    # Assigning colors to smoker values for the visualization
    color_mapping = {"yes": "red", "no": "blue"}
    filtered_df["color"] = filtered_df["smoker"].map(color_mapping)

    # Scatter Plot (BMI vs. Charges), color-coded based on smoker status
    scatter_plot = filtered_df.hvplot.scatter(
        x="bmi",
        y="charges",
        color="color",
        size=100,
        alpha=0.6,
        responsive=True,
        title="BMI vs. Charges (Colored by Smoker Status)",
        legend="top_right"
    )

    # Bar Chart - Average Charges by Region
    bar_chart = df.groupby("region")["charges"].mean().reset_index()
    bar_chart_plot = bar_chart.hvplot.bar(
        x="region",
        y="charges",
        title="Average Charges by Region",
        xlabel="Region",
        ylabel="Average Charges"
    )
    # Return both plots in a vertical layout
    return pn.Column(scatter_plot, bar_chart_plot)

# Create a layout with widgets on the left and visualization on the right
dashboard = pn.Row(
    pn.Column(region_selector, smoker_label, smoker_selector, age_slider),  # Removed extra label
    update_plot
)

# Serve the dashboard using panel
pn.serve(dashboard)

# import panel as pn
# from dashboardapi import insuranceAPI
# from bokeh.plotting import figure
# pn.extension()
#
# # Initialize the gad api
# api = insuranceAPI()
# api.load_insurance("insurance.csv")
#
#
# pn.extension()
#
# df_widget = pn.widgets.DataFrame(api.get_data(), height=300, width=750)
#
# #df_card = pn.Card(pn.Column(pn.widgets.DataFrame(api.get_data()), height=300, width=500),
# #    title="Dataframe", width=, collapsed=False
# #)
#
# layout = pn.template.FastListTemplate(
#     title="Health Insurance Dashboard",
#    # sidebar=[
#        # df_card
#       #  plot_card,
#    # ],
#    theme_toggle=False,
#    main=[
#         pn.Tabs(
#            ("Associations", df_widget),  # Replace None with callback binding
#            #("Network", plot),  # Replace None with callback binding
#            active=1  # Which tab is active by default?
#        )
#
#     ],
#     header_background='#a93226'
#
# ).servable()
#
# layout.show()
