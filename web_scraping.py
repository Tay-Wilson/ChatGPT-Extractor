# web_scraping.py
import time
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from utils import add_to_history, update_history_sidebar

class WebScraper:
    def __init__(self):
        pass
    
    # Fetch conversations
    def fetch_conversations(self, url_entry, driver, conversation_text, auto_analyze, logger, texts, current_language):
        try:
            shared_link = url_entry.get()

            driver.get(shared_link)

            time.sleep(5)

            html_content = driver.page_source

            soup = BeautifulSoup(html_content, 'html.parser')

            title_elem = soup.find('h1', class_='text-3xl font-semibold leading-tight text-token-text-primary sm:text-4xl')
            title = title_elem.get_text().strip() if title_elem else "未找到标题"
            
            date_elem = soup.find('div', class_='pt-3 text-base text-gray-400 sm:pt-4')
            date = date_elem.get_text().strip() if date_elem else "未找到日期"

            messages = soup.find_all('div', class_='w-full text-token-text-primary')

            conversations = []

            for message in messages:
                speaker_name_elem = message.find('div', class_='font-semibold select-none')
                speaker_name = speaker_name_elem.get_text().strip() if speaker_name_elem else "Anonymous"

                content_elem = message.find(['div', 'p'])
                if content_elem:
                    content = content_elem.get_text().strip()
                    if content:
                        if content.startswith(speaker_name):
                            content = content[len(speaker_name):].strip()
                        if content.startswith("ChatGPT"):
                            content = content.replace("ChatGPT", "").strip()
                        conversations.append((speaker_name, content))

            if conversations:
                conversation_text.config(state=tk.NORMAL)
                conversation_text.delete("1.0", tk.END)
                conversation_text.insert(tk.END, f"标题: {title}\n日期: {date}\n\n")
                for role, content in conversations:
                    conversation_text.insert(tk.END, f"{role}: {content}\n")
                conversation_text.config(state=tk.DISABLED)
                
                if auto_analyze:
                    full_conversation_text = '\n'.join([f"{role}: {content}" for role, content in conversations])
                    self.analyze_conversations(full_conversation_text)

                return title, shared_link, '\n'.join([f"{role}: {content}" for role, content in conversations])  # 返回对话详情

            else:
                messagebox.showwarning(texts[current_language]["warning_title"], texts[current_language]["warning_message"])
                return None

        except Exception as e:
            logger.error("Error fetching conversations: %s", e)
            messagebox.showwarning(texts[current_language]["warning_title"], texts[current_language]["warning_message"])
            return None
