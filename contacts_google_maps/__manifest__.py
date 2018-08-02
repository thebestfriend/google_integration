# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': 'Contacts Google Maps',
    'version': '10.0.1.0.0',
    'author': "AbAKUS IT-Solutions",
    'category': 'Extra Tools',
    'summary': "view all contacts location on google maps",
    'depends': [
        'contacts',
        'partner_google_maps',
    ],
    'data': [
        'views/contact_view.xml'
    ],
    'installable': True,
    'application': False,
}
