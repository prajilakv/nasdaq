import pandas as pd
import nasdaqdatalink
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


"""
Data Extraction class is defined here.
"""
class DataExtraction():

    def fse_data(self):
        fse_df = nasdaqdatalink.get("FSE/BDT_X")
        fse_df = fse_df.dropna(subset=['Close', 'Open'])
        return fse_df
 
"""
Data Manipulation Logics are defined in the below class
"""
    
class DataManipulation():
   
    def get_moving_average(self,window=None, df=None):
        try:
            for win in window:
                df['MA_'+str(win)] = df['Close'].rolling(window=win).mean()
            return df   

        except Exception as e:
            print(e)
    
    def get_monthly_average(self,df):
        try:
            df_avg = df.groupby(pd.Grouper(freq='M'))['Close'].mean()
            return df_avg
        except Exception as e:
            print(e)
            
    def get_consecutive_high(self,df):
        try:
            df["is_consecutive_high"] = (df["Close"].rolling(5).apply(lambda x: (x.diff().fillna(0) >= 0).all()))
            return df
        except Exception as e:
            print(e)
            
    def get_consecutive_low(self,df):
        try:
            df["is_consecutive_low"] = (df["Close"].rolling(4).apply(lambda x: (x.diff().fillna(0) <= 0).all()))
            return df
        except Exception as e:
            print(e)
            

            
##Data Is Extracted here from the API 

data_df = DataExtraction().fse_data()

"""
Data Manipulations are done here. 

"""

data_df_moving_avge_consecutive = DataManipulation().get_moving_average([90,30,7],data_df) #moving average window can be passed as a list
data_df_moving_avge_consecutive = DataManipulation().get_consecutive_high(data_df_moving_avge_consecutive) # 5 days consecutive high dates are marked as 1.0. Green Upward triangle is marked on the graph
data_df_moving_avge_consecutive = DataManipulation().get_consecutive_low(data_df_moving_avge_consecutive) # 4 days consecutive low is marked as 1.0. Red downward triangle is marked on the graph
data_df_monthly_average = DataManipulation().get_monthly_average(data_df) # monthly average is calculated


"""
Data Presentation logic is done here
"""

#set axes
fig, ax = plt.subplots(figsize = (15,8))
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.DayLocator())

# different date ranges can be selected for plotting the charts
date_slicing_from = '2008-10-01'
date_slicing_to   = '2008-12-01'

# monthly average
data_df_monthly_average[date_slicing_from :date_slicing_to].plot(use_index=True, kind='line',ax=ax, color='red',legend=True) 

#Moving averages
data_df_moving_avge_consecutive[date_slicing_from :date_slicing_to].plot(y = ['MA_90'],use_index=True, kind = 'line', ax = ax, secondary_y=True,color='blue',legend=True)
data_df_moving_avge_consecutive[date_slicing_from :date_slicing_to].plot(y = ['MA_30'],use_index=True, kind = 'line', ax = ax, secondary_y=True,color='orange',legend=True)
data_df_moving_avge_consecutive[date_slicing_from :date_slicing_to].plot(y = ['MA_7'],use_index=True, kind = 'line', ax = ax, secondary_y=True,color='green',legend=True)

#Consecutive high and low
data_df_moving_avge_consecutive_2012_2008 = data_df_moving_avge_consecutive.loc[date_slicing_from :date_slicing_to]
data_df_moving_avge_consecutive_H = data_df_moving_avge_consecutive_2012_2008.loc[data_df_moving_avge_consecutive_2012_2008['is_consecutive_high'] == 1.0]
data_df_moving_avge_consecutive_L = data_df_moving_avge_consecutive_2012_2008.loc[data_df_moving_avge_consecutive_2012_2008['is_consecutive_low'] == 1.0]

plt.scatter(data_df_moving_avge_consecutive_H.index.values, data_df_moving_avge_consecutive_H['Close'].values,marker="^",c='green')#high
plt.scatter(data_df_moving_avge_consecutive_L.index.values, data_df_moving_avge_consecutive_L['Close'].values,marker="v",c='red')#low

plt.legend(loc='upper left')
plt.show()