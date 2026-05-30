import pandas as pd

def get_orders_df(orders):
    return pd.read_csv(orders)

def get_order_items_df(order_items):
    return pd.read_csv(order_items)

def get_products_df(products):
    return pd.read_csv(products)

def get_users_df(users):
    return pd.read_csv(users)