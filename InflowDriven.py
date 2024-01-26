# 0 引进包
from dynamic_stock_model import DynamicStockModel   # import model
import numpy as np  # calculation package
import matplotlib.pyplot as plt    # import mapping package
import xlrd    # for reading excel
import pandas as pd   # for export data

# 1. Load and check data1

BitumenInflowExcel = xlrd.open_workbook('4_Inflow.xlsx')     # data for bitumen
BitumenInflow_DataSheet = BitumenInflowExcel.sheet_by_name('Sheet1')
BitumenInflowLTExcel = xlrd.open_workbook('4_Inflow_LT.xlsx')   # data for bitumen lifetime
BitumenInflowLT_DataSheet = BitumenInflowLTExcel.sheet_by_name('Sheet1')
outflow_data = []
DynamicStock_data = []
Stock_data = []

Years = []   # 121 for bitumen from 1900 to 2019; 91 for cement from 1930 to 2019.
for m in range(1,121):  # read year
    Years.append(int(BitumenInflow_DataSheet.cell_value(m,0)))

for col in range(1,185):   # data for 184 countries
    BitumenInflow = []
    LifeTime = []
    for r in range(1,121):
        BitumenInflow.append(float(BitumenInflow_DataSheet.cell_value(r,col)))    # read stock
    for r in range(1,121):
        LifeTime.append(float(BitumenInflowLT_DataSheet.cell_value(r, col)))

    # 2. Import Model
    BitumenInflow_DSM = DynamicStockModel(t = Years, i = BitumenInflow,
                                             lt = {'Type':'Normal', 'Mean': np.array(LifeTime),
                                                   'StdDev': 0.15*np.array(LifeTime) })     #23-fold paper setting: 0.15

    CheckStr, ExitFlag = BitumenInflow_DSM.dimension_check()
    # print(CheckStr)

    s_c, ExitFlag = BitumenInflow_DSM.compute_s_c_inflow_driven()
    o_c, ExitFlag = BitumenInflow_DSM.compute_o_c_from_s_c()


    O, ExitFlag = BitumenInflow_DSM.compute_outflow_total()
    outflow_data.append(O.flatten())
    S, ExitFlag = BitumenInflow_DSM.compute_stock_total()
    Stock_data.append(S.flatten())
    print(np.size(O))
BitumenOutflow_df = pd.DataFrame(outflow_data).T
BitumenOutflow_df.to_excel('4_Outflow.xlsx', sheet_name='Sheet1')
BitumenStock_df = pd.DataFrame(Stock_data).T
BitumenStock_df.to_excel('4_Stock.xlsx', sheet_name='Sheet1')

