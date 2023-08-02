import glob
import re
import phonenumbers


def get_pdf_file_paths(directory):
    file_paths = glob.glob(directory + '/**/*.pdf', recursive=True)
    return file_paths

def validate_email(email):
    pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return pattern.match(email) is not None

def validate_us_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "US")
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return False
