#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install urllib3')
get_ipython().system('pip install boto3')
# get_ipython().run_line_magic('load_ext', 'autotime')
get_ipython().system('pip install ipympl')
#Import the necessary packages
import io
import boto3
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from datetime import datetime 
from time import time
from pandas.core.api import isnull
from numpy import isnan
# from google.colab import files
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# link = "https://822787745626.signin.aws.amazon.com/console" 
# user_name = "python_turno"
class ParquetToDataFrame():
    def __init__(self, option, date, vehicle_no):
        session = boto3.Session(aws_access_key_id="AKIA37EPYU5NE2TTUYCX",
                                aws_secret_access_key="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")        
        self.client = session.client('s3')
        self.s3 = session.resource('s3')
        self.bucket = 'battery-oem-data'
        self.option = option
        self.vehicle_no = vehicle_no
        self.date = datetime.strptime(date, "%d-%m-%Y")
        self.day = self.date.day
        self.month = self.date.month
        self.year = self.date.year
        self.prefix = self.create_prefix()

    def create_prefix(self):
        if self.month <= 10:
            month = '0'+ str(self.month)
        else:
            month = str(self.month)
        if self.day <= 10:
            day = '0'+ str(self.day)
        else:
            day = str(self.day)
        prefix = ('intellicar/stream/enriched-v1/'+str(self.option)+'-data/year='+str(self.year)+'/month='+ month +'/day='+ day)
        return prefix
        
        
    def get_data(self):
        df = pd.DataFrame()
        prefix = self.prefix
        objects_dict = self.client.list_objects_v2(Bucket=self.bucket, Prefix= prefix)
        for item in objects_dict['Contents']:
            if item['Key'].endswith('.parquet'):
                s3_keys = [item['Key']]
                buffers = [self.download_s3_parquet_file(key) for key in s3_keys]
                dfs = [pq.read_table(buffer).to_pandas() for buffer in buffers]
                data = pd.concat(dfs, ignore_index=True)
                df = df.append(data)
        data_df = df[df['vehicleNo'] == self.vehicle_no]
        data_df = self.additional_fields(data_df)      
        return data_df

    def download_s3_parquet_file(self,key):
        buffer = io.BytesIO()
        self.s3.Object(self.bucket, key).download_fileobj(buffer)
        return buffer 

    def additional_fields(self,df):
        df = df.sort_values(by = 'time')
        df['delta_t'] = ((df['time'] - df['time'].shift(1)))/1000 #delta_t in seconds
        df['timestamp'] = pd.to_datetime(df['time'],unit='ms')
        df['Date_conv'] = pd.to_datetime(df['timestamp']).dt.date
        df['Time_conv'] = pd.to_datetime(df['timestamp']).dt.time
        return df
