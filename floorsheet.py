#streamlit practice

import streamlit as st
import numpy as np
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
import numpy as np
import pandas as pd
import glob as gl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options


st.title('Daily Floor Sheet Analysis')
df = pd.DataFrame()
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Load Recent Data')
if pressed:
    refer = "http://www.nepalstock.com/floorsheet"
    options = Options()
    #options.add_argument('no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    #options.headless = True
    browser = webdriver.Firefox()
    browser.implicitly_wait(40)
    browser.get(refer)
    no_of_rows = Select(browser.find_element_by_xpath('/html/body/div[5]/table/tbody/tr[1]/td/form/label[5]/select'))
    no_of_rows.select_by_visible_text(no_of_rows.options[4].text)
    browser.find_element_by_xpath('//*[@id="news_info-filter"]/input[1]').click()
    c = browser.find_element_by_xpath('//*[@id="home-contents"]/table/tbody/tr[503]/td/div/a[1]').text
    floor_df = pd.DataFrame()
    for i in range(0,(int(c[7:10])+1)):
        link = "http://www.nepalstock.com/main/floorsheet/index/{0}/?contract-no=&stock-symbol=&buyer=&seller=&_limit=500".format(i)
        browser.get(link)
        source = browser.page_source
        temp_df = pd.read_html(source)[0][1:501]
        floor_df = floor_df.append(temp_df)
        time.sleep(5)
#    data_load_state.text('Loading data...done!')
    #
    # Save File as csv_current_datetime
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    floor_df.to_csv("Floorsheet_New", header=False)
    ana_df = pd.read_csv("Floorsheet_New")
    final_df = ana_df.iloc[:-3]
    final_df.drop(columns = ['Unnamed: 9', 'Unnamed: 10','1','S.N.'], inplace=True)
    df = final_df
else:
    df = pd.read_csv('Floorsheet') #Change This in First Run to CSV file downloaded while running 1st script
    df = df.iloc[:-3]
    df.drop(columns = ['Unnamed: 9', 'Unnamed: 10','1','S.N.'], inplace=True)

st.write("# Floor Sheet")
#df.drop(columns = ['Unnamed: 9', 'Unnamed: 10','1'], inplace=True)

df
df["Amount"] = pd.to_numeric(df['Amount'], errors='coerce')

st.write("## According to Stock Symbol")
option = st.sidebar.selectbox(
    '',
     df['Stock Symbol'].unique())
Symbol = df[df['Stock Symbol']==option]
Symbol.reset_index(drop = True, inplace=True)
Symbol

st.write("## According to Buyer Broker")
buyers = st.sidebar.selectbox(
    '',
     df['Buyer Broker'].unique())
buyer = df[df['Buyer Broker']==buyers]
buyer.reset_index(drop = True, inplace=True)
buyer

st.write("## According to Seller Broker")
sellers = st.sidebar.selectbox(
    '',
     df['Seller Broker'].unique())
seller = df[df['Seller Broker']==sellers]
seller.reset_index(drop=True, inplace=True)
seller

st.write("## Buyer Broker and Symbol")
buyer_symbol = df[(df["Buyer Broker"]==buyers) & (df["Stock Symbol"]==option)]
buyer_symbol.reset_index(drop=True,inplace=True)
buyer_symbol


st.write("## Seller Broker and Symbol")
seller_symbol = df[(df["Seller Broker"]==sellers) & (df["Stock Symbol"]==option)]
seller_symbol.reset_index(drop=True,inplace=True)
seller_symbol

st.write("## High amount Transactions ")
amt = [100000, 200000, 300000, 400000, 500000]
amount = st.sidebar.selectbox(
    '',
     amt)
transac = df[df['Amount']>=amount]
transac.reset_index(drop = True, inplace=True)
transac

st.write("## High Amount and Company")
hgh_com = df[(df["Amount"]>=amount) & (df["Stock Symbol"]==option)]
hgh_com.reset_index(drop = True, inplace=True)
hgh_com

st.write("## High Amount and Buyer Broker")
hgh_brokr = df[(df["Amount"]>=amount) & (df["Buyer Broker"]==buyers)]
hgh_brokr.reset_index(drop = True, inplace = True)
hgh_brokr

st.write("## High Amount and Seller Broker")
sel_brokr = df[(df["Amount"]>=amount) & (df["Seller Broker"]==sellers)]
sel_brokr.reset_index(drop = True, inplace = True)
sel_brokr

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Export Results??')
if pressed:
    seller_symbol.to_csv("Seller Broker & Symbol.csv")
    buyer_symbol.to_csv("Buyer Broker & Symbol.csv")
    seller.to_csv("Seller Broker.csv")
    buyer.to_csv("Buyer Broker.csv")
    Symbol.to_csv("According to Symbol")
    transac.to_csv("High Transactions.csv")
    hgh_com.to_csv("High Transactions According to Symbol.csv")
    sel_brokr.to_csv("sell_brokr.csv")
    hgh_brokr.to_csv("hgh_broker.csv")
    st.write("Results Exported as CSV")
