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

import geocoder

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_display_gm = fields.Boolean('Display Google Maps?')

    @api.depends('street', 'street2', 'city', 'state_id',
                 'state_id.name', 'country_id', 'country_id.name', 'zip')
    def _compute_glatlng(self):
        # key = self.env['ir.config_parameter'].get_param('Google_Maps_User_Key')
        for record in self:
            address = record._get_address()
            if address:
                g = geocoder.google(address, key='AIzaSyDVws0_U97KYYtn-R2OSsWf3RIy-2_JG_M').latlng
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
        content_string = (
            '<div class="oe_kanban_global_click o_res_partner_kanban o_kanban_record">'
            '<div class="o_kanban_tags_section oe_kanban_partner_categories">'
            '<span class="oe_kanban_list_many2many">'
            '<div name="category_id" can_create="true" can_write="true" modifiers="{}" class=" oe_form_field o_form_field_many2manytags o_kanban_tags"></div>'
            '</span>'
            '</div>'
            '<div class="o_kanban_image" style="float: left;text-align: center;">'
            '<img src="%s/web/image?model=res.partner&amp;field=image_small&amp;id=%d&amp;unique=20180725215223" style="margin-left: 8px; max-width: 100&percnt;;">'
            '</div>'
            '<div class="oe_kanban_details">'
            '<strong class="oe_partner_heading">%s, %s</strong>'
            '<ul>'
            '<li>%s</li>'
            '<li>%s</li>'
            '<li>%s, %s</li>'
            '<li class="o_text_overflow">%s</li>'
            '</ul>'
            '<div class="oe_kanban_partner_links">'
            '</div>'
            '</div>'
            '</div>' % (
                web_base,
                self.id,
                self.parent_id.name if self.parent_id else '',
                self.name or '',
                self.function if self.function else '',
                self.street or '',
                self.city or '',
                self.country_id.name if self.country_id else '',
                self.email if self.email else ''
            )
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
        gm_c_lat = 51.26  # float(IC.get_param('Google_Maps_Center_Latitude'))
        gm_c_lng = 4.40  # float(IC.get_param('Google_Maps_Center_Longitude'))
        gm_zoom = 10  # int(IC.get_param('Google_Maps_Zoom'))

        return locations, (gm_c_lat, gm_c_lng, gm_zoom)
