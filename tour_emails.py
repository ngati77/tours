# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:17:48 2018

@author: Tamuz
"""


from django.core.mail import EmailMultiAlternatives

class tour_emails:
    def send_email(msg_html, msg_plain, email, title):
        #title = 'אישור הזמנה'
        subject         = title
        from_email      = 'yael.gati@cambridgeinhebrew.com'
        to              = email
        text_content    = msg_plain
        html_content    = msg_html
        msg             = EmailMultiAlternatives(subject, text_content, from_email, [to],cc=['yael.gati@cambridgeinhebrew.com','yrimon@gmail.com'] ,bcc=['noam.gati@gmail.com'])
        msg.attach_alternative(html_content, "text/html")
        success = msg.send()
        return success
 


    
