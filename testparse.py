import re
from bs4 import BeautifulSoup

def clean_html(raw_html):
    """Remove HTML tags from raw content."""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def remove_urls(text):
    """Remove URLs from the email content."""
    return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

def remove_dates(text):
    """Remove date information from the email."""
    return re.sub(r'(\b[A-Za-z]+,? \d{1,2},? \d{4}\b)|(\d{1,2}:\d{2}:\d{2} (AM|PM))', '', text)

def remove_email_addresses(text):
    """Remove email addresses from the content."""
    return re.sub(r'\S+@\S+', '', text)

def remove_forwarded_replied_headers(text):
    """Remove forwarded or replied email headers, such as '-----Original Message-----'."""
    return re.sub(r'-----Original Message-----.*?From:.*?Subject:.*?\n', '', text, flags=re.DOTALL)

def remove_special_characters(text):
    """Remove special characters that don't contribute to readability (e.g., ©, ®, ™)."""
    return re.sub(r'[^\w\s]', '', text)

def remove_excess_whitespace(text):
    """Remove excess whitespace (multiple spaces, newlines) and normalize spacing."""
    return re.sub(r'\s+', ' ', text).strip()

def remove_signature(text):
    """Remove typical email signatures and job titles."""
    return re.sub(r'(?i)(regards|sincerely|best|thanks|cheers).+?(?=^)', '', text, flags=re.DOTALL)

def remove_contact_info(text):
    """Remove phone numbers and other contact details."""
    return re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '', text)

def preprocess_email_content(raw_email):
    """Preprocess email by removing HTML, URLs, dates, and unnecessary details."""
    clean_text = clean_html(raw_email)  # Step 1: Remove HTML
    
    clean_text = remove_urls(clean_text)  # Step 2: Remove URLs
    
    #clean_text = remove_dates(clean_text)  # Step 3: Remove dates
    
    clean_text = remove_email_addresses(clean_text)  # Step 4: Remove email addresses
    
    #clean_text = remove_forwarded_replied_headers(clean_text)  # Step 5: Remove forwarded/replied headers
    
    clean_text = remove_signature(clean_text)  # Step 6: Remove signatures
    
    clean_text = remove_contact_info(clean_text)  # Step 7: Remove contact details
    
    clean_text = remove_special_characters(clean_text)  # Step 8: Remove special characters
    
    clean_text = remove_excess_whitespace(clean_text)  # Step 9: Normalize whitespace
    
    return clean_text

# Example usage with provided email content

