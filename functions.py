"""
CSE 163
Jangwon Yun, Victor Ahn, Yongjung Lee
Why Russia Should Stop War

This file contains the functions that filter the data and could visualize the
graphs that is relevant to the Ukraine War. We try to compare the data
through different lens, and utilize the pandas, seaborn, matplotlib, and
ipywidgets. Due to the ipywidgets, we could get best visualization through
Jupyter Notebook.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as widgets


def filter_data_russ_uk(russ_eq, uk_eq):
    """
    This function takes in the data about russian equipment losses and
    ukraine equipment losses, filter the data to have total losses by
    equipment types, and returns the filtered data.
    """
    filtered_russ = russ_eq.groupby("equipment")["losses_total"].sum()
    f_russ = pd.DataFrame({'equipment': filtered_russ.index,
                           'losses_total': filtered_russ.values})
    filtered_uk = uk_eq.groupby("equipment")["losses_total"].sum()
    f_uk = pd.DataFrame({'equipment': filtered_uk.index,
                         'losses_total': filtered_uk.values})
    loss_data = pd.merge(f_russ, f_uk, on='equipment', how='outer')
    loss_data = loss_data.rename(columns={'equipment': 'Equipment',
                                          'losses_total_x': 'Russia',
                                          'losses_total_y': 'Ukraine'})
    loss_data = loss_data.fillna(0)
    return loss_data


def graph_russ_uk(loss_data):
    """
    This function takes in the filtered data from the function
    filter_data_russ_uk creates the list of equipment types, and insert them
    into the widget that could select the equipment, and creates
    the bar graph that could compare the losses between Russia and Ukraine.
    """
    eq_russ_list = list(loss_data['Equipment'].unique())
    widget_russ_uk = widgets.Dropdown(options=eq_russ_list,
                                      description='Equipment:',
                                      disabled=False)

    def create_bar_graph(eq):
        eq_data = loss_data[(loss_data['Equipment'] == eq)]
        eq_data.plot(x='Equipment', y=['Russia', 'Ukraine'], kind='bar',
                     figsize=(9, 9))
        plt.ylim(0, 1000)
        plt.title("Total Loss Equipment of Russia")
        plt.xlabel('Equipment Types')
        plt.ylabel('Total Loss')
    plot_uk_russ = widgets.interact(create_bar_graph, eq=widget_russ_uk)
    return plot_uk_russ


def line_plot_casualties(casualty):
    """
    This function takes in the data about the civilian casualties, filter
    the cumulative data to collect exact number of casualties per each
    month, and returns the merged data between killed and injured numbers.
    """
    killed_data = {'Month': ['February', 'March', 'April', 'May'],
                   'Killed': [casualty.loc['02/28/22']['Killed'],
                              casualty.loc['03/31/22']['Killed'],
                              casualty.loc['04/28/22']['Killed'],
                              casualty.loc['05/25/22']['Killed']]}
    injured_data = {'Month': ['February', 'March', 'April', 'May'],
                    'Injured': [casualty.loc['02/28/22']['Injured'],
                                casualty.loc['03/31/22']['Injured'],
                                casualty.loc['04/28/22']['Injured'],
                                casualty.loc['05/25/22']['Injured']]}
    filtered_killed = pd.DataFrame(killed_data)
    filtered_injured = pd.DataFrame(injured_data)
    diff_killed = filtered_killed['Killed'].diff()
    diff_injured = filtered_injured['Injured'].diff()
    diff_killed = diff_killed.set_axis(['February', 'March', 'April', 'May'])
    diff_killed['February'] = casualty.loc['02/28/22']['Killed']
    diff_injured = diff_injured.set_axis(['February', 'March', 'April', 'May'])
    diff_injured['February'] = casualty.loc['02/28/22']['Injured']
    comb_killed_injured = pd.merge(diff_killed, diff_injured,
                                   right_index=True, left_index=True)
    return comb_killed_injured


def graph_casualties(comb_killed_injured):
    """
    This function takes in the filtered data from line_plot_casualties,
    creates the list by the columns of the data, killed and injured,
    create the radiobutton widget, and create the line graph that visualizes
    the casualties by types(killed and injured).
    """
    casualties_list = list(comb_killed_injured.columns)
    widget_casualties = widgets.RadioButtons(options=casualties_list,
                                             description='Types',
                                             disabled=False)

    def create_line_graph(cas):
        cas_data = comb_killed_injured[cas]
        sns.lineplot(data=cas_data)
        plt.title("Casualties of Civilians From The Ukranian War")
        plt.xlabel('Month')
        plt.ylabel('Total Numbers')
    plot_casualties = widgets.interact(create_line_graph,
                                       cas=widget_casualties)
    return plot_casualties


def financial_loss_russia(fi_russ):
    """
    This function takes in the data about financial losses of top 10
    richest people in Russia, filter the data to contain the names and
    the year over year change in Billion USD, and plot the bar graph to
    show how much financial they have lost in this year.
    """
    filtered_fi = fi_russ[['Name', 'YoY change in billion USD']]
    sns.barplot(x="YoY change in billion USD", y="Name", data=filtered_fi,
                color="red")
    plt.title("Financial Losses of Richest Top 10 Russian")
    plt.xlabel('Year over Year change in Billion USD')
    plt.ylabel('Year over Year change in Billion USD')
    plt.savefig('Financial.png')
