Importing necessary libraries

def load_raw():
Creating function called load_raw that loads the customers.csv and transactions.csv files from their location in data/raw/customers and data/raw/transactions

customers = pd.read_csv(customers_path, parse_dates=['signup_date'], dayfirst=False)
tx

Assigning these variables to customers and tx which loads the csv file from the path and calls it to be read
parse_dates is a parameter in pd.read_csv that converts specific columns into Datetime Objects rather than leaving them as generic Strings. This is to unlock further datetime oriented functionalities instead of being limited to dates as strings and of course to maintain consistency
return customers, tx

Moving on to the next function def clean_transactions is a function to clean the csv file

drop.duplicates() removes duplicate transaction rows by transaction_id

pd.to_numeric(...., errors = 'coerce') converts values to numeric form and errors... turns bad values to NaN which is futher filled by .fillna(0) fixes it to 0 as an int

