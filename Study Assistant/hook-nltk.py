# PyInstaller hook for NLTK to fix scipy.stats import issue
import sys
import os

# Fix the scipy.stats import issue by importing before NLTK
try:
    import scipy.stats
except ImportError:
    pass

# Add NLTK data path
nltk_data_path = os.path.join(sys._MEIPASS, 'nltk_data')
if nltk_data_path not in sys.path:
    sys.path.insert(0, nltk_data_path)

# Import NLTK after scipy is loaded
import nltk
