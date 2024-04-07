import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from collections import Counter
import re
import jieba.analyse
import logging
from langdetect import detect

# Initialize logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Define logger
logger = logging.getLogger(__name__)

# Define language detection functions
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def is_chinese(text):
    try:
        return detect(text) == 'zh-cn' or detect(text) == 'zh-tw'
    except:
        return False

# Set default language
current_language = "chinese"
auto_analyze = False

# Define text labels for English and Chinese
texts = {
    "english": {
        "window_title": "ChatGPT Conversation Extractor",
        "url_label": "Enter ChatGPT shared link:",
        "fetch_button": "Fetch Conversations",
        "save_button": "Save Conversation",
        "analyze_button": "Analyze Conversation",
        "conversation_text": "Conversation Text:",
        "warning_title": "Warning",
        "warning_message": "Unable to extract conversation.",
        "closing_message": "Are you sure you want to exit?",
        "language_button": "Switch Language",
        "highlight_label": "Enter Keywords to Highlight (comma-separated):",
        "highlight_button": "Highlight Keywords",
        "speaker_counts_label": "Speaker Counts (English):",
        "word_counts_label_english": "Most Common Words (English):",
        "word_counts_label_chinese": "Most Common Words (Chinese):"
    },
    "chinese": {
        "window_title": "ChatGPT 对话提取器",
        "url_label": "请输入 ChatGPT 的共享链接:",
        "fetch_button": "提取对话",
        "save_button": "保存对话记录",
        "analyze_button": "分析对话",
        "conversation_text": "对话记录:",
        "warning_title": "警告",
        "warning_message": "无法提取对话记录。",
        "closing_message": "确定要退出吗？",
        "language_button": "切换语言",
        "highlight_label": "输入要高亮显示的关键词（逗号分隔）:",
        "highlight_button": "高亮显示关键词",
        "speaker_counts_label": "发言次数统计 (中文):",
        "word_counts_label_english": "最常见的词语统计 (英文):",
        "word_counts_label_chinese": "最常见的词语统计 (中文):"
    }
}

# Initialize Selenium WebDriver
def initialize_driver():
    chrome_service = Service("C:/Users/Admin/Desktop/chromedriver-win64/chromedriver.exe")
    chrome_service.start()
    driver = webdriver.Chrome(service=chrome_service)
    return driver

driver = initialize_driver()

# Fetch conversations
def fetch_conversations():
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
            analyze_conversations(full_conversation_text)

    else:
        messagebox.showwarning(texts[current_language]["warning_title"], texts[current_language]["warning_message"])

# Save conversations
def save_conversations():
    conversation_record = conversation_text.get("1.0", tk.END)

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(conversation_record)
        messagebox.showinfo("保存成功", "对话记录已成功保存。")
    else:
        messagebox.showwarning("保存取消", "未保存对话记录。")

# Analyze conversations
def analyze_conversations(conversation_record):
    languages = detect_language(conversation_record)

    if "english" in languages:
        logging.info("English conversation detected.")
        analyze_english_conversations(conversation_record)
    
    if "chinese" in languages:
        logging.info("Chinese conversation detected.")
        analyze_chinese_conversations(conversation_record)

# Language detection function
def detect_language(text):
    is_ascii = any(ord(char) < 128 for char in text)
    is_chinese = any(0x4e00 <= ord(char) <= 0x9fff for char in text)
    
    languages = []
    if is_ascii:
        languages.append("english")
    if is_chinese:
        languages.append("chinese")
    
    return languages

# Analyze English conversations
def analyze_english_conversations(conversation_record):
    speakers = []
    words = []
    for line in conversation_record.split("\n"):
        if line.strip() and ":" in line:
            speaker, content = line.split(":", 1)
            speakers.append(speaker.strip())
            words.extend(content.strip().split())
    speaker_counts = Counter(speakers)
    english_words = [word for word in words if all(ord(char) < 128 for char in word)]
    word_counts = Counter(english_words)

    display_analysis_results("english", speaker_counts, word_counts)

    logging.info("Analyzing English conversation...")
    logging.info("Speaker counts: %s", speaker_counts)
    logging.info("Word counts: %s", word_counts)

# Analyze Chinese conversations
def analyze_chinese_conversations(conversation_record):
    words = jieba.cut(conversation_record)
    punctuation = set(':！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.')
    stopwords = set()
    filtered_words = [word for word in words if word not in punctuation and word not in stopwords and word.strip()]
    word_counts = Counter(filtered_words)

    display_analysis_results("chinese", None, word_counts)

    logging.info("Analyzing Chinese conversation...")
    logging.info("Word counts: %s", word_counts)


ANALYSIS_WINDOW_WIDTH=600
ANALYSIS_WINDOW_HEIGHT=300

# Fetch and analyze conversations
def fetch_and_analyze_conversations():
    fetch_conversations()
    conversation_record = conversation_text.get("1.0", tk.END)
    analyze_conversations(conversation_record)

# Display analysis results
def display_analysis_results(language, speaker_counts=None, word_counts=None):
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Conversation Analysis")
    analysis_window.geometry(f"{ANALYSIS_WINDOW_WIDTH}x{ANALYSIS_WINDOW_HEIGHT}")
    
    if speaker_counts:
        speaker_label = tk.Label(analysis_window, text=f"Speaker Counts ({language.capitalize()}):")
        speaker_label.pack()
        for speaker, count in speaker_counts.items():
            speaker_info = f"{speaker}: {count} times"
            speaker_info_label = tk.Label(analysis_window, text=speaker_info)
            speaker_info_label.pack()

    if word_counts:
        if language == "english":
            word_label = tk.Label(analysis_window, text=texts[current_language]["word_counts_label_english"])
        else:
            word_label = tk.Label(analysis_window, text=texts[current_language]["word_counts_label_chinese"])
        word_label.pack()
        for word, count in word_counts.most_common(5):
            word_info = f"{word}: {count} times"
            word_info_label = tk.Label(analysis_window, text=word_info)
            word_info_label.pack()

# Create the main window
root = tk.Tk()
root.title(texts[current_language]["window_title"])

# Create labels, entry, and buttons
url_label = tk.Label(root, text=texts[current_language]["url_label"])
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

fetch_button = tk.Button(root, text=texts[current_language]["fetch_button"], command=fetch_and_analyze_conversations)
fetch_button.pack()

save_button = tk.Button(root, text=texts[current_language]["save_button"], command=save_conversations)
save_button.pack()

analyze_button = tk.Button(root, text=texts[current_language]["analyze_button"], command=fetch_and_analyze_conversations)
analyze_button.pack()

conversation_text = tk.Text(root, width=80, height=20)
conversation_text.pack()
conversation_text.config(state=tk.DISABLED)

# Create the language switch button
def change_language():
    global current_language
    if current_language == "english":
        current_language = "chinese"
    else:
        current_language = "english"
    # Update all text in the window
    root.title(texts[current_language]["window_title"])
    url_label.config(text=texts[current_language]["url_label"])
    fetch_button.config(text=texts[current_language]["fetch_button"])
    save_button.config(text=texts[current_language]["save_button"])
    analyze_button.config(text=texts[current_language]["analyze_button"])

language_button = tk.Button(root, text=texts[current_language]["language_button"], command=change_language)
language_button.pack()

# Close WebDriver when closing the window
def on_closing():
    if messagebox.askyesno(texts[current_language]["warning_title"], texts[current_language]["closing_message"]):
        driver.quit()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
