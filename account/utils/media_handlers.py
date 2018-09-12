"""Utility functions"""

import os.path
from django.template.defaultfilters import slugify

def upload_avatar(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{}{}".format(instance.display_name.lower(), ext)

def upload_expenditure_document(instance, filename):
    _, ext = os.path.splitext(filename)
    name = "{} {}".format(instance.paymentmode,  instance.transaction_number)
    norm_file_name = slugify(name)
    return "expenditure_documents/{}{}".format(norm_file_name, ext)

def upload_bank_document(instance, filename):
    _, ext = os.path.splitext(filename)
    name = "{} {}".format(instance.transaction_number, instance.transaction_number)
    norm_file_name = slugify(name)
    return "bank_documents/{}{}".format(norm_file_name, ext)

def upload_remit_document():
    pass

def upload_receipt(instance, filename):
    _, ext = os.path.splitext(filename)
    norm_file_name = slugify(instance.name)
    return "receipt/{}{}".format(norm_file_name, ext)
