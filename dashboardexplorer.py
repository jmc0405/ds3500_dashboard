import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv

# Load dataset
df = pd.read_csv("insurance.csv")

# Define interactive widgets with improvements
smoker_label = pn.pane.Markdown("**Smoker Status:**")  # Add label for smoker toggle
region_selector = pn.widgets.Select(name="Region", options=list(df["region"].unique()), value="southeast")
smoker_selector = pn.widgets.ToggleGroup(name="Smoker", options=["yes", "no"], behavior="radio")

# Keep built-in slider label only
age_slider = pn.widgets.IntRangeSlider(name="Age Range", start=df["age"].min(), end=df["age"].max(), value=(20, 50))

# Define filtering function
@pn.depends(region_selector, smoker_selector, age_slider)
def update_plot(region, smoker, age_range):
    filtered_df = df[(df["region"] == region) &
                     (df["smoker"] == smoker) &
                     (df["age"].between(age_range[0], age_range[1]))].copy()

    # Map smoker values to colors
    color_mapping = {"yes": "red", "no": "blue"}
    filtered_df["color"] = filtered_df["smoker"].map(color_mapping)

    # Scatter Plot (BMI vs. Charges) with correct color mapping
    scatter_plot = filtered_df.hvplot.scatter(
        x="bmi",
        y="charges",
        color="color",  # Now using the mapped color column
        size=100,
        alpha=0.6,
        responsive=True,
        title="BMI vs. Charges (Colored by Smoker Status)",
        legend="top_right"
    )

    # Bar Chart (Average Charges by Region)
    bar_chart = df.groupby("region")["charges"].mean().reset_index()
    bar_chart_plot = bar_chart.hvplot.bar(
        x="region",
        y="charges",
        title="Average Charges by Region",
        xlabel="Region",
        ylabel="Average Charges"
    )

    return pn.Column(scatter_plot, bar_chart_plot)  # Return both plots properly

# Layout dashboard correctly with label
dashboard = pn.Row(
    pn.Column(region_selector, smoker_label, smoker_selector, age_slider),  # Removed extra label
    update_plot  # Function reference, ensures updates dynamically
)

# Serve the panel
pn.serve(dashboard)

import panel as pn
from dashboardapi import insuranceAPI
from bokeh.plotting import figure
pn.extension()

# Initialize the gad api
api = insuranceAPI()
api.load_insurance("insurance.csv")


pn.extension()




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
