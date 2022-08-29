from curses import meta
from typing_extensions import Self
import pandas as pd
import numpy as np
import dateutil.parser as dp
from datetime import datetime as dt
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABCMeta, abstractmethod
import pickle
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess
import sympy as sy
from datetime import timedelta
import warnings

warnings.filterwarnings("ignore")


'''
Abstract Class for Estimator
'''
class estimator(metaclass=ABCMeta):

    @abstractmethod
    def estimate(self, data:pd.DataFrame) -> np.double:
        pass

'''
Air Cleaner Filter RUL Estimator
'''
class filterRUL(estimator):
    def __init__(self, life:int, model:str) -> None:

        '''
        Hyper-parameters & Custom parameters
        '''
        self._max_lifetime = life    # Maximum Filter Lifetime
        self._outcabin_mean = 67.24013933547695 # should be changed
        self._outcabin_std = 54.32043175206877 # should be changed
        self._inflow_cutoff = 70
        self._ols_dt_min = 10

        if model is None:
            self.model = pickle.load(open('knn_outcabin', 'rb'))
        else:
            self.model = pickle.load(open(model, 'rb'))

    def estimate(self, data:pd.DataFrame, start_date:str, end_date:str) -> dict:

        # 1. estimate outcabin pm2.5
        input = data.dropna()["airkorea_pm25_z_filtered"]
        outcabin_pm25 = self.model.predict(input.to_numpy().reshape(-1,1))

        # 2. z-score reverse (for outcabin pm2.5)
        outcabin_pm25_list = outcabin_pm25.reshape(-1).tolist()
        data["auton_outcabin_pm25_z"] = pd.Series(outcabin_pm25_list, index=input.index)
        data["auton_outcabin_pm25"] = data["auton_outcabin_pm25_z"]*self._outcabin_std+self._outcabin_mean

        # 3. pm2.5 concentration flows into the in-cabin
        data["auton_inflow_pm25"] = data["auton_outcabin_pm25"]*(1-self._inflow_cutoff/100)

        # 4. RUL condition indication with OLS
        t_data = data[["date", 'auton_inflow_pm25', 'auton_incabin_pm25']]
        t_range = pd.date_range(start=start_date, end=end_date, freq='{}min'.format(self._ols_dt_min))

        
        stack = {}
        for start_date in t_range.to_list():
            end_date = start_date + timedelta(minutes=self._ols_dt_min)
            mask = (t_data['date'] > start_date) & (t_data['date'] <= end_date)

            t_sliced = t_data.loc[mask][['date', 'auton_inflow_pm25', 'auton_incabin_pm25']]

            if t_sliced.dropna().empty is False:

                y1_data = t_sliced['auton_inflow_pm25']
                y2_data = t_sliced['auton_incabin_pm25']
                x_data = t_sliced.index

                mask_1 = ~np.isnan(x_data) & ~np.isnan(y1_data)
                mask_2 = ~np.isnan(x_data) & ~np.isnan(y2_data)
                res_1 = stats.linregress(x_data[mask_1], y1_data[mask_1])
                res_2 = stats.linregress(x_data[mask_2], y2_data[mask_2])

                def g(x):
                    return res_1.slope*x+res_1.intercept
                def u(x):
                    return res_2.slope*x+res_2.intercept

                x = sy.Symbol('x')
                area = sy.integrate(g(x) - u(x), (x, x_data.min(), x_data.max()))
                if area != sy.nan:
                    stack[start_date] = area
                
        stack_area = pd.DataFrame(data=list(stack.items()), columns=['date', 'area'])
        cumsum = stack_area["area"].dropna().cumsum(axis=0)

        result = {}
        result["max_life"] = self._max_life
        result["life"] = cumsum.values[-1]
        result["rul"] = (cumsum.values[-1]/self._max_life)*100
        return result


'''
Load data form file
'''
# def loaddata_from_file(filepath:str) -> pd.DataFrame:

#     # 1. load raw data from file
#     # [Warning] 1st Column = date, 2nd Column = value
#     airkorea_pm25 = pd.read_excel(filepath, header=None, sheet_name='실외 초미세먼지 농도', parse_dates=[0])
#     airkorea_pm25.columns = ['date', 'airkorea_pm25']
#     auton_incabin_pm25 = pd.read_excel(filepath, header=None, sheet_name='차량내 초미세먼지 농도', parse_dates=[0])
#     auton_incabin_pm25.columns = ['date', 'auton_incabin_pm25']

#     # 2. date merge
#     aligned_pm25 = pd.merge_asof(auton_incabin_pm25, airkorea_pm25, on=['date'])
    
#     # 3. return raw data (without preprocessing)
#     return aligned_pm25

def loaddata_from_df(df_airkorea,df_sensor) -> pd.DataFrame:

    # 1. load raw data from file
    # [Warning] 1st Column = date, 2nd Column = value
    #airkorea_pm25 = pd.read_excel(filepath, header=None, sheet_name='실외 초미세먼지 농도', parse_dates=[0])
    airkorea_pm25=pd.DataFrame(index=range(0), columns=['date', 'airkorea_pm25']) 
    for airkorea in df_airkorea:
        airkorea_pm25.append({'date' : airkorea['pub_date'],'airkorea_pm25': airkorea['airkorea']['P.M 2.5']}, ignore_index=True)
        
    #auton_incabin_pm25 = pd.read_excel(filepath, header=None, sheet_name='차량내 초미세먼지 농도', parse_dates=[0])

    auton_incabin_pm25=pd.DataFrame(index=range(0), columns=['date', 'auton_incabin_pm25']) 
    for sensor in df_sensor:
        auton_incabin_pm25.append({'date' : sensor['pub_date'],'auton_incabin_pm25': sensor['sensor']['P.M 2.5']}, ignore_index=True)
        
    # 2. date merge
    aligned_pm25 = pd.merge_asof(auton_incabin_pm25, airkorea_pm25, on=['date'])
    
    # 3. return raw data (without preprocessing)
    return aligned_pm25


'''
Preprocessing
'''
def preprocess(aligned_data:pd.DataFrame) -> pd.DataFrame:

    # 1. zero to NaN
    aligned_data["airkorea_pm25"] = aligned_data["airkorea_pm25"].replace(0,np.NaN)

    # 2. Z-score Normalization
    aligned_data["airkorea_pm25_z"] = stats.zscore(aligned_data["airkorea_pm25"].dropna())

    # 3. LOWESS Filtering
    _lowess_fraction = 0.01 # 1% data will be used for local regression
    airkorea_filtered = lowess(aligned_data["airkorea_pm25_z"].values, aligned_data["airkorea_pm25_z"].index.values, frac=_lowess_fraction)
    index, data = np.transpose(airkorea_filtered)
    aligned_data["airkorea_pm25_z_filtered"] = pd.Series(data, index=index.astype(int))


def deeplearning(df_airkorea,df_sensor):
    # 1. load data
    #data = loaddata_from_file(filepath="./data/44_2022-3-1_2022-3-31.xlsx")
    try:
        data=loaddata_from_df(df_airkorea,df_sensor)
        preprocess(data)

        # 2. estimate from data
        model = filterRUL(life=1000000, model='knn_outcabin')
        result = model.estimate(data, '2022-03-01', '2022-04-01')
        print("RUL Indication : {}% ({}/{})".format(result["rul"], result["life"],result["max_life"]))
        return result["rul"], result["life"],result["max_life"]
    except:
        return None
