#!/usr/bin/env python
# coding: utf-8

# ## Silver_Transformations_Notebook_ShoppingMartData
# 
# New notebook

# ### SILVER LAYER NOTEBOOK: DATA CLEANING AND INTEGRATION
# ##### LOAD DATA FROM BRONZE LAYER
# 

# In[1]:


from pyspark.sql.functions import *


# In[3]:


df_customers = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Customers/ShoppingMart_customers.csv")
df_orders = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Orders/ShoppingMart_orders.csv")
df_products = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Products/ShoppingMart_products.csv")


# In[4]:


display(df_orders.limit(10))


# In[5]:


df_orders=df_orders.dropna(subset=['OrderID','OrderDate','CustomerID','ProductID','TotalAmount'])


# In[6]:


df_orders=df_orders.withColumn('OrderDate',to_date(col('OrderDate')))


# In[7]:


df_orders=df_orders \
    .join (df_customers, on ='CustomerID', how="inner") \
    .join (df_products,on='ProductID',how="inner")
    


# In[8]:


display(df_orders.limit(10))


# In[11]:


df_orders.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Orders/ShoppingMart_customers_orderdata")


# # Unstructured Data

# In[12]:


df_reviews = spark.read.json("Files/ShoppingMart_Bronze_Reviews/ShoppingMart_review.json")
display(df_reviews.limit(10))


# In[13]:


df_social = spark.read.json("Files/ShoppingMart_Bronze_Social_Media/ShoppingMart_social_media.json")
df_weblogs = spark.read.json("Files/ShoppingMart_Bronze_Web_Logs/ShoppingMart_web_logs.json")


# In[14]:


df_reviews.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Reviews/ShoppingMart_reviews")
df_social.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Social_Media/ShoppingMart_social_media")
df_weblogs.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Web_Logs/ShoppingMart_web_logs")

