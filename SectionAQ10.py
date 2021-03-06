## Quesiton 10
import pandas as pd
import numpy as np
from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Spark').getOrCreate()

df = spark.read.format("com.databricks.spark.csv").option("header", "true").load("flights.csv")

df2 = spark.read.format("com.databricks.spark.csv").option("header", "true").load("airports.csv")

df.registerTempTable("df")
df2.registerTempTable("df2")

ds= spark.sql("select OriginAirportID,Sum(DepDelay) AS Total_DepDelay from df Group by OriginAirportID")
ds2= spark.sql("select airport_id,city from df2")


dataset1= ds.toPandas()
dataset2= ds2.toPandas()

dataset1.set_index('OriginAirportID')
dataset2.set_index('airport_id')

dataset3= dataset2.loc[dataset2['airport_id'].isin(dataset1['OriginAirportID'])]

dataset3.set_index('airport_id')
dataset4= dataset1.loc[dataset1['OriginAirportID'].isin(dataset2['airport_id'])]

dataset3.rename(columns = {'city': 'Origin'}, inplace = True)
dataset4.rename(columns = {'OriginAirportID': 'airport_id'}, inplace = True)

dataset5= pd.merge(dataset3, dataset4, on="airport_id")
dataset5.dropna()

print(dataset5.head())
