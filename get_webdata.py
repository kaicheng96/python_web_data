import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from datetime import datetime

def scrape_video():
    # Get the URL from the input field
    url = url_entry.get()

    # Configure Chrome driver
    service = ChromeService(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Visit the target URL
        driver.get(url)
        time.sleep(5)

        # Get page content
        html_content = driver.page_source

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        video_element = soup.find('video')
        video_download = video_element["src"]

        # Download video
        response = requests.get(video_download, stream=True)

        # Check if request is successful
        if response.status_code == 200:
            # Generate filename based on current time
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_{current_time}.mp4"
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            messagebox.showinfo("Success", "成功下载!")
        else:
            messagebox.showerror("Error", "下载失败.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        driver.quit()

# Create tkinter window
window = tk.Tk()
window.title("www.zhibo8.com视频下载器")

# Label and Entry for URL input
url_label = tk.Label(window, text="网址:")
url_label.pack(pady=5)
url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=5)

# Button to trigger web scraping
scrape_button = tk.Button(window, text="运行", command=scrape_video)
scrape_button.pack(pady=10)

# Run tkinter event loop
window.mainloop()
