import os
import re
import pandas as pd
import pdfplumber


def extract_information_from_cv(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        email = ""
        phone = ""
        for page in pdf.pages:
            text += page.extract_text()
        # Extract email using regular expression
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            email = email_match.group(0)
        # Extract phone number using regular expression
        phone_match = re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
        if phone_match:
            phone = phone_match.group(0)
    return {'Email': email, 'Phone': phone, 'Text': text}


def process_cv_directory(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            cv_info = extract_information_from_cv(pdf_path)
            data.append(cv_info)
    return data


def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)


if __name__ == "__main__":
    input_directory = "/Users/swarnaghanty/Library/Mobile Documents/com~apple~CloudDocs/cvs pdf"
    output_excel_file = "output_file.xlsx"

    cv_data = process_cv_directory(input_directory)
    save_to_excel(cv_data, output_excel_file)
