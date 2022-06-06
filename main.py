"""
CSE 163
Jangwon Yun, Victor Ahn, Yongjung Lee
Why Russia Should Stop

This file runs the functions that are structured in the file functions.py,
and create various visualizations that are related to the Ukraine War.
Through various visualiztions, we aim to give strong indication about why
Russia should stop this war. The data about equipment losses is collected
from Kaggles, and the data about civillian casualties and financial losses
are collected from Statista.
"""
import pandas as pd
import functions as fo


def main():
    russ_eq = pd.read_csv("russian_weapon_losses.csv")
    uk_eq = pd.read_csv("ukraine_weapon_losses.csv")
    casualty = pd.read_csv("number_of_civilian_casualties.csv",
                           index_col='Date', parse_dates=True)
    fi_russ = pd.read_csv("financial_losses.csv")
    bar_graph_detail = fo.filter_data_russ_uk(russ_eq, uk_eq)
    fo.graph_russ_uk(bar_graph_detail)
    line_graph_detail = fo.line_plot_casualties(casualty)
    fo.graph_casualties(line_graph_detail)
    fo.financial_loss_russia(fi_russ)
