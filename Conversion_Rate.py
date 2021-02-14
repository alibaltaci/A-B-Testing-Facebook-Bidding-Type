# Conversion Rate

"""
Conversion Rate = Number of Actions / Number of Website Clicks x 100

Number of Actions --> Purchase

Number of website click --> Click

 """

# Import libraries
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import helper_functions as hf

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Load the datasets

# Control Group - Maximum Bidding
df_A = pd.read_excel(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\ab_testing_data.xlsx", sheet_name="Control Group")
df_A.head()

# Test Group - Average Bidding
df_B = pd.read_excel(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\ab_testing_data.xlsx", sheet_name="Test Group")
df_B.head()

# Get rid of empty columns
df_A=df_A[["Impression","Click","Purchase","Earning"]]
df_B=df_B[["Impression","Click","Purchase","Earning"]]

# Conversion Rate for Control Group
hf.conversion_rate(df_A["Purchase"], df_A["Click"]) # 0.11592561427164819

# Conversion Rate for Test Group
hf.conversion_rate(df_B["Purchase"], df_B["Click"]) # 0.15656625309447395

# Conversion rate between Purchase and Impression
# Control Group
hf.conversion_rate(df_A["Purchase"], df_A["Impression"]) # 0.005580006941065655

# Test Group
hf.conversion_rate(df_B["Purchase"], df_B["Impression"]) # 0.004922002820825441


## Check for a statistical difference using the Z-Test.

# Hypothesis Definitions
"""
H0 : (M1 = M2) There is NO statistically significant difference between the conversion rates of the control and test groups.
H1 : (M1 != M2) There is statistically significant difference between the conversion rates of the control and test groups.

"""

# Preparation of data for testing

# Click
total_click_control = df_A["Click"].sum()
total_click_test = df_B["Click"].sum()
click_list = [total_click_control, total_click_test]

# Purchase
total_purchase_control = df_A["Purchase"].sum()
total_purchase_test = df_B["Purchase"].sum()
purchase_list = [total_purchase_control, total_purchase_test]

# Z-Test
hf.hypothesis_test(proportions_ztest(count=purchase_list, nobs=click_list))

# P-value = 0.0000, so that H0 can be REJECTED!

# H1 : (M1 != M2) There is statistically significant difference between the conversion rates of the control and test groups.