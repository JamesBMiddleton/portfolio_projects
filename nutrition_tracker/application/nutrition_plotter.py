import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                as FigureCanvas)

df = pd.read_csv('nutrition_data.csv', index_col=0)

rdi_df = pd.DataFrame(
    columns=['Male', 'Female', 'Colour'],
    index=df.columns[1:-2],
    data=[[2500, 2000, '#C26862'],
         [3700, 2700, '#589A5D'],
         [400, 400, '#C26862'],
         [16, 16, '#C26862'],
         [130, 130, '#589A5D'],
         [38, 25, '#589A5D'],
         [np.nan, np.nan, 'white'],
         [30, 30, '#C26862'],
         [70, 70, '#C26862'],
         [np.nan, np.nan, 'white'],
         [np.nan, np.nan, 'white'],
         [20, 20, '#C26862'],
         [5, 5, '#C26862'],
         [300, 300, '#C26862'],
         # Protein and all amino acids are per kg bodyweight.
         [0.8, 0.8, '#589A5D'], 
         [0.010, 10, '#589A5D'],
         [0.020, 0.020, '#589A5D'],
         [0.039, 0.039, '#589A5D'],
         [0.030, 0.030, '#589A5D'],
         [0.015, 0.015, '#589A5D'],
         [0.025, 0.025, '#589A5D'],
         [0.015, 0.015, '#589A5D'],
         [0.004, 0.004, '#589A5D'],
         [0.026, 0.026, '#589A5D'],
         #
         [1.2, 1.1, '#589A5D'],
         [1.3, 1.1, '#589A5D'],
         [16, 14, '#589A5D'],
         [5, 5, '#589A5D'],
         [1.3, 1.3, '#589A5D'],
         [400, 400, '#589A5D'],
         [2.4, 2.4, '#589A5D'],
         [550, 425, '#589A5D'],
         [3000, 2333, '#589A5D'],
         [90, 75, '#589A5D'],
         [800, 800, '#589A5D'],
         [15, 15, '#589A5D'],
         [120, 90, '#589A5D'],
         [1000, 1000, '#589A5D'],
         [0.7, 0.7, '#589A5D'],
         [150, 150, '#589A5D'],
         [8, 18, '#589A5D'],
         [420, 320, '#589A5D'],
         [2.3, 1.8, '#589A5D'],
         [700, 700, '#589A5D'],
         [3400, 2600, '#589A5D'],
         [55, 55, '#589A5D'],
         [1500, 1500, '#C26862'],
         [11, 8, '#589A5D']])

def create_plot_vars(food_df, food_id, grams, rdi_df, 
                     advanced_view, sex, weight):
    """Creates all the datasets required create a nutrition plot, including
    RDI percentages, labels etc."""

    # Selecting a food using food_id, unless the input is a Series containing
    # the sum of multiple foods.
    if type(food_df) != pd.DataFrame:
        food_series = food_df
        food_name = 'Daily nutrition targets'
    else:
        food_series = food_df.iloc[food_id, 1:-2].astype(float).copy(deep=True)
        food_series = (food_series / 100) * grams
        food_name = food_df.iloc[food_id, -2]
    
    # Selecting male or female RDI series and applying weight based variations
    # in protein RDI.
    rdi_value_series = rdi_df.loc[:, sex].copy(deep=True)
    rdi_value_series.iloc[14:24] = rdi_value_series.iloc[14:24] * weight
    rdi_colour_series = rdi_df.loc[:, 'Colour'].copy(deep=True)   
    
    # Creating a Series for the food's percentage of RDI.
    rdi_percent_bar = (food_series / rdi_value_series) * 100
    rdi_percent_label = rdi_percent_bar.round(2).astype(str) + '%'
    
    # Limiting the bar size to 100% RDI.
    rdi_percent_bar = rdi_percent_bar.apply(lambda x: 100. if x > 100 else x)
    
    # Formatting the bar when no data or RDI target is available.
    for row in range(len(rdi_percent_bar)):
        if np.isnan(food_series[row]) == True:
            rdi_percent_bar[row] = 100
            rdi_percent_label[row] = 'No data'
            rdi_colour_series[row] = '#efebe7'
        elif np.isnan(rdi_value_series[row]) == True:
            rdi_percent_bar[row] = 100
            rdi_percent_label[row] = 'No target'
            rdi_colour_series[row] = '#efebe7'
    
    return (food_series, rdi_value_series, rdi_colour_series, 
            rdi_percent_bar, rdi_percent_label, food_name)

def create_plot(ax, food_series, rdi_value_series, rdi_colour_series,
                rdi_percent_bar, rdi_percent_label):
    """Takes an axis and plot variables as input, produces a horizontal bar
    plot on the input axis."""
    
    bars = ax.barh(range(len(food_series)),
                   rdi_percent_bar,
                   color=rdi_colour_series)

    # Iterates through each bar's dimensions to determine an appropriate
    # location for the percentage label. 
    for bar in range(len(bars)):

        width = bars[bar].get_width()
        width = int(width)

        if width < 40:
            xloc = 6
            align = 'left'
        else:
            xloc = 0
            align = 'center'
            width = width/2

        yloc = bars[bar].get_y() + bars[bar].get_height() / 2

        ax.annotate(
            rdi_percent_label[bar], xy=(width, yloc), xytext=(xloc, 0),
            textcoords="offset points",
            horizontalalignment=align, verticalalignment='center',
            weight='bold', clip_on=True, size=13)

    ax.set_yticks(range(len(food_series)))
    y_ticklabels = [
        '{0} - {1} {2}'.format(name.split('(')[0].strip(')'),
                               round(value,2), name.split('(')[1].strip(')')) 
        for name, value in zip(food_series.index, food_series)
        ]
    ax.set_yticklabels(y_ticklabels, size=13)
    ax.invert_yaxis()
    ax.set_xlim(0,100)
    ax.set_ylim((len(food_series) -0.4), -0.6)
    ax.get_xaxis().set_visible(False)
    ax.set_facecolor('#efebe7')

def regex_search(food_input, df):
    """Uses a regex expression to create a dataset of foods with matching 
    descriptions, ordered by the availabilty of nutritional values."""
    
    food_regexed = food_input.split(' ')
    for index in range(len(food_regexed)):
        food_regexed[index] = '(?=.*' + food_regexed[index] + '.*)'
    food_regexed = "".join(food_regexed)

    # Calculates the percentage of nutrients available for each food and uses
    # that percentage to orders the results.
    result = df[
        df.Description.str.contains(food_regexed, regex=True) == True
        ].copy(deep=True)
    result = result.sort_values(by='Completeness (%)', ascending=False)
    return result.iloc[:, -2:]


class NutritionDiary:
    """A diary instance starts as an array of 0's, users can then add foods to
    their diary instance to track their daily intake of each nutrient."""
    
    def __init__(self):
        self.diary = pd.Series(index=df.iloc[1, 1:-2].index, data=np.zeros(48))

    # Returns the sum of the nutrition diary and a specified food.
    def add_food(self, food_df, food_id, grams):
        self.diary += ((food_df.iloc[food_id, 1:-2].fillna(0) / 100) * grams)


class Canvas(FigureCanvas):
    """Bridges Matplotlib and PyQt, allowing plots to be displayed within a 
    PyQt application."""
    
    def __init__(self, parent, *args, **kwargs):
        fig, ((self.ax1, self.ax2),
              (self.ax3, self.ax4),
              (self.ax5, self.ax6)) = plt.subplots(
                  3, 2,
                  gridspec_kw={'width_ratios': [1, 1],
                               'height_ratios': [1, 2, 3]},
                  dpi=55,
                  figsize=(15,19.8))
        
        fig.patch.set_facecolor('#efebe7')
        super().__init__(fig)
        self.setParent(parent)
                
        (food_series, rdi_value_series, rdi_colour_series, rdi_percent_bar,
         rdi_percent_label, food_name) = create_plot_vars(*args, **kwargs)
               
        self.ax1.set_title('General', size=14)
        create_plot(self.ax1,
                    food_series[0:4],
                    rdi_value_series[0:4],
                    rdi_colour_series[0:4],
                    rdi_percent_bar[0:4],
                    rdi_percent_label[0:4])
        
        self.ax2.set_title('Carbohydrates', size=14)
        create_plot(self.ax2,
                    food_series[4:8],
                    rdi_value_series[4:8],
                    rdi_colour_series[4:8],
                    rdi_percent_bar[4:8],
                    rdi_percent_label[4:8])
        
        self.ax3.set_title('Fats', size=14)
        create_plot(self.ax3,
                    food_series[8:14],
                    rdi_value_series[8:14],
                    rdi_colour_series[8:14],
                    rdi_percent_bar[8:14],
                    rdi_percent_label[8:14])
        
        self.ax4.set_title('Proteins', size=14)
        create_plot(self.ax4,
                    food_series[14:23],
                    rdi_value_series[14:23],
                    rdi_colour_series[14:23],
                    rdi_percent_bar[14:23],
                    rdi_percent_label[14:23])
        
        self.ax5.set_title('Vitamins', size=14)
        create_plot(self.ax5,
                    food_series[24:37],
                    rdi_value_series[24:37],
                    rdi_colour_series[24:37],
                    rdi_percent_bar[24:37],
                    rdi_percent_label[24:37])
        
        self.ax6.set_title('Minerals', size=14)
        create_plot(self.ax6,
                    food_series[37:],
                    rdi_value_series[37:],
                    rdi_colour_series[37:],
                    rdi_percent_bar[37:],
                    rdi_percent_label[37:])
        
        plt.suptitle(food_name.capitalize(), size=18)        
        fig.subplots_adjust(left = 0.2,
                            right = 0.995,
                            top=0.95,
                            wspace=0.5,
                            hspace=0.07)

        
		

