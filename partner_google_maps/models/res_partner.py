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

import logging
import geocoder
from odoo import api, models, fields
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_display_gm = fields.Boolean('Display Google Maps?')

    @api.depends('street', 'street2', 'city', 'state_id',
                 'state_id.name', 'country_id', 'country_id.name', 'zip')
    def _compute_glatlng(self):
        key = self.env['ir.config_parameter'].get_param('Google_Maps_API_Key')
        for record in self:
            address = record._get_address()
            if address:
                g = geocoder.google(address, key=key).latlng
                if g:
                    record.g_lat = g[0]
                    record.g_lng = g[1]

    def _get_address(self):
        address = []
        if self.street:
            address.append(self.street)
        if self.street2:
            address.append(self.street2)
        if self.city:
            address.append(self.city)
        if self.state_id:
            address.append(self.state_id.name)
        if self.country_id:
            address.append(self.country_id.name)
        if self.zip:
            address.append(self.zip)

        return ', '.join(address)


    g_lat = fields.Float(
        compute='_compute_glatlng', string='G Latitude', store=True,
        multi='glatlng')
    g_lng = fields.Float(
        compute='_compute_glatlng', string='G Longitude', store=True,
        multi='glatlng')

    @api.multi
    def get_location_widget(self):
        self.ensure_one()
        web_base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        u_name = "%s%s%s" % (
            self.parent_id.name if self.parent_id else '',
            ', ' if self.parent_id and self.name else '',
            self.name if self.name else '')
        u_function = '<li>' + self.function + '</li>' if self.function else ''
        u_street = '<li>' + self.street + '</li>' if self.street  else ''
        u_city = '<li>' + self.city + '</li>' if self.city else ''
        u_country = '<li>' + self.country_id.name + '</li>' if self.country_id else ''
        u_email = '<li>' + self.email + '</li>' if self.email else ''
        u_phone = '<li>' + self.phone + '</li>' if self.phone else ''
        content_string = '''<div>
                <div style="float: left;text-align: center; padding-left: px;">
                <img src="%s/web/image?model=res.partner&amp;field=image_small&amp;id=%d" style="margin-left: 8px; max-width: 100%%;padding-top: 20px;">
                </div>'
                <div style="padding-left: 42px; font-size:13px;">
                <strong style="padding: 10px">%s</strong>
                <ul style="list-style-type: none; margin-top: 0;">
                %s
                %s
                %s
                %s
                %s
                %s
                </ul>
                </div>
                </div>''' % (
            web_base,
            self.id,
            u_name,
            u_function,
            u_street,
            u_city,
            u_country,
            u_email,
            u_phone
        )

        return content_string

    @api.model
    def get_google_maps_data(self, domain=[]):
        # get all partners need to display google maps
        domain.append(('is_display_gm', '=', True))
        partners = self.search(domain)
        locations = []
        for partner in partners:
            location = [
                partner.get_location_widget(), partner.g_lat, partner.g_lng, partner.id]
            locations.append(location)

        # get google maps center configuration
        IC = self.env['ir.config_parameter']
        gm_c_lat = float(IC.get_param('Google_Maps_Center_Latitude'))  # 51.26
        gm_c_lng = float(IC.get_param('Google_Maps_Center_Longitude'))  # 4.40
        gm_zoom = int(IC.get_param('Google_Maps_Zoom'))  # 10

        return locations, (gm_c_lat, gm_c_lng, gm_zoom)
