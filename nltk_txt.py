import streamlit as st
import nltk
nltk.download('punkt', download_dir='nltk_data', force=True)
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import fitz  # PyMuPDF
import docx

# Streamlit app title
st.title('NLTK Text Summarizer')
st.write("Created By Ansh Varshney")
# Downloading NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    fullText = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(fullText)

# File upload option
uploaded_file = st.file_uploader("Upload Files", type=['pdf', 'txt', 'docx'])
file_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        file_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        file_text = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        file_text = extract_text_from_docx(uploaded_file)

# Text area for direct input (prefilled with file_text if a file is uploaded)
user_input_text = st.text_area("Enter Text", file_text if file_text else "Natural language processing enables computers to understand human language. This technology is behind voice-activated assistants, online customer support, and more.", height=300)

# Slider for selecting the number of sentences in the summary
num_sentences = st.slider("Select the number of sentences for the summary:", 1, 10, 2)

def summarize_text(text, num_sentences):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Find synsets and basic sentence scoring based on word frequency
    word_scores = {}
    for word in filtered_words:
        synsets = wn.synsets(word)
        if synsets:
            word_scores[word] = len(synsets)

    # Simple scoring for demonstration purposes
    sentence_scores = {}
    for sentence in sent_tokenize(text):
        sentence_scores[sentence] = sum(word_scores.get(word, 0) for word in word_tokenize(sentence))

    # Sort sentences by score and select top sentences for summary
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = ' '.join(sorted_sentences[:num_sentences])
    return summary

if st.button('Summarize'):
    summary_result = summarize_text(user_input_text, num_sentences)
    st.write(summary_result)
