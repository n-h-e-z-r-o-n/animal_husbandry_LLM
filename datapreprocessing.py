import os
import pdfplumber
import re


def extract_text_from_pdf(pdf_file_path):
    """Extract text from a PDF file."""
    text = ''
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def clean_text(text):
    """Clean and format text."""
    # Remove extra whitespaces, newlines, and tabs
    cleaned_text = re.sub(r'\s+', ' ', text)
    # Remove special characters and non-printable characters
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
    # Remove multiple spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()


def save_text_to_file(text, output_file):
    """Save text to a file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)


def process_pdf_files(input_dir, output_file):
    """Process PDF files in the input directory and save cleaned text to a single file."""
    pdf_files = [file for file in os.listdir(input_dir) if file.endswith('.pdf')]
    all_text = ''
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(text)
        all_text += cleaned_text + '\n\n'  # Add a newline between texts of different PDFs
    save_text_to_file(all_text, output_file)
    print(f"Cleaned text saved to {output_file}")


if __name__ == "__main__":
    input_dir = "C:\Year4\CSC 418 Emerging tech\data"
    output_file = "C:\Year4\CSC 418 Emerging tech\data\output.txt"
    process_pdf_files(input_dir, output_file)
