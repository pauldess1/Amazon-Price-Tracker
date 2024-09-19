import tkinter as tk
from tkinter import messagebox
import threading
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

class Alert:
    def __init__(self, url, user, receiver, password, threshold, interval):
        self.url = url
        self.user = user
        self.receiver = receiver
        self.password = password
        self.headers = HEADERS
        self.threshold = threshold
        self.interval = interval

    def get_title(self, soup):
        title_tag = soup.find(id='productTitle')
        if title_tag:
            return title_tag.get_text().strip()
        else:
            raise ValueError("Title element not found")

    def get_price(self, soup):
        price_int_tag = soup.find("span", class_="a-price-whole")
        price_fract_tag = soup.find("span", class_="a-price-fraction")
        if price_int_tag and price_fract_tag:
            price_int = self.str_to_int(price_int_tag.get_text())
            price_fract = self.str_to_int(price_fract_tag.get_text().zfill(2))
            return price_int + 0.01 * price_fract
        else:
            raise ValueError("Price element(s) not found")

    def str_to_int(self, string):
        return int(''.join(filter(str.isdigit, string)))

    def check_price(self):
        try:
            page = requests.get(self.url, headers=self.headers)
            page.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(page.content, 'html.parser')
            title = self.get_title(soup)
            price = self.get_price(soup)
            if price < self.threshold:
                self.send_mail(price, title, self.url)
        except Exception as e:
            print(f'Failed to check price: {e}')

    def send_mail(self, price, title, url):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        try:
            server.login(user=self.user, password=self.password)

            msg = MIMEMultipart('alternative')
            msg['From'] = self.user
            msg['To'] = self.receiver
            msg['Subject'] = 'Price Drop Alert'

            html_body = self.generate_html_body(price, title, url)
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            server.sendmail(self.user, self.receiver, msg.as_string())
            print(f'EMAIL HAS BEEN SENT FOR {title}!')

        except Exception as e:
            print(f'Failed to send email: {e}')

        finally:
            server.quit()

    def generate_html_body(self, price, title, url):
        return f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                h1 {{
                    font-size: 22px;
                    color: #333;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .price {{
                    font-size: 24px;
                    color: #333;
                    font-weight: bold;
                }}
                a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Price Drop Alert</h1>
                <p>The price of your item <strong>"{title}"</strong> has dropped to <span class="price">{price}€</span>.</p>
                <p>Check out the updated price here: <a href="{url}">{url}</a></p>
                <p>Best regards,<br>Your Price Tracker</p>
            </div>
        </body>
        </html>
        """

    def run(self):
        while True:
            self.check_price()
            time.sleep(self.interval)

class AlertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amazon Price Alert Manager")

        self.alerts = []

        # Labels and Entries for URL, Threshold, etc.
        tk.Label(root, text="Product URL:").grid(row=0, column=0)
        tk.Label(root, text="Email:").grid(row=1, column=0)
        tk.Label(root, text="Receiver:").grid(row=2, column=0)
        tk.Label(root, text="Password:").grid(row=3, column=0)
        tk.Label(root, text="Threshold (€):").grid(row=4, column=0)
        tk.Label(root, text="Interval (seconds):").grid(row=5, column=0)

        self.url_entry = tk.Entry(root)
        self.user_entry = tk.Entry(root)
        self.receiver_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show='*')
        self.threshold_entry = tk.Entry(root)
        self.interval_entry = tk.Entry(root)

        self.url_entry.grid(row=0, column=1)
        self.user_entry.grid(row=1, column=1)
        self.receiver_entry.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)
        self.threshold_entry.grid(row=4, column=1)
        self.interval_entry.grid(row=5, column=1)

        tk.Button(root, text="Add Alert", command=self.add_alert).grid(row=6, column=0, columnspan=2)

    def add_alert(self):
        url = self.url_entry.get()
        user = self.user_entry.get()
        receiver = self.receiver_entry.get()
        password = self.password_entry.get()
        try:
            threshold = float(self.threshold_entry.get())
            interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for threshold and interval.")
            return

        alert = Alert(url, user, receiver, password, threshold, interval)
        self.alerts.append(alert)
        threading.Thread(target=alert.run, daemon=True).start()
        messagebox.showinfo("Alert Added", "The alert has been added and is now running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlertApp(root)
    root.mainloop()