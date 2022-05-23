"""
CSE 163
Jangwon Yun, Victor Ahn, Yongjung Lee
Why Russia Should Stop War
"""
import pandas as pd

def main():
    eq = pd.read_csv('/Users/jangwonyun/Desktop/UkrainevsRussia/russia_losses_equipment.csv')
    print(eq)

if __name__ == '__main__':
    main()