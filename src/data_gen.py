import pandas as pd
import numpy as np

def generate_customer_data(n=1000):
    np.random.seed(42)
    data = {
        "customer_id": range(1, n+1),
        "age": np.random.randint(18, 70, n),
        "tenure_months": np.random.randint(1, 60, n),
        "monthly_spend": np.random.randint(200, 2000, n),
        "churned": np.random.choice([0, 1], size=n, p=[0.8, 0.2])
    }
    return pd.DataFrame(data)


df = generate_customer_data(20)
print(df.head())


# src/data_gen.py (realistic generator)
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, date

fake = Faker()

def generate_customers(n_customers=2000,signup_start = datetime(2020, 1, 1).date()):
    """Create a DataFrame of customer metadata."""
    customers = []
    for i in range(n_customers):
        signup_end = datetime(2023, 12, 31).date()  # proper date object
        sd = fake.date_between(start_date=signup_start, end_date=signup_end)

        customers.append({
        'customer_id': f"C{i+1:05d}",
        'age': random.randint(18, 70),
        'gender': random.choice(['M', 'F', 'Other']),
        'location': fake.city(),
        'income_level': random.choices(['low', 'medium', 'high'], weights=[0.4,0.4,0.2])[0],
        'signup_date': pd.to_datetime(sd),
        'loyalty_program': random.choice([0, 1]),   # 0 = not enrolled, 1 = enrolled
        'preferred_channel': random.choice(['Online', 'Offline', 'Both'])
    })

    return pd.DataFrame(customers)

def generate_transactions(customers_df, n_transactions=20000, end_date=datetime(2024, 8, 31).date()):

    """Create a DataFrame of transaction records (one row per purchase)."""
    products = ['Rice', 'Snacks', 'Shampoo', 'Soap', 'Toothpaste', 'Oil','C-Type Cable','Chair','Laptop Case','Earphones']
    price_map = {'Rice':60, 'Snacks':50, 'Shampoo':120, 'Soap':40, 'Toothpaste':80, 'Oil':200,'C-Type Cable':300,'Chair':1500,'Laptop Case':800,'Earphones':600}

    customer_ids = customers_df['customer_id'].tolist()
    signup_map = dict(zip(customers_df['customer_id'], customers_df['signup_date']))

    tx_rows = []
    for i in range(n_transactions):
        cid = random.choice(customer_ids)
        start = signup_map[cid]   # convert pandas.Timestamp to datetime.date
        tx_date = fake.date_between(start_date=start, end_date=end_date)
        product = random.choice(products)
        brand = random.choices(['private', 'third_party'], weights=[0.35, 0.65])[0]
        qty = random.choices([1,2,3,5,10,15], weights=[0.60,0.15,0.10,0.05,0.05,0.05])[0]
        price = price_map[product]
        tx_rows.append({
        'transaction_id': f"T{i+1:07d}",
        'customer_id': cid,
        'transaction_date': pd.to_datetime(tx_date),
        'product_category': product,
        'brand_type': brand,
        'payment_method': random.choice(['Cash', 'Card', 'UPI/Wallet']),
        'quantity': qty,
        'price_per_unit': price,
        'discount_applied': random.choice([0, 1]),  # binary flag
        'total_amount': price * qty * (0.9 if random.random() < 0.2 else 1.0)  # 20% chance of discount
    })


    return pd.DataFrame(tx_rows)

def generate_and_save(out_dir='data/raw', n_customers=2000, n_transactions=20000):
    """Main helper: generate and save CSVs."""
    customers = generate_customers(n_customers)
    transactions = generate_transactions(customers, n_transactions)
    # ensure output folder exists (safe)
    import os
    os.makedirs(out_dir, exist_ok=True)
    customers.to_csv(f"{out_dir}/customers.csv", index=False)
    transactions.to_csv(f"{out_dir}/transactions.csv", index=False)
    print(f"Saved customers ({len(customers)}) and transactions ({len(transactions)}) to {out_dir}")

if __name__ == "__main__":
    # For reproducibility, seed the RNGs
    random.seed(42)
    np.random.seed(42)
    Faker.seed(42)

    generate_and_save(n_customers=2000, n_transactions=20000)
