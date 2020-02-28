from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings

import sendgrid

from .banner import BANNER

def sendgrid_messenger(request, mailing_list, subject, context, template):
    """send email using sendgrid"""

    sg = sendgrid.SendGridClient(
        settings.SENDGRID_USERNAME, settings.SENDGRID_PASSWORD)

    message = sendgrid.Mail()
    message.set_subject(subject)
    message.set_html(render_to_string(template, context))
    message.set_text(render_to_string(template, context))
    message.set_from('FunnShopp <no-reply@funnshopp.com>')

    receivers = []

    for mail in mailing_list:
        message.add_to(mail)
        status, msg = sg.send(message)

        if status == 200:
            receivers.append(mail)
        else:
            messages.error(request, msg)

    messages.info(request, f"{BANNER['EMAIL_SUCCESS']} {', '.join(receivers)}")
