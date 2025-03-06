import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set correct data path
path = r"C:\Users\ahmed\Desktop\adham\project dataset\comp project\data"

# List of dataset files
files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# Load datasets into a dictionary
datasets = {name: pd.read_csv(os.path.join(path, filename)) for name, filename in files.items()}

# Replace missing values
datasets["orders"]["order_approved_at"].fillna("Not Approved", inplace=True)
datasets["orders"]["order_delivered_carrier_date"].fillna("Not Shipped", inplace=True)
datasets["orders"]["order_delivered_customer_date"].fillna("Not Delivered", inplace=True)
datasets["products"]["product_category_name"].fillna("Unknown", inplace=True)

columns_to_fill = ["product_name_lenght", "product_description_lenght", "product_photos_qty"]
for col in columns_to_fill:
    datasets["products"][col].fillna(datasets["products"][col].median(), inplace=True)

size_columns = ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
for col in size_columns:
    datasets["products"][col].fillna(datasets["products"][col].median(), inplace=True)

datasets["order_reviews"]["review_comment_title"].fillna("No Title", inplace=True)
datasets["order_reviews"]["review_comment_message"].fillna("No Comment", inplace=True)

# Order Status Distribution
order_status_counts = datasets["orders"]["order_status"].value_counts()
plt.figure(figsize=(10, 5))
sns.barplot(x=order_status_counts.index, y=order_status_counts.values, palette="viridis")
plt.xlabel("Order Status")
plt.ylabel("Count")
plt.title("Distribution of Order Status")
plt.xticks(rotation=45)
plt.show()

# Orders Distribution by Day of the Week
datasets["orders"]["order_purchase_timestamp"] = pd.to_datetime(datasets["orders"]["order_purchase_timestamp"])
datasets["orders"]["order_day"] = datasets["orders"]["order_purchase_timestamp"].dt.day_name()
order_day_counts = datasets["orders"]["order_day"].value_counts()
plt.figure(figsize=(10, 5))
sns.barplot(x=order_day_counts.index, y=order_day_counts.values, palette="coolwarm")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Orders")
plt.title("Orders Distribution by Day of the Week")
plt.xticks(rotation=45)
plt.show()

# Monthly Orders Count
datasets["orders"]["month"] = datasets["orders"]["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = datasets["orders"].groupby("month").size()
plt.figure(figsize=(12, 6))
monthly_orders.plot(kind="line", marker="o", color="orange")
plt.title("Monthly Orders Count")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.grid(True)
plt.show()

# Monthly Revenue
order_items_merged = pd.merge(datasets["order_items"], datasets["orders"], on="order_id")
order_items_merged["revenue"] = order_items_merged["price"] + order_items_merged["freight_value"]
monthly_revenue = order_items_merged.groupby("month")["revenue"].sum()
plt.figure(figsize=(12, 6))
monthly_revenue.plot(kind="bar", color="green")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.grid(True)
plt.show()

# Average Order Value
average_order_value = monthly_revenue / monthly_orders
plt.figure(figsize=(12, 6))
average_order_value.plot(kind="line", marker="o", color="blue")
plt.title("Average Order Value")
plt.xlabel("Month")
plt.ylabel("Average Order Value")
plt.grid(True)
plt.show()

# Correlation Heatmap
numeric_cols = order_items_merged.select_dtypes(include=["float64", "int64"])
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# Export cleaned datasets
for name, df in datasets.items():
    df.to_csv(os.path.join(path, f"cleaned_{name}.csv"), index=False)
