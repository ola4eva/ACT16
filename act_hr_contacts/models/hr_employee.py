# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    guarantor_ids = fields.Many2many(
        comodel_name='res.partner', string='Guarantors')
    pfa_id = fields.Many2one('res.partner', string='PFA',
                             domain="[('pfa', '=', True)]")
    pfa_number = fields.Char('PFA Number')
    hmo_id = fields.Many2one('res.partner', string='HMO',
                             domain="[('hmo', '=', True)]")
    hmo_number = fields.Char('HMO Number')
