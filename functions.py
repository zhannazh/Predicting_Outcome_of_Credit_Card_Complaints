
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.    
    Source: https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.2f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.


def get_variable_categories(df, var):
    return df[var].value_counts().index

def get_percent_of_obs_in_category(df,var,category):
    return df[df[var]==category][var].count()/df.shape[0]

def categories_with_less_than_X_percent(df, var, fraction):
    categories_with_less_than_X_percent = []
    for category in get_variable_categories(df,var):
        if get_percent_of_obs_in_category(df,var,category) < fraction:
            categories_with_less_than_X_percent.append(category)
    return categories_with_less_than_X_percent

def group_categories_with_less_than_X_percent_into_Other(df, var, fraction):
    df['{}_recoded'.format(var)]=df[var]
    
    for category in categories_with_less_than_X_percent(df, var, fraction):
        df.loc[df[var] == category, '{}_recoded'.format(var)] = '{}-Other groupped'.format(var)
    return df

def fraction_of_outcomes_with_monetary_relief(df,var):
    df = df.groupby([var]).Y.mean()
    df = pd.DataFrame(df).sort_values(by='Y',ascending=False).reset_index()
    return df.rename(columns={'Y':'mean(Y)'})


def bar_chart_Y_by_categories_of_variable(df,var, title):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.title(title, size=18)
    plt.bar(df.index, df['mean(Y)'], color = 'orange')
    plt.xticks(df.index, df[var], rotation=90)
    plt.yticks(np.arange(10*(df['mean(Y)'].max()+.1))/10)
    plt.ylabel("Fraction with Monetary Relief", size=12)
    add_value_labels(ax)
    plt.show()    


def create_dummies(df, var, prefix, excluded_category):
    f = pd.get_dummies(df[var], prefix=prefix)
    f = f.drop([excluded_category], axis=1)
    df = pd.concat([df, f], axis=1)
    return df    


def process_zipcodes(f):

    # Remove empty space from variable ZIP code
    f["ZIP code"] = f["ZIP code"].str.strip()

    print("Length of the zip code in the dataset")
    print(f["ZIP code"].str.len().value_counts())
    print()
    
    print("Number of non-alphanumeric characters: ")
    print(f[f["ZIP code"].str.isalnum()==False].shape[0])
    print()

    print('Alpha characters in the zip code:')
    print(f["ZIP code"].str.extract('([A-Z])')[0].value_counts())
    print()

    print('Number of null values: ', f['ZIP code'].isna().sum())
    
    return f


def feature_importance(clf, df):

    """ This function produces a bar chart of feature importance and gives a list of 
    ranked features / variables """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 1
    plt.title('Feature Importance', size=18)
    ax.bar(np.arange(len(df.drop('Y',axis=1).columns)), clf.feature_importances_, width, 
           color='r', edgecolor='k')
    ax.set_xticks(np.arange(len(clf.feature_importances_)))
    ax.set_xticklabels(df.drop('Y',axis=1).columns.values, rotation = 90, size=15)
    ax.set_ylabel("Feature's Information Gain", size=14)
    plt.show()

    d = {}
    for i in range(len(df.drop('Y',axis=1).columns)):
        d[df.drop('Y',axis=1).columns[i]]=format(clf.feature_importances_[i], '.3f')
    print('Features by Importance (Information gain or decrease in entropy)')

    return sorted(d.items(), key=lambda x: x[1], reverse=True)
    
