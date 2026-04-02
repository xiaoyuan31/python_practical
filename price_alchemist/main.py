import tkinter as tk
from tkinter import messagebox
import requests
from textblob import TextBlob

API_KEY = "c10a0487f323472e810228d5963d48a7"

# ---------------- AI ----------------
def analyze_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return "📈 Positive"
    elif score < 0:
        return "📉 Negative"
    else:
        return "🟡 Neutral"

# ---------------- API ----------------
def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}"
    response = requests.get(url).json()
    return response.get("articles", [])[:5]

def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url).json()
    return response

# ---------------- UI Logic ----------------
def search():
    topic = entry.get().lower()

    if topic == "":
        messagebox.showwarning("Warning", "Enter a topic")
        return

    listbox.delete(0, tk.END)

    # News
    articles = get_news(topic)

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        sentiment = analyze_sentiment(title)

        listbox.insert(tk.END, f"{i}. {title}")
        listbox.insert(tk.END, f"   {sentiment}")
        listbox.insert(tk.END, "")

    # Price
    price_data = get_price(topic)

    if topic in price_data:
        price = price_data[topic]["usd"]
        price_label.config(text=f"💰 Price: ${price}")
    else:
        price_label.config(text="💰 Price: Not found")

# ---------------- UI ----------------
root = tk.Tk()
root.title("🧪 Price Alchemist")
root.geometry("500x600")

# Title
title_label = tk.Label(root, text="🧪 Price Alchemist", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Entry
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=10)

# Button
search_btn = tk.Button(root, text="Search", command=search)
search_btn.pack(pady=5)

# Price Label
price_label = tk.Label(root, text="💰 Price: ", font=("Arial", 12))
price_label.pack(pady=10)

# Listbox
listbox = tk.Listbox(root, width=60, height=20)
listbox.pack(pady=10)

root.mainloop()