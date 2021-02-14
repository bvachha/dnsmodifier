from app import app


def parse_soa_email(email, encode):
    """
    handles the encoding of the soa email address into the correct format
    :param email: email address to parse and encode
    :param encode: encode mode or decode mode flag
    :return: encoded email address
    """
    app.logger.info(f"Parsing email {email} into format specified for SOA records")
    if encode:
        email_split = email.split('@')
        email = email_split[0]
        email = email.replace(".", "\.")
        email = email+'.'+email_split[1]
        return email