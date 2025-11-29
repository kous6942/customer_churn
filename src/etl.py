# src/etl.py
import os
import pandas as pd
import numpy as np
from typing import Tuple

def load_raw(customers_path: str = 'data/raw/customers.csv',
             transactions_path: str = 'data/raw/transactions.csv') -> Tuple[pd.DataFrame, pd.DataFrame]:
    

    ##load raw csvs and parse date columns
    #gives customers_df and transactions_df as dataframes
    customers    = pd.read_csv(customers_path, parse_dates = ['signup_date'], dayfirst=False) 
    tx = pd.read_csv(transactions_path, parse_dates = ['transaction_date'],dayfirst=False)

    return customers, tx

def clean_transactions(tx: pd.DataFrame) -> pd.DataFrame:
    #Clean transaction DataFrame:
    #1. drop duplicates in transaction id

    tx.drop_duplicates(subset =['transaction_id'])

    #2. ensure numerica columns and reasonable totals

    tx['quantity'] = pd.to_numeric(tx['quantity'], errors = 'coerce').fillna(0).astype(int)
    tx['price_per_unit'] = pd.to_numeric(tx['price_per_unit'], errors='coerce').fillna(0.0)
    tx['total_amount'] = pd.to_numeric(tx['total_amount'], errors='coerce')
    tx['total_amount'] = tx['total_amount'].fillna(tx['quantity'] * tx['price_per_unit'])

    #3. normalize categorical text (vectorized string ops)
    tx['payment_method'] = tx['payment_method'].astype(str).str.strip().str.title().replace({'Nan':'Unknown'})
    tx['brand_type'] = tx['brand_type'].astype(str).str.lower().replace({'private':'private','third_party':'third_party'})

    #4. ensure discount flag is binary int
    tx['discount_applied'] = tx.get('discount_applied', 0)
    tx['discount_applied'] = pd.to_numeric(tx['discount_applied'], errors='coerce').fillna(0).astype(int)

    # remove zero/negative total_amount
    tx = tx[tx['total_amount'] > 0].copy()

    return tx   

def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:

    customers = customers.drop_duplicates(subset=['customer_id']).copy()
    customers['signup_date'] = pd.to_datetime(customers['signup_date'], errors='coerce')
    # ensure loyalty_program is binary int
    customers['loyalty_program'] = pd.to_numeric(customers.get('loyalty_program', 0), errors='coerce').fillna(0).astype(int)
    customers['preferred_channel'] = customers['preferred_channel'].astype(str).str.title().fillna('Unknown')
    return customers
                                                  