# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016- TUANNGUYEN36.VN@GMAIL.COM
#    @author TuanNguyen (https://www.linkedin.com/in/tuan-nguyen-90191271)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Partner Google Maps',
    'version': '10.0.1.0.0',
    'author': "tuannguyen36.vn@gmail.com",
    'category': 'Extra Tools',
    'summary': "view all partner location on google maps",
    'depends': [
        'base',
        'web'],
    'data': [
        'data/ir_config_parameter_data.xml',
        'views/partner_google_maps_templates.xml',
        'views/res_partner_view.xml'
    ],
    'qweb': [
        'static/src/xml/custom_view.xml',
        'static/src/xml/partner_google_maps.xml',
    ],
    'active': False,
    'installable': True,
    'application': False,
}
