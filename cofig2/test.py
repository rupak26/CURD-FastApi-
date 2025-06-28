import logging

def test_error_email():
    logger = logging.getLogger()

    # This should trigger the email alert if SMTPHandler is configured correctly
    logger.error("Test error: This should send you an email alert!")

if __name__ == "__main__":
    test_error_email()
    print("Test error logged. Check your email inbox for alert.")
