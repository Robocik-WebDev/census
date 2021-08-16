from flask import send_from_directory


def send_file(file):
    return send_from_directory('../client/public', file)
