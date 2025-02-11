import panel as pn
from dashboardhw import insuranceAPI
from bokeh.plotting import figure
pn.extension()

# Initialize the gad api
api = insuranceAPI()
api.load_insurance("insurance.csv")


pn.extension()



df_widget = pn.widgets.DataFrame(api.get_data(), height=300, width=750)

#df_card = pn.Card(pn.Column(pn.widgets.DataFrame(api.get_data()), height=300, width=500),
#    title="Dataframe", width=, collapsed=False
#)

layout = pn.template.FastListTemplate(
    title="Health Insurance Dashboard",
   # sidebar=[
       # df_card
      #  plot_card,
   # ],
   theme_toggle=False,
   main=[
        pn.Tabs(
           ("Associations", df_widget),  # Replace None with callback binding
           #("Network", plot),  # Replace None with callback binding
           active=1  # Which tab is active by default?
       )

    ],
    header_background='#a93226'

).servable()

layout.show()
