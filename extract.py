import google.generativeai as genai
from PIL import Image
import os
import re

# Set your Google API key
os.environ['GOOGLE_API_KEY'] = 'Google api'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_information(text):
    parsed_data = {
        "Name": "",
        "Father's Name": "",
        "CNIC/B.Form No": "",
        "Domicile": "",
        "Phone No": "",
        "Form No": "",
        "Gender": "",
        "Address": "",
        "City": "",
        "Postal Code": "",
        "Category":"",
        "Choice of Subject": "",
        'Department': '',
        'Reg #': ''
    }

    # Updated regex patterns for each field
    patterns = {
        "Name": re.compile(r"Name:\s*([A-Za-z\s]+)(?=\n)"),
        "Father's Name": re.compile(r"Father Name:\s*([A-Za-z\s]+)(?=\n)"),
        "CNIC/B.Form No": re.compile(r"National Identity Card No./Form-B:\s*(\d{13})"),
        "Domicile": re.compile(r"Domicile:\s*([A-Za-z\s]+)(?=\n)"),
        "Phone No": re.compile(r"Phone No:\s*([\d-]+)(?=\n)"),
        "Form No": re.compile(r"Form No:\s*([\w\-]*)\n"),  # Handle missing Form No
        "Gender": re.compile(r"Gender:\s*([A-Za-z]+)(?=\n)"),
        "Address": re.compile(r"Address:\s*(.+?)(?=\nCity:)", re.DOTALL),  # Multi-line address
        "City": re.compile(r"City:\s*([A-Za-z\s]+)(?=\n)"),
        "Category": re.compile(r"Category:\s*([A-Za-z\s]+)(?=\n)"),
        "Postal Code": re.compile(r"Postal Code:\s*(\d{5})(?=\n)"),
        "Choice of Subject": re.compile(r"Choice of Subject:\s*([A-Za-z\s\(\),]+)(?=\n)"),
        'Department': re.compile(r"Department:\s*([A-Za-z\s]+)(?=\n)"),
        'Reg #': re.compile(r"Reg #:\s*([A-Za-z0-9\-]+)(?=\n)")
    }


    # Extract information based on the regular expressions
    for key, pattern in patterns.items():
        match = pattern.search(text)
        if match:
            parsed_data[key] = match.group(1).strip()
    if not parsed_data['Reg #']:
        reg_no =  re.search(r"Form No.:\s*([A-Za-z0-9\-]+)(?=\n)", text)
        if reg_no:
            parsed_data['Reg #'] = reg_no.group(1).strip()
    # Check for CNIC with two patterns
    if not parsed_data["CNIC/B.Form No"]:
        cn_value = re.search(r"CNIC:\s*(\d{13})", text)
        if cn_value:
            parsed_data["CNIC/B.Form No"] = cn_value.group(1).strip()
        else:
            # If CNIC is not found, try to find National Identity Card No./Form-B
            cn_value = re.search(r"National Identity Card No./Form-B:\s*([\d\w\-]+)", text)
            if cn_value:
                parsed_data["CNIC/B.Form No"] = cn_value.group(1).strip()


    return parsed_data

def extract_text_from_image(img):
    # Generate content from the image using the new model
    response = model.generate_content(["Extract all text from image, and split it in new line. Like name and gender comes in different line. remove unnecessary spaces, and rearrange in format like CNIC: ****, Name: ****. Ensure that all information is captured carefully including Form No. and Category, Name, Father Name, Choice of Subject, Domicile, Phone No,Address, City, Postal Code", img])
    print(response)
    if hasattr(response, 'text'):
        # Extracted text from the image
        extracted_text = response.text
        
        # Remove bold indicators
        cleaned_text = extracted_text.replace("*", "")
        cleaned_text = extracted_text.replace("-", "")
        
        # Parse the relevant information
        extracted_info = parse_information(cleaned_text)

        return extracted_info
