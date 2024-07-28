# Install the required packages
!pip install fitz
!pip install PyMuPDF
!pip install pdfplumber
!pip install --upgrade pymupdf

import fitz  # PyMuPDF
import pdfplumber
import re
import random
import os

def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove non-printable characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

class AuroraChatbot:
    def __init__(self, book_content):
        self.book_content = book_content
    
    def detect_suicidal_thoughts(self, message):
        # Simplified logic for detecting suicidal thoughts
        suicidal_keywords = ['suicide', 'end my life', 'kill myself', 'not worth living']
        return any(keyword in message.lower() for keyword in suicidal_keywords)
    
    def get_advice_from_book(self):
        # Randomly sample a section from the book for advice
        sentences = self.book_content.split('.')
        advice = random.choice(sentences).strip()
        return advice
    
    def respond(self, user_message):
        if self.detect_suicidal_thoughts(user_message):
            advice = self.get_advice_from_book()
            return (f"It sounds like you're going through a tough time. "
                    f"Here's something that might help: {advice}. "
                    f"Please consider talking to a professional.")
        else:
            return "I'm here to help you. Tell me more about what's going on."

# File path to the PDF
pdf_path = '/content/symptoms_and_remedies.pdf'

# Extract and preprocess the text
try:
    book_text = extract_text_from_pdf(pdf_path)
    cleaned_text = preprocess_text(book_text)

    # Initialize the chatbot with the cleaned book content
    aurora = AuroraChatbot(cleaned_text)

    # Example usage
    user_message = "I feel like there's no point in living anymore."
    response = aurora.respond(user_message)
    print(response)

except FileNotFoundError as e:
    print(e)
