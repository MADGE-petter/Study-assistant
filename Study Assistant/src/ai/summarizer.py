import logging
import nltk
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class TextSummarizer:
    def __init__(self, language="english"): 
        self.language = language
        self.tokenizer = None
        self.stemmer = None
        self.summarizer = None
        self.is_ready = (
            False  
        )

        try:
            
            nltk.data.find(f"tokenizers/punkt")
            nltk.data.find(f"corpora/stopwords")
            self.tokenizer = Tokenizer("english")
            self.summarizer = LsaSummarizer()
            self.summarizer.stop_words = get_stop_words("english")
            self.is_ready = True
            logging.info(
                f"TextSummarizer initialized successfully for language: {language}"
            )
        except LookupError as e:
            logging.error(
                f"Error initializing TextSummarizer for language '{language}': NLTK resources might be missing."
            )
            logging.error(
                "Please ensure 'punkt' and 'stopwords' are downloaded manually."
            )
            logging.error("If using Vietnamese, 'punkt_tab' is also required.")
            logging.error(
                "Run the following command in your terminal: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')\""
            )
        except Exception as e:
            logging.error(
                f"An unexpected error occurred during TextSummarizer initialization: {e}"
            )

    def summarize_text(self, text, sentences_count=5):
        """
        Tóm tắt văn bản đã cho bằng thuật toán LSA.

        Args:
            text (str): Văn bản cần tóm tắt.
            sentences_count (int): Số lượng câu muốn có trong bản tóm tắt.

        Returns:
            str: Bản tóm tắt của văn bản hoặc thông báo lỗi.
        """
        if not self.is_ready:
            return "Chức năng tóm tắt không khả dụng do lỗi khởi tạo."

        if not text or not text.strip():
            return "Không có nội dung để tóm tắt."

        try:
            parser = PlaintextParser.from_string(text, self.tokenizer)
            summary = self.summarizer(parser.document, sentences_count)
            return "\n".join(str(sentence) for sentence in summary)
        except Exception as e:
            logging.error(f"Error during text summarization: {e}")
            return "Đã xảy ra lỗi khi tóm tắt văn bản này."
