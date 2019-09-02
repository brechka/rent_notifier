""" Send email via smtp_host (Simple Mail Transfer Protocol). """


import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header


def get_contacts(filename='contacts.txt'):
    """
    Extracts names and email-addresses from filename.
    Returns a lists of above data respectively.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    
    return names, emails


def get_addresser_info(filename='addresser_info.txt'):
    """
    Retrieves e-mail and password for the future using given mail account.
    """
    
    addresser_info = []
    
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for line in contacts_file:
            addresser_info.append(line.split()[0])
    
    return addresser_info


def read_msg_template(filename='message.html'):
    """
    Extracts the message text from the filename and returns it.
    """

    with open(filename, 'r', encoding='utf-8') as temp_file:
        template_file = temp_file.read()
    
    return template_file


def send_mail(properties):
    """
    Calls get_contacts and read_template functions. Establishes gmail SMTP
    connection. Sends a message returned from the read_msg_template function
    to get_contacts's users in advance substituted the constants by appropriate
    data.
    """
    
    num_rooms, location, price, photo, url = properties
    names, emails = get_contacts()
    login, password = tuple(get_addresser_info())
    message_template = read_msg_template()

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(login, password)
    for name, email in zip(names, emails):
        message = message_template.format(
            PERSON_NAME = name.title(),
            NUM_ROOMS = num_rooms,
            LOCATION = location,
            PRICE = price,
            PHOTO = photo,
            LINK = url
        )

        msg = MIMEText(message, 'html')
        
        msg['Subject'] = Header('Flat renting', 'utf-8')
        msg['From'] = login
        msg['To'] = email

        s.sendmail(msg['From'], email, msg.as_string())

    s.quit()
