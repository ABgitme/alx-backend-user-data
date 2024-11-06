#!/usr/bin/env python3
"""
This module connects to a MySQL database, retrieves user data,
and logs it with sensitive fields redacted. The logging system
is configured to redact specific fields marked as PII (Personally
Identifiable Information) such as name, email, phone, SSN, and password.
"""
import re
import logging
import os
import mysql.connector
from mysql.connector import connection

# Define fields that should be considered as Personally
# Identifiable Information (PII)
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields, redaction, message, separator):
    """
    This function filters sensitive data from a given message
    by replacing the values of specified fields with a redaction string.

    Parameters:
    fields (list): A list of field names to be redacted.
    redaction (str): The string to replace the redacted field values with.
    message (str): The input message containing the sensitive data.
    separator (str): The character used to separate fields in the message.

    Returns:
    str: The filtered message with redacted sensitive data.
    """
    pattern = r'({})=([^{}]+)'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1={}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """
    A logging formatter class that redacts sensitive fields in log messages.

    Attributes:
        REDACTION (str): The string used to
            replace sensitive data.
        FORMAT (str): The logging format to be used.
        SEPARATOR (str): The separator character between
            fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Initializes the RedactingFormatter with specified fields to redact.

        Args:
            fields (list): List of fields to be redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record message,
        redacting specified sensitive fields.

        Args:
            record (logging.LogRecord): The log record
                to be formatted.

        Returns:
            str: The formatted and redacted log message.
        """
        """Format the record message, filtering sensitive fields"""
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger that redacts specified PII fields
    in log messages. Logs are restricted to the INFO level and do not
    propagate to other loggers.

    Returns:
        logging.Logger: Configured logger for user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Configure stream handler with redacting formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using credentials
    stored in environment variables.

    Environment Variables:
        PERSONAL_DATA_DB_USERNAME (str): Database username (default: 'root').
        PERSONAL_DATA_DB_PASSWORD (str): Database password (default: '').
        PERSONAL_DATA_DB_HOST (str): Database host (default: 'localhost').
        PERSONAL_DATA_DB_NAME (str): Name of the database to connect to.

    Returns:
        mysql.connector.connection.MySQLConnection:
            Connection to the MySQL database.
    """
    # Fetch environment variables for database credentials
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish and return a connection to the database
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Main function to retrieve and log users' data from the database
    with filtered sensitive information. Connects to the database,
    retrieves all rows from the users table, and logs each row
    using a redacted format for PII fields.
    """
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows from users table
    cursor.execute("SELECT * FROM users;")
    columns = [col[0] for col in cursor.description]

    # Setup the logger
    logger = get_logger()

    for row in cursor:
        # Create a dictionary mapping column names to row values
        row_data = "; ".join(f"{col}={val}" for col, val in zip(columns, row))
        # Log the formatted and filtered row data
        logger.info(row_data.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
