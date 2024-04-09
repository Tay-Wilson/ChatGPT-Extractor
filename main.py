#main.py
import tkinter as tk
from tkinter import Text  # 添加对 Text 组件的导入
from tkinter import messagebox, filedialog
from gui import GUI
from data_processing import DataProcessor
from web_scraping import WebScraper
# 在适当的位置导入或定义所需的模块和变量
from selenium import webdriver  # 导入 Selenium Webdriver
from tkinter import Entry  # 导入 Tkinter 的 Entry 组件
# 创建 Tkinter 根窗口
root = tk.Tk()  # 在此处创建根窗口
# 假设您正在使用 Selenium 创建一个 Chrome WebDriver 实例
driver = webdriver.Chrome()

# 假设您的 UI 中有一个名为 url_entry 的 Entry 组件用于输入网址
url_entry = Entry(root)  # 这里的 root 是您 Tkinter 应用程序的根窗口

# 假设您有一个名为 conversation_text 的 Text 组件用于显示对话内容
conversation_text = Text(root)  # 这里的 root 是您 Tkinter 应用程序的根窗口

# 定义一个变量来控制是否自动分析对话
auto_analyze = True

# 假设您已经配置了日志记录器（logger）
import logging
logger = logging.getLogger(__name__)

current_language="chinese"

# Define GUI texts
texts = {
    "english": {
        "window_title": "ChatGPT Conversation Extractor",
        "url_label": "Enter ChatGPT shared link:",
        "fetch_button": "Fetch Conversations",
        "save_button": "Save Conversation",
        "analyze_button": "Analyze Conversation",
        "clear_button": "Clear History",
        "conversation_text": "Conversation Text:",
        "conversation_history_label": "Conversation History",
        "warning_title": "Warning",
        "warning_message": "Unable to extract conversation.",
        "closing_message": "Are you sure you want to exit?",
        "language_button": "Switch Language",
        "highlight_label": "Enter Keywords to Highlight (comma-separated):",
        "highlight_button": "Highlight Keywords",
        "speaker_counts_label": "Speaker Counts (English):",
        "word_counts_label": "Most Common Words (English):"
    },
    "chinese": {
        "window_title": "ChatGPT 对话提取器",
        "url_label": "请输入 ChatGPT 的共享链接:",
        "fetch_button": "提取对话",
        "save_button": "保存对话记录",
        "analyze_button": "分析对话",
        "clear_button": "清除历史记录",
        "conversation_text": "对话记录:",
        "conversation_history_label": "对话历史记录",
        "warning_title": "警告",
        "warning_message": "无法提取对话记录。",
        "closing_message": "确定要退出吗？",
        "language_button": "切换语言",
        "highlight_label": "输入要高亮显示的关键词（逗号分隔）:",
        "highlight_button": "高亮显示关键词",
        "speaker_counts_label": "发言次数统计 (中文):",
        "word_counts_label": "最常见的词语统计 (中文):"
    }
}


# Define the callback functions for interacting with the GUI
# 在 main.py 中调用 fetch_conversations 方法时，确保传递所需的参数
def fetch_conversations():
    # 创建 WebScraper 实例
    scraper = WebScraper()

    # 在调用 fetch_conversations 方法时传递所需的参数
    conversation_record = scraper.fetch_conversations(url_entry, driver, conversation_text, auto_analyze, logger, texts, current_language)


def save_conversations():
    # Call the method to save conversations from the MainWindow instance
    main_window.save_conversations()

def analyze_conversations():
    # Call the method to analyze conversations from the DataProcessor instance
    speaker_counts, word_counts = processor.analyze_conversations(main_window.get_conversation_text())
    # Call the method to display analysis results in the GUI
    main_window.display_analysis_results(speaker_counts, word_counts)



# Pass the 'texts' variable to GUI constructor
main_window = GUI(texts, current_language, fetch_conversations, save_conversations, analyze_conversations, None, None)

processor = DataProcessor()
scraper = WebScraper()

# Set the callback functions for the GUI buttons
main_window.set_fetch_callback(fetch_conversations)
main_window.set_save_callback(save_conversations)
main_window.set_analyze_callback(analyze_conversations)


# Run the application
root.mainloop()
