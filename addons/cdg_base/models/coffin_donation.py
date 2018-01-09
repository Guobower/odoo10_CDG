# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoffinDonation(models.Model):
    _name = 'coffin.donation'

    name = fields.Char(string='捐款者姓名', compute='set_donate_name', store=True)

    coffin_id = fields.Char(string='施棺編號', compute='set_donate_name', store=True)
    donate_id = fields.Char(string='捐款編號', compute='set_donate_name', store=True)
    donate_price = fields.Integer(string='施棺捐款金額', compute='set_donate_name', store=True)

    coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')

    @api.depends('donate_single_id')
    def set_donate_name(self):
        for line in self:
            donate_single = line.donate_single_id
            for row in donate_single.donate_list:
                if row.donate_type == 3:
                    line.donate_price = row.donate
                    line.name = row.donate_member.name
                    line.coffin_id = self.coffin_donation_id.coffin_id

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺捐款檔')
        for line in lines:
            id_create = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_id':line[u'捐款編號'],
                'donate_price':line[u'捐款金額'],
            })