import tkinter as tk
from tkinter import messagebox
import requests
from textblob import TextBlob
from tkmacosx import Button  # Use tkmacosx for better button support on MacOS

API_KEY = "c10a0487f323472e810228d5963d48a7"

# ---------------- AI ----------------
def analyze_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

# ---------------- API ----------------
def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}"
    return requests.get(url).json().get("articles", [])[:5]

def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    return requests.get(url).json()

# ---------------- UI Logic ----------------
def search():
    topic = entry.get().lower()

    if topic == "":
        messagebox.showwarning("Warning", "Enter a topic")
        return

    text_area.config(state="normal")
    text_area.delete("1.0", tk.END)

    # NEWS
    articles = get_news(topic)

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        sentiment = analyze_sentiment(title)

        text_area.insert(tk.END, f"{i}. {title}\n")

        if sentiment == "positive":
            text_area.insert(tk.END, "   📈 Positive\n\n", "green")
        elif sentiment == "negative":
            text_area.insert(tk.END, "   📉 Negative\n\n", "red")
        else:
            text_area.insert(tk.END, "   🟡 Neutral\n\n", "yellow")

    # PRICE
    price_data = get_price(topic)
    if topic in price_data:
        price = price_data[topic]["usd"]
        price_label.config(text=f"💰 ${price}")
    else:
        price_label.config(text="💰 Not found")

    text_area.config(state="disabled")

# ---------------- UI ----------------
root = tk.Tk()
root.title("🧪 Price Alchemist")
root.geometry("600x650")
root.configure(bg="#1e1e1e")

# Title
tk.Label(root, text="🧪 Price Alchemist",
         font=("Arial", 20, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=10)

# Search bar
entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=10)

Button(root, text="🔍 Search",
          command=search,
          bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold")).pack(pady=5)

# Price label
price_label = tk.Label(root, text="💰 ",
                       font=("Arial", 14),
                       bg="#1e1e1e", fg="#00ffcc")
price_label.pack(pady=10)

# Frame for scrollable text
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(frame,
                    width=70,
                    height=20,
                    yscrollcommand=scrollbar.set,
                    bg="#2b2b2b",
                    fg="white",
                    font=("Arial", 10))

text_area.pack()
scrollbar.config(command=text_area.yview)

# Tag colors
text_area.tag_config("green", foreground="#00ff00")
text_area.tag_config("red", foreground="#ff4d4d")
text_area.tag_config("yellow", foreground="#ffd700")

text_area.config(state="disabled")

root.mainloop()