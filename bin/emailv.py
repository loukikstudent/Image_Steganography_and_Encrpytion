from email_validator import validate_email, EmailNotValidError


def check_mail(email: str):
    """

    :type email: str
    :param email: 
    :return: 
    """
    try:
        # validated email
        valid = validate_email(email)

        # normalize email
        email = valid.email
        return email
    except EmailNotValidError as e:
        return False

# if __name__=="__main__":
#     print(check_mail(""))