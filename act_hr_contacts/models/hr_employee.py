# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    guarantor_ids = fields.Many2many(
        comodel_name='res.partner', string='Guarantors')
