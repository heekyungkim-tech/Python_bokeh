import pandas as pd

from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import row

def update_chart(attr, old, new):
    print(old)
    print(new)
    conAmnt = my_contrib.groupby([mySelect.value])['AMNT'].sum()
    
    # update x_axis of the chart
    my_bar.x_range,factors = list(conAmnt.index.values)
    
    # update columndatasource with new data
    my_cds.data = dict(c_type=conAmnt.index.values,
                       tot_amt=conAmnt.values)
    
    
# read the datafile into a dataframe
my_contrib = pd.read_excel('data/2017_Contributions.xlsx')

# needs these for hover tools and most othet bokeh chart functionality
from bokeh.models import HoverTool,ColumnDataSource,NumeralTickFormatter, Select

# Add Select Widget
mySelect = Select(title="summurize contributions by:",options=['OFFICECD','C_CODE','BOROUGHCD'], value='OFFICECD')

# create a groupby to analyze funds raised by contributor type
conAmnt = my_contrib.groupby([mySelect.value])['AMNT'].sum()

x_val = conAmnt.index.values
y_val = conAmnt.values

# Create a columndatasource object
my_cds = ColumnDataSource(data=dict(
    c_type = x_val,
    tot_amt = y_val
))

# Create Hovertool with tooltips
myHover = HoverTool(tooltips = [
    ("Amnt Raised:","@tot_amt{$0,0.00 a}") 
])

# Create a figure object with necessary parameter
my_bar = figure(x_range=x_val,
               width=600,height=400,
               x_axis_label = "Types of contributors", y_axis_label = "Funds raised in $",
               title = "Analyzing contributions by contributor type",

                tools = 'xpan,zoom_in,tap')

# Bar chart should use columnDataSource as its source for data
my_bar.vbar(x='c_type', top='tot_amt', width=-.5, color='red',source=my_cds,
            selection_color='blue',
            nonselection_color = 'green', nonselection_alpha=0.2)


my_bar.yaxis.formatter = NumeralTickFormatter(format='$0,0 a')

# Add the hoverTool to the plot figure
my_bar.add_tools(myHover)

# Capture Select on_change event
mySelect.on_change('value',update_chart)


# Show the bar charts and Select widget
curdoc().add_root(row(mySelect,my_bar))

# Add title to the server application
curdoc().title="My First BokehServer Chart"
