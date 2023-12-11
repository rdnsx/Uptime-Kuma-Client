import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import font
import subprocess
import requests
import threading
import time
import datetime
import json
import socket
import webbrowser


def get_default_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"

def save_config():
    config = {"ip_address": ip_address.get(), "url": url.get()}
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            ip_address.set(config.get("ip_address", get_default_ip()))
            url.set(config.get("url", ""))
    except FileNotFoundError:
        ip_address.set(get_default_ip())
        url.set("")

def monitor_ip():
    while monitoring:
        response = subprocess.run(["ping", "-c", "1", ip_address.get()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            try:
                requests.get(url.get())
            except requests.RequestException as e:
                print("Error making request:", e)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not online_time.get():
                online_time.set(current_time)
            offline_time.set("")
        else:
            if not offline_time.get() and online_time.get():
                offline_time.set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(30)

def update_button_color(button, color):
    def change_color():
        button.config(bg=color)
    root.after(0, change_color)

def start_monitoring():
    global monitoring
    if not ip_address.get() or not url.get():
        messagebox.showerror("Error", "Please enter both IP address and URL.")
        return
    save_config()
    monitoring = True
    update_button_color(start_button, "green")
    update_button_color(stop_button, "systemButtonFace")
    monitor_thread = threading.Thread(target=monitor_ip, daemon=True)
    monitor_thread.start()

def stop_monitoring():
    global monitoring
    monitoring = False
    update_button_color(stop_button, "red")
    update_button_color(start_button, "systemButtonFace")
    online_time.set("")
    offline_time.set("")

def open_url():
    webbrowser.open("https://github.com/rdnsx/RDNSX-IPmon-for-Mac")

def on_enter(event):
    event.widget.config(fg="orange", cursor="hand2")

def on_leave(event):
    event.widget.config(fg="white")

# GUI Setup
root = tk.Tk()
root.title("Uptime Kuma Client")

# Load and display the logo
logo = PhotoImage(file="uptimekuma.png")
logo_label = tk.Label(root, image=logo)
logo_label.pack(side="top", pady=10)

# Variables
monitoring = False
ip_address = tk.StringVar()
url = tk.StringVar()
online_time = tk.StringVar()
offline_time = tk.StringVar()

load_config()

# Input fields
tk.Label(root, text="IP Address:").pack()
ip_entry = tk.Entry(root, textvariable=ip_address)
ip_entry.pack()

tk.Label(root, text="URL:").pack()
url_entry = tk.Entry(root, textvariable=url)
url_entry.pack()

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.pack()

stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring)
stop_button.pack()

# Display areas
tk.Label(root, text="Online Since:").pack()
tk.Label(root, textvariable=online_time).pack()

tk.Label(root, text="Offline Since:").pack()
tk.Label(root, textvariable=offline_time).pack()

# Footer Frame
footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=10)

# Custom smaller font for footer
footer_font = font.Font(size=10)  # Adjust the size as needed

# Footer Label
footer_label = tk.Label(footer_frame, text="Built with ❤️ by ", font=footer_font)
footer_label.pack(side="left")

# Clickable Link Label
link_label = tk.Label(footer_frame, text="RDNSX", font=footer_font)
link_label.pack(side="left")
link_label.bind("<Button-1>", open_url)
link_label.bind("<Enter>", on_enter)
link_label.bind("<Leave>", on_leave)

root.mainloop()
