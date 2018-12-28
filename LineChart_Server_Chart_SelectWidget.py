import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Select
from bokeh.io import curdoc
from bokeh.layouts import row

# Defining update function
def update_plot(attr, old, new):
    # update the dataframe slice by the new recipinet name selected
    recipSelect = contrib[contrib['RECIPNAME'] == mySelect.value]
    # re-run the code for getting funds raised for that recipient
    recipAmnt = recipSelect.groupby(['DATE'])['AMNT'].sum()
    # update the columndatasource with this new data
    recipAmntCDS.data = dict(x_val = recipAmnt.index.values,
                             y_val = recipAmnt.values)
    
      
# REading in the initial dataset    
contrib = pd.read_excel('data/2017_Contributions.xlsx')

# Create a list with all the names of the recipients
recipList = contrib.RECIPNAME.unique()

# Add select widget
mySelect = Select(title='Select Recipient', 
                  options=list(recipList),
                  value='Abreu, Randy')


# Slicing the dataframe to select only those records where
# recipient name matches. In the code below recipList[0] would be
# replaced by the value user selects in the SELECT widget as mySelect.value
recipSelect = contrib[contrib['RECIPNAME'] == mySelect.value]

# Now using groupby statement retrieve the funds raised over time on 
# this sliced dataframe
recipAmnt = recipSelect.groupby(['DATE'])['AMNT'].sum()
recipAmntCDS = ColumnDataSource(data=dict(
                x_val = recipAmnt.index.values,
                y_val = recipAmnt.values
))

myLine = figure(x_axis_type='datetime',
               width=600, height=400)

myLine.line(x='x_val', y='y_val', source=recipAmntCDS, line_color='blue')
myLine.yaxis.formatter = NumeralTickFormatter(format='0,0')

#Capturing on_change event
mySelect.on_change('value', update_plot)

curdoc().add_root(row(mySelect,myLine))