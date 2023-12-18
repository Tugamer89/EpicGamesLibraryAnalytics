import os
import pandas as pd
import matplotlib.pyplot as plt

if not os.path.exists("./images"):
    os.makedirs("./images")

def get_plot_size(x):
    return round((7 * len(x) + 1867)/122);

df = pd.read_csv("output.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

df["Date Year"] = df["Date"].dt.year
df["Date Month"] = df["Date"].dt.month
df["Date Year Month"] = df["Date Year"].astype(str) + "-" + df["Date Month"].astype(str).str.zfill(2)

average_price = round(df["Price"].mean(), 2)
price_sum = round(df["Price"].sum(), 2)
print(f'Average: {average_price:>{len(str(float(price_sum)))}} €')
print(f'Total:   {price_sum} €')

# Price chart over time
plt.figure(figsize=(18, 6))
plt.plot(df["Date"], df["Price"], linestyle='-', color='b')
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Price chart over time")
plt.xticks(rotation=45, ha="right")
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(50))
plt.tight_layout()
plt.savefig("./images/price_over_time.png", dpi=300)
plt.close()

# Graph of the average prices over the months
average_price_mese = df.groupby("Date Year Month")["Price"].mean()
plt.figure(figsize=(get_plot_size(average_price_mese), 6))
plt.bar(average_price_mese.index, average_price_mese.values, color='tab:blue')
plt.xlabel("Month")
plt.ylabel("Price")
plt.title("Graph of the average prices over the months")
plt.xticks(rotation=45, ha="right")
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(50))
plt.tight_layout()
plt.savefig("./images/average_price_over_months.png", dpi=300)
plt.close()

# Graph of average prices by distributor
average_price_distributore = df.groupby("Distributor")["Price"].mean()
plt.figure(figsize=(get_plot_size(average_price_distributore), 6))
plt.bar(average_price_distributore.index, average_price_distributore.values, color='c')
plt.xlabel("Distributor")
plt.ylabel("Average price")
plt.title("Graph of average prices by distributor")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig("./images/average_price_by_distributor.png", dpi=300)
plt.close()

# Graph of distributors over time
distributors_per_year = df.groupby("Date Year Month")["Distributor"].nunique()
plt.figure(figsize=(get_plot_size(distributors_per_year), 6))
plt.plot(distributors_per_year, linestyle='-', marker='o', color='g')
plt.xlabel("Month")
plt.ylabel("Number of distributors")
plt.title("Graph of distributors over time")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(50, integer=True))
plt.tight_layout()
plt.savefig("./images/distributors_over_time.png", dpi=300)
plt.close()

# Graph of the number of orders over time
orders_per_year = df.groupby("Date Year Month")["Order ID"].nunique()
plt.figure(figsize=(get_plot_size(orders_per_year), 6))
plt.plot(orders_per_year, linestyle='-', marker='o', color='m')
plt.xlabel("Month")
plt.ylabel("Number of orders")
plt.title("Graph of the number of orders over time")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(50, integer=True))
plt.tight_layout()
plt.savefig("./images/orders_number_over_time.png", dpi=300)
plt.close()
