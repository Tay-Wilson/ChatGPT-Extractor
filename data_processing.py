#data_processing.py
from collections import Counter
import jieba.analyse
import langid

class DataProcessor:
    @staticmethod
    def detect_language(text):
        try:
            return langid.classify(text)[0]
        except:
            return "unknown"

    @staticmethod
    def analyze_conversations(conversation_record):
        # Implement conversation analysis logic here
        pass
