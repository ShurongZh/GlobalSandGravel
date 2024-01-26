
'''
Author: Shurong Zhaung
Date: 2023.5.9
Object: Sand and gravel MFA
Data:   Cement stock, building life time
'''


# 0 import
from dynamic_stock_model import DynamicStockModel   # import model
import numpy as np  # calculation package
import xlrd    # for reading excel
import pandas as pd   # for export data

# 1. Load and check data1
StockExcel = xlrd.open_workbook('Railway_GravelStock.xlsx')
Stock_DataSheet = StockExcel.sheet_by_name('Sheet1')
StockLTExcel = xlrd.open_workbook('Railway_GravelStock_LT.xlsx')
StockLT_DataSheet = StockLTExcel.sheet_by_name('Sheet1')
outflow_data = []
DynamicStock_data = []
inflow_data = []

Years = []   # year from 1970 to 2019
for m in range(1,51):  # read year
    Years.append(int(Stock_DataSheet.cell_value(m,0)))

for col in range(1,185):    #184 countries
    Stock_1 = []
    LifeTime = []
    for r in range(1,51):
        Stock_1.append(float(Stock_DataSheet.cell_value(r,col)))    # read stock
    for r in range(1,51):
        LifeTime.append(float(StockLT_DataSheet.cell_value(r, col)))

    # 2. Import Model
    Stock_DSM = DynamicStockModel(t = Years, s = Stock_1,
                                             lt = {'Type':'Normal', 'Mean': np.array(LifeTime),
                                                   'StdDev': 0.3*np.array(LifeTime) })     # Cement: 0.2; sublayer: 0.3; #bitumen: 0.15; railway: 0.3

    CheckStr, ExitFlag = Stock_DSM.dimension_check()
    # print(CheckStr)

    s_c, o_c, i, ExitFlag = Stock_DSM.compute_stock_driven_model()
    # S_C: Stock by cohort
    # O_C: Outflow by cohort
    # I: Inflow

    O, ExitFlag = Stock_DSM.compute_outflow_total()  #total outflow
    DS, ExitFlag = Stock_DSM.compute_stock_change()  #stcok change
    Bal, ExitFlag = Stock_DSM.check_stock_balance()  #sand stock balance


    print(np.size(i))
    # print(i)
    outflow_data.append(O.flatten())
    i = np.where(i >= 0, i, 0)
    inflow_data.append(i.flatten())
outflow_df = pd.DataFrame(outflow_data).T
outflow_df.to_excel('1_outflow.xlsx', sheet_name='Sheet1')
inflow_df = pd.DataFrame(inflow_data).T
inflow_df.to_excel('1_inflow.xlsx', sheet_name='sheet1')

print(np.abs(Bal).sum())  #show sum absolute of all mass balance mismaches





