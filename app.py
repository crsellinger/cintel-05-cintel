################################
# Caleb Sellinger
# 44630 Cont Intel
# Dr. Case
# 11-4-2024
################################

import plotly.express as px
from shiny.express import input, ui
from shiny import render, reactive
from shinywidgets import render_plotly
import palmerpenguins
import seaborn
import pandas

#Penguins data set
penguins_df = palmerpenguins.load_penguins()

#Page options, specifically title
ui.page_opts(title="Caleb Sellinger - Module 2: Palmer Penguins Data", fillable=True)

#Reactive Calculations
@reactive.calc
#filter species
def filtered_data():
    selected_species = input.selected_species_list()
    
    if selected_species:
        filtered = penguins_df[penguins_df["species"].isin(selected_species)]
        
    return filtered

@reactive.calc
#fitler columns
def filtered_data_2():
    selected_columns = input.selected_columns()

    if selected_columns:
        filtered = pandas.DataFrame(penguins_df).filter(items=list(selected_columns),axis=1)

    else:
        return penguins_df

    return filtered
    
#column component
with ui.layout_columns():
    #card componenet for Data Table
    with ui.card(full_screen=True):
        ui.h2("Penguins Data Table")
        #Data Table
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data_2())

    #Card component for Data Grid
    with ui.card(full_screen=True):
        ui.h2("Penguin Data Grid")
        #Data Grid
        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())

#column component
with ui.layout_columns():

    @render.plot(alt="Seaborn histogram plot")
    def plot3():
        return seaborn.histplot(data=penguins_df,x="species",y="body_mass_g",bins=input.seaborn_bin_count())
    
    @render_plotly
    def plot4():
        return px.histogram(data_frame=penguins_df,x="flipper_length_mm",y="body_mass_g",nbins=input.selected_number_of_bins())

#Card component for scatter plot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    #Scatter plot for penguins data
    @render_plotly
    def plot5():
        return px.scatter(filtered_data(),x="flipper_length_mm",y="body_mass_g",color="species",title="Body Mass vs Flipper Length",labels={"body_mass_g":"Body Mass (g)","f1lipper_length_mm":"Flipper Length (mm)","species":"Species"})
    
#Side bar component
with ui.sidebar(open="open",bg="#99ccff",fillable=True):
    ui.input_dark_mode(mode="light")
    ui.h2("Sidebar")
    ui.input_checkbox_group("selected_species_list","Select Species (Plot 1 & 2)",choices=["Adelie","Gentoo","Chinstrap"],selected=["Adelie","Gentoo","Chinstrap"],inline=False)
    ui.input_slider("seaborn_bin_count","Seaborn Slider (Plot 3)",0,150,50)
    ui.input_numeric(id="selected_number_of_bins",label="Select Number of Bins (Plot4)",value=10)
    ui.input_selectize(id="selected_columns",label="Select Column to Display",choices=["island","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g","sex","year"],selected=["species","island","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g","sex","year"],multiple=True)
    ui.hr()
    ui.a("Link HERE",href="https://github.com/crsellinger/cintel-02-data",target="_blank")
