from email_validator import validate_email, EmailNotValidError
from validate_email import validate_email
from validate_email.updater import update_builtin_blacklist


# def check_mail(email: str):
#     """
#
#     :type email: str
#     :param email:
#     :return:
#     """
#     try:
#         # validated email
#         valid = validate_email(email)
#
#         # normalize email
#         email = valid.email
#         return email
#     except EmailNotValidError as e:
#         return False

def check_mail(email: str):
    """

    :type email: object
    """
    update_builtin_blacklist(force=False, background=True, callback=None)
    is_valid = validate_email(email_address=email, check_regex=True, smtp_timeout=10, dns_timeout=10, use_blacklist=True)
    return is_valid

if __name__=="__main__":
    print(check_mail("loukik.aiesec@gmail.com"))