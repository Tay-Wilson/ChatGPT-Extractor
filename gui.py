# gui.py
import tkinter as tk
from tkinter import messagebox, filedialog
from utils import add_to_history, update_history_sidebar

class GUI:
    def __init__(self, texts, current_language, fetch_callback, save_callback, analyze_callback, clear_callback, change_language_callback):
        self.texts = texts
        self.current_language = current_language
        self.fetch_callback = fetch_callback
        self.save_callback = save_callback
        self.analyze_callback = analyze_callback
        self.clear_callback = clear_callback
        self.change_language_callback = change_language_callback

        self.root = tk.Tk()
        self.root.title(self.texts[self.current_language]["window_title"])

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        url_label = tk.Label(self.root, text=self.texts[self.current_language]["url_label"])
        url_label.pack()

        url_entry = tk.Entry(self.root, width=50)
        url_entry.pack()

        fetch_button = tk.Button(self.root, text=self.texts[self.current_language]["fetch_button"], command=self.fetch_callback)
        fetch_button.pack()

        save_button = tk.Button(self.root, text=self.texts[self.current_language]["save_button"], command=self.save_callback)
        save_button.pack()

        analyze_button = tk.Button(self.root, text=self.texts[self.current_language]["analyze_button"], command=self.analyze_callback)
        analyze_button.pack()

        clear_button = tk.Button(self.root, text=self.texts[self.current_language]["clear_button"], command=self.clear_callback)
        clear_button.pack()

        language_button = tk.Button(self.root, text=self.texts[self.current_language]["language_button"], command=self.change_language_callback)
        language_button.pack()

        conversation_text = tk.Text(self.root, width=80, height=20)
        conversation_text.pack()
        conversation_text.config(state=tk.DISABLED)

    # 添加设置回调函数的方法
    def set_fetch_callback(self, fetch_callback):
        self.fetch_callback = fetch_callback

    def set_save_callback(self, save_callback):
        self.save_callback = save_callback

    def set_analyze_callback(self, analyze_callback):
        self.analyze_callback = analyze_callback

    def set_clear_callback(self, clear_callback):
        self.clear_callback = clear_callback

    def set_change_language_callback(self, change_language_callback):
        self.change_language_callback = change_language_callback

    def update_conversation_text(self, conversation_text):
        # 实现更新对话文本的方法
        pass

    def save_conversations(self):
        # 实现保存对话记录的方法
        pass

    def display_analysis_results(self, speaker_counts, word_counts):
        # 实现显示分析结果的方法
        pass

    def run(self):
        self.root.mainloop()
