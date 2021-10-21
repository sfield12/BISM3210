# Import packages
from bokeh import *
from bokeh.plotting import figure, show
import pandas as pd
import seaborn as sns
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

# Check out available datasets
# print(sns.get_dataset_names())

# load data
Titanic = sns.load_dataset('titanic')

# exploratory analysis
print(Titanic.head())
print(Titanic.describe())

# age variable exploratory analysis

print(Titanic[["age"]].describe())

# creating age categories
age_cat = pd.cut(Titanic.age, bins=[0, 3, 17, 65, 99], labels=['Baby/Toddler', 'Child', 'Adult', 'Elderly'])
print(age_cat)
Titanic.insert(5, 'Age group', age_cat)
print(Titanic["Age group"])
print(Titanic.groupby(["Age group", "survived"])["survived"].count())

# sex variable exploratory analysis
# print(Titanic[["sex"]].describe())
# sex_survived = Titanic.groupby(["sex", "survived"])['survived'].count().reset_index(name='count')
# print(type(sex_survived))
# print(sex_survived)
# sex_survived_pct = (sex_survived / sex_survived.groupby(level=0).sum() * 100)
# print(type(sex_survived_pct))
# print(sex_survived_pct)

sur = Titanic.groupby(["sex", "survived"])["sex"].count().reset_index(name='count')
sur.columns = ['sex', 'survived', 'percent']
print(sur)
s_sur = sur.groupby(["sex", "survived"])\
    .agg({"percent": 'sum'})\
    .groupby(level=0).apply(lambda x: 100 * x / x.sum())\
    .sort_values(by=["sex", "survived", "percent"], ascending=[True, True, False])
print(s_sur)
print(type(s_sur))

#print(s_sur[s_sur["survived"] == 1])

# s_survd = Titanic.groupby(["sex", "survived"]).count().rename("count_survived")
# s_survd1 = s_survd.groupby(level=0).apply(lambda x: 100* x /float(x.sum())).to_frame().reset_index()
#
# print('hello')

# creating function for bar chart


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):

    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0, end=max(data[y_name]) * 1.5)

    hover_tool = HoverTool(tooltips=[
        ('Sex', '@sex'),
        ('Percentage survived', '@count_survived'),
    ])


    tools = []
    if hover_tool:
        tools = [hover_tool, ]

    #tools = ['hover']

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height,
                  min_border=0, toolbar_location="above", tools=tools,
                  outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.5,
                 fill_color="#0bcddb")
    plot.add_glyph(source, glyph)
    plot.tools.append(hover_tool)
    #plot.add_tools(HoverTool(tooltips=tooltips))

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Percentage survived"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Sex"
    plot.xaxis.major_label_orientation = 1
    return plot


def survivalRatePerSex():
    s_survd = Titanic.groupby(["sex", "survived"])["survived"].count().rename("count_survived")
    s_survd1 = s_survd.groupby(level='sex').apply(lambda x: 100 * x / float(x.sum())).to_frame().reset_index()
    print(s_survd1.head())
    s_survived = (s_survd1[s_survd1.survived==1])
    plot = create_bar_chart(s_survived, 'Survival rate per sex', "sex", "count_survived")
    return plot




# return plot

survivalRatePerSex()

# number of people in the family

num_rows1 = len(Titanic['survived'])

family_size = []

for i in range(num_rows1):
    family_size.append(Titanic["sibsp"][i] + Titanic["parch"][i] + 1)

# print(family_size)

Titanic.insert(6, 'fam_size', family_size)
# print(Titanic['fam_size'].count())
fam_survived = (Titanic.groupby(['fam_size', 'survived'])['survived'].count())
fam_survived_pct = (fam_survived / fam_survived.groupby(level=0).sum() * 100)
# print(fam_survived_pct)

# cabin location exploration

# print(Titanic["deck"].describe())

# multi choice drop down menu for cabin location

class_dict = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7
}
# print(class_dict)

drop_options = [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [1, 2, 3, 4, 5, 6, 7],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4],
    [1, 2, 3],
    [1, 2],
    [1],
    [2],
    [2, 3, 4, 5, 6, 7, 8],
    [2, 3, 4, 5, 6, 7],
    [2, 3, 4, 5, 6],
    [2, 3, 4, 5],
    [2, 3, 4],
    [2, 3],
    [3, 4, 5, 6, 7, 8],
    [3, 4, 5, 6, 7],
    [3, 4, 5, 6],
    [3, 4, 5],
    [3, 4],
    [3],
    [4, 5, 6, 7, 8],
    [4, 5, 6, 7],
    [4, 5, 6],
    [4, 5],
    [4],
    [5, 6, 7, 8],
    [5, 6, 7],
    [5, 6],
    [5],
    [6, 7, 8],
    [6, 7],
    [6],
    [7, 8],
    [7],
    [8]
]
