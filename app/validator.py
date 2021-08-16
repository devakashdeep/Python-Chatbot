import re


def is_string(str):
    return bool(re.match('[a-z]', str.strip().lower()))


def valid_string(str):
    return str.strip()


def is_empty(str):
    if len(str.strip()) > 0:
        return False
    return True


def valid_email(str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.fullmatch(regex, str.strip()))


def validate_str_field(val, field_name):
    error = None
    valid = True
    if not val:
        error = f"{field_name} required"
        valid = False
    else:
        if val == "":
            error = f"{field_name} can't be empty"
            valid = False
        if not is_string(val):
            error = f"{field_name} must be string"
            valid = False

    return {"is_valid": valid, "error": error}


def validate_email_field(val):
    error = None
    valid = True
    if not val:
        error = "Email required"
        valid = False
    else:
        if val == "":
            error = f"Email can't be empty"
            valid = False
        if not valid_email(val):
            error = f"Invalid Email"
            valid = False

    return {"is_valid": valid, "error": error}


def validate_username_field(val, field_name):
    error = None
    valid = True
    if not val:
        error = f"{field_name} required"
        valid = False
    else:
        if val == "":
            error = f"{field_name} can't be empty"
            valid = False
        if not is_string(val) and not bool(re.match('[A-Z][a-z][0-9]', val)):
            error = f"Invalid {field_name}"
            valid = False

    return {"is_valid": valid, "error": error}


def validate_password(val, field_name):
    error = None
    valid = True
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    if not val:
        error = f"{field_name} required"
        valid = False
    else:
        if val == "":
            error = f"{field_name} can't be empty"
            valid = False

        pat = re.compile(reg)
        mat = re.search(pat, val)
        if not mat:
            error = f"{field_name} must contain Capital alphabets, numbers, and special characters"
            valid = False

    return {"is_valid": valid, "error": error}
