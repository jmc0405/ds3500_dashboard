import panel as pn
from dashboardhw import insuranceAPI
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

pn.extension()

# initialize the API
api = insuranceAPI()
api.load_insurance("insurance.csv")

#plot Widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1000)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=700)

# define interactive widgets

df_widget = pn.widgets.DataFrame(api.get_data(), height=width, width=height)
smoker_label = pn.pane.Markdown("**Smoker Status:**")
region_selector = pn.widgets.Select(name="Region", options=list(api.get_data()["region"].unique()), value="southeast")
smoker_selector = pn.widgets.ToggleGroup(name="Smoker", options=["yes", "no", "total"], behavior="radio")
age_slider = pn.widgets.IntRangeSlider(name="Age Range", start=api.get_data()["age"].min(), end=api.get_data()["age"].max(), value=(20, 50))

# Update scatter plot function
def update_scatter_plot(region, smoker, age_range, width, height):
    """
    Updates the scatter plot based of desired filtering

    :param region: value for certain region we want to look visualize
    :param smoker: status if we want to look at smoker or nonsmoker or both
    :param age_range: list which has starting min value and ending max value
    :param width: value for how wide the plot is
    :param height: value for how tall plot is
    :return: updated scatter plot
    """
    # filter data based on selected inputs
    df = api.get_data()

    if smoker == "total":
        filtered_df = df[
            (df["region"] == region) &
            (df["age"].between(age_range[0], age_range[1]))
        ].copy()
    else:
        filtered_df = df[
            (df["region"] == region) &
            (df["smoker"] == smoker) &
            (df["age"].between(age_range[0], age_range[1]))
        ].copy()

    # ensure smoker is a categorical variable
    filtered_df["smoker"] = filtered_df["smoker"].astype("category")

    # assign colors explicitly
    color_mapping = {"yes": "red", "no": "blue"}
    filtered_df["color"] = filtered_df["smoker"].map(color_mapping)

    # create scatter plot with hover information
    scatter_plot = filtered_df.hvplot.scatter(
        x="bmi",
        y="charges",
        color="color",  # assign explicit colors
        size=100,
        alpha=0.6,
        width = width,
        height = height,
        responsive=True,
        title="BMI vs. Insurance Charges (Colored by Smoker Status)",
        legend="top_right",
        hover_cols=["smoker"]  # show smoker status on hover
    )

    return scatter_plot

# update bar plot function
def update_bar_plot(smoker, age_range, width, height):
    """
    Update the bar chart to show average charges for all regions,
    filtered by smoker status and age range

    :param smoker: status value for either smoker or nonsmoker or both
    :param age_range: age range we want to look at
    :param width: value for how wide we want it
    :param height: value for how tall we want plot
    :return: updated bar plot with desired values and filtering
    """
    # fetch data
    df = api.get_data()

    # apply filtering based on smoker status
    if smoker == "total":
        filtered_df = df[df["age"].between(age_range[0], age_range[1])].copy()
    else:
        filtered_df = df[
            (df["smoker"] == smoker) &
            (df["age"].between(age_range[0], age_range[1]))
        ].copy()

    # group by region and calculate average charges
    bar_chart = filtered_df.groupby("region")["charges"].mean().reset_index()

    # create bar chart
    bar_chart_plot = bar_chart.hvplot.bar(
        x="region",
        y="charges",
        title="Average Charges by Region",
        xlabel="Region",
        ylabel="Average Charges",
        color="lightblue",  # Set color for clarity
        height = height,
        width = width,
        responsive=True
    )

    return bar_chart_plot

# update pie chart function
def update_pie_chart(smoker):
    """
       Update the pie chart to show the distribution of charges by region,
    filtered by smoker status and age range.

    :param smoker: status for either we want smoker or nonsmoker or both
    :return: updated pie chart
    """
    # fetch data
    df = api.get_data()

    # filters based of smoker status
    if smoker == "total":
        filtered_df = df[df["age"]].copy()
    else:
        filtered_df = df[
            (df["smoker"] == smoker)
        ].copy()

    # group by region and calculate total charges
    pie_data = filtered_df.groupby("region")["charges"].sum().reset_index()
    pie_data['angle'] = pie_data['charges'] / pie_data['charges'].sum() * 2 * pi
    pie_data['color'] = Category20c[len(pie_data)]

    # Create pie chart
    pie_chart = figure(
        height=280,
        title="Distribution of Charges by Region",
        toolbar_location=None,
        tools="hover",
        tooltips="@region: @charges{0,0.00}",  # Format charges as currency
        x_range=(-0.5, 1.0),
    )

    pie_chart.wedge(
        x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white",
        fill_color='color',
        legend_field='region',
        source=pie_data,
    )

    # customize the chart
    pie_chart.axis.axis_label = None
    pie_chart.axis.visible = False
    pie_chart.grid.grid_line_color = None

    return pie_chart

# Bind widgets to update functions
scatter_plot = pn.bind(update_scatter_plot, region_selector, smoker_selector, age_slider, width, height)
bar_chart = pn.bind(update_bar_plot, smoker_selector, age_slider, width, height)
pie_chart = pn.bind(update_pie_chart, smoker_selector)
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

plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),

    title="Plot", width=320, collapsed=True
)

pie_chart_card = pn.Card(
    pn.Column(pie_chart),
    title="Pie Chart", width=320, collapsed=False
)

# Create layout
layout = pn.template.FastListTemplate(
    title="Health Insurance Dashboard",
    sidebar=[search_card, plot_card,pie_chart_card],
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
