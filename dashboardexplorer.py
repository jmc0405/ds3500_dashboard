import panel as pn
from dashboardhw import insuranceAPI
from bokeh.plotting import figure
import hvplot.pandas
import holoviews as hv
pn.extension()

# Initialize the gad api
api = insuranceAPI()
api.load_insurance("insurance.csv")


pn.extension()

"""Defining interactive widgets"""

df_widget = pn.widgets.DataFrame(api.get_data(), height=650, width=1100)
smoker_label = pn.pane.Markdown("**Smoker Status:**")  # Add label for smoker toggle
region_selector = pn.widgets.Select(name="Region", options=list(api.get_data()["region"].unique()), value="southeast")
smoker_selector = pn.widgets.ToggleGroup(name="Smoker", options=["yes", "no"], behavior="radio")

# Slider for selecting an age range (by default it's from 20 to 50)
age_slider = pn.widgets.IntRangeSlider(name="Age Range", start=api.get_data()["age"].min(), end=api.get_data()["age"].max(), value=(20, 50))


def update_scatter_plot(region, smoker, age_range):
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
    df = api.get_data()  # Get the data once
    filtered_df = df[
        (df["region"] == region) &
        (df["smoker"] == smoker) &
        (df["age"].between(age_range[0], age_range[1]))
        ].copy()

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
    # Return both plots in a vertical layout
    return scatter_plot

def update_bar_plot(region, smoker, age_range):
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
    df = api.get_data()  # Get the data once
    #Bar Chart - Average Charges by Region
    bar_chart = api.get_data().groupby("region")["charges"].mean().reset_index()
    bar_chart_plot = bar_chart.hvplot.bar(
        x="region",
        y="charges",
        title="Average Charges by Region",
        xlabel="Region",
        ylabel="Average Charges",
        size=100

     ).opts(width=1100, height=650)
    return bar_chart_plot

scatter_plot = pn.bind(update_scatter_plot,region_selector, smoker_selector, age_slider)
bar_chart = pn.bind(update_bar_plot,region_selector, smoker_selector, age_slider)

search_card = pn.Card(
    pn.Column(
        smoker_label,
            smoker_selector,
        region_selector
    ),
    title="Search", width=320, collapsed=False
)


layout = pn.template.FastListTemplate(
    title="Health Insurance Dashboard",
    sidebar=[
       #df_card
      search_card
   ],
   theme_toggle=False,
   main=[
        pn.Tabs(
             # Replace None with callback binding
           #("Network", plot),  # Replace None with callback binding
            ("Scatter", scatter_plot),
            ("Bar Chart", bar_chart),
            ("DataFrame", df_widget),
           active=1  # Which tab is active by default?
       )

    ],
    header_background='#a93226'

).servable()

layout.show()
