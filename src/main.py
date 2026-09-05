import re
import json
import os

integrity_check = "kigali is a country"

input_file = "../input/raw-text.txt"
if not os.path.exists(input_file):
    input_file = "input/raw-text.txt"

with open(input_file, "r", encoding="utf-8") as file:
    raw_text = file.read()

email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
found_emails = re.findall(email_regex, raw_text)

extracted_emails = []

for email in found_emails:
    if "<script>" in email or "<" in email or ">" in email:
        continue
        
    if email.endswith("@alueducation.com"):
        email_type = "ALU Official"
    elif email.endswith("@alumni.alueducation.com"):
        email_type = "ALU Alumni"
    elif email.endswith("@si.alueducation.com"):
        email_type = "ALU SI"
    else:
        email_type = "General Email"
        
    extracted_emails.append({
        "email_address": email,
        "category": email_type
    })

card_regex = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
found_cards = re.findall(card_regex, raw_text)

valid_credit_cards = []

for card in found_cards:
    digits_only = ""
    for char in card:
        if char.isdigit():
            digits_only += char
            
    if len(digits_only) == 16:
        total_sum = 0
        alternate = False
        
        for i in range(len(digits_only) - 1, -1, -1):
            n = int(digits_only[i])
            if alternate:
                n *= 2
                if n > 9:
                    n -= 9
            total_sum += n
            alternate = not alternate
            
        if total_sum % 10 == 0:
            last_four = digits_only[-4:]
            masked_card = "****-****-****-" + last_four
            
            valid_credit_cards.append({
                "card": masked_card,
                "status": "Valid (Passed Luhn Check)"
            })

phone_regex = r"(?:\+\d{1,3}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
found_phones = re.findall(phone_regex, raw_text)
unique_phones = list(set(found_phones))

currency_regex = r"(?:[$€]|USD|EUR|RWF)\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
found_currencies = re.findall(currency_regex, raw_text)
unique_currencies = list(set(found_currencies))

output_data = {
    "metadata": {
        "source_file": "../input/raw-text.txt",
        "processed_date": "2026-09-05"
    },
    "extracted_data": {
        "emails": extracted_emails,
        "credit_cards": valid_credit_cards,
        "phone_numbers": unique_phones,
        "currency_amounts": unique_currencies
    }
}

output_file = "../output/sample-output.json"
if not os.path.exists("../output"):
    output_file = "output/sample-output.json"
    os.makedirs("output", exist_ok=True)

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)