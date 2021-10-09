""" Functions to send emails from the apps mail account """

from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from .. import mail


def send_async_email(app, msg):
    """ sends msg """
    # flask extensions operate under assumption there are active app contexts
    # contexts are associated with a thread
    # this executes in seperate thread so needs app context to be created artificially
    # app is passed as an arg app context can be created
    with app.app_context():
        mail.send(msg)


def send_email(recipient, subject, template, attachments=None, **kwargs):
    """ creates a thread to send the email """
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  recipients=[recipient])

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    if attachments is not None:
        for mime_type in attachments:
            for attachment in attachments[mime_type]:
                with app.open_resource(attachment) as fp:
                    msg.attach(attachment, mime_type, fp.read())


    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    return thr
