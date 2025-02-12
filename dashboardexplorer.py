import panel as pn
from dashboardhw import insuranceAPI
import hvplot.pandas
import holoviews as hv

pn.extension()

# Initialize the API
api = insuranceAPI()
api.load_insurance("insurance.csv")

# Define interactive widgets
df_widget = pn.widgets.DataFrame(api.get_data(), height=650, width=1100)
smoker_label = pn.pane.Markdown("**Smoker Status:**")
region_selector = pn.widgets.Select(name="Region", options=list(api.get_data()["region"].unique()), value="southeast")
smoker_selector = pn.widgets.ToggleGroup(name="Smoker", options=["yes", "no"], behavior="radio")
age_slider = pn.widgets.IntRangeSlider(name="Age Range", start=api.get_data()["age"].min(), end=api.get_data()["age"].max(), value=(20, 50))

# Debugging: Print widget values
def print_widget_values(region, smoker, age_range):
    print(f"Region: {region}, Smoker: {smoker}, Age Range: {age_range}")

# Update scatter plot function
def update_scatter_plot(region, smoker, age_range):
    # Filter data based on selected inputs
    df = api.get_data()
    filtered_df = df[
        (df["region"] == region) &
        (df["smoker"] == smoker) &
        (df["age"].between(age_range[0], age_range[1]))
    ].copy()

    # Assign colors to smoker values
    color_mapping = {"yes": "red", "no": "blue"}
    filtered_df["color"] = filtered_df["smoker"].map(color_mapping)

    # Create scatter plot
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
    return scatter_plot

# Update bar plot function
def update_bar_plot(smoker, age_range):
    """
    Update the bar chart to show average charges for all regions, filtered by smoker status and age range.
    :param smoker: str
        The smoker status ("yes" or "no").
    :param age_range: int tuple
        The selected age range.
    :return: Bar chart showing average charges by region.
    """
    # Filter data based on smoker status and age range
    df = api.get_data()
    filtered_df = df[
        (df["smoker"] == smoker) &
        (df["age"].between(age_range[0], age_range[1]))
    ]

    # Group by region and calculate average charges
    bar_chart = filtered_df.groupby("region")["charges"].mean().reset_index()

    # Create bar chart
    bar_chart_plot = bar_chart.hvplot.bar(
        x="region",
        y="charges",
        title="Average Charges by Region",
        xlabel="Region",
        ylabel="Average Charges",
        size=100
    ).opts(width=1100, height=650)
    return bar_chart_plot

# Bind widgets to update functions
scatter_plot = pn.bind(update_scatter_plot, region_selector, smoker_selector, age_slider)
bar_chart = pn.bind(update_bar_plot,  smoker_selector, age_slider)

# Debugging: Bind widget values to a print function
pn.bind(print_widget_values, region_selector, smoker_selector, age_slider)

# Create search card
search_card = pn.Card(
    pn.Column(
        smoker_label,
        smoker_selector,
        region_selector,
        age_slider
    ),
    title="Search", width=320, collapsed=False
)



# Create layout
layout = pn.template.FastListTemplate(
    title="Health Insurance Dashboard",
    sidebar=[search_card],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Scatter", scatter_plot),
            ("Bar Chart", bar_chart),
            ("DataFrame", df_widget),
            active=1
        )
    ],
    header_background='#a93226'
).servable()

# Show the layout
layout.show()
