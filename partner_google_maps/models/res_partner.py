# -*- coding: utf-8 -*-

import geocoder

from openerp import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends('street', 'street2', 'city', 'state_id',
                 'state_id.name', 'country_id', 'country_id.name', 'zip')
    def _compute_glatlng(self):
        for record in self:
            address = record._get_address()
            if address:
                g = geocoder.google(address).latlng
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

    is_display_gm = fields.Boolean('Display Google Maps?')
    g_lat = fields.Float(
        compute='_compute_glatlng', string='G Latitude', store=True,
        multi='glatlng')
    g_lng = fields.Float(
        compute='_compute_glatlng', string='G Longitude', store=True,
        multi='glatlng')

    @api.model
    def get_google_maps_data(self, domain=[]):
        # get all partners need to display google maps
        domain.append(('is_display_gm', '=', True))
        partners = self.search(domain)
        locations = []
        for partner in partners:
            location = [
                partner.street, partner.g_lat, partner.g_lng, partner.id]
            locations.append(location)

        # get google maps center configuration
        IC = self.env['ir.config_parameter']
        gm_c_lat = float(IC.get_param('Google_Maps_Center_Latitude'))
        gm_c_lng = float(IC.get_param('Google_Maps_Center_Longitude'))
        gm_zoom = int(IC.get_param('Google_Maps_Zoom'))

        return locations, (gm_c_lat, gm_c_lng, gm_zoom)
