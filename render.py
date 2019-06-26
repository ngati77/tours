# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 21:49:00 2019

@author: Tamuz
"""

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os

from bidi import algorithm as bidialg

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        #print(template)
        html = template.render(params)
        #print('----------------------------------------------------------------')
        #print(html)
        response = BytesIO()
        pdf = pisa.CreatePDF(bidialg.get_display(html, base_dir="L"), response)
        #pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, fileName: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = fileName
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store", file_name)
        #print('File Path')
        #print(file_path)
        with open(file_path, 'wb') as pdf:
            #pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
             pisa.CreatePDF(bidialg.get_display(html, base_dir="L"), pdf)
        return [file_name, file_path]
