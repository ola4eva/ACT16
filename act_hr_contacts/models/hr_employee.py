# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    guarantor_ids = fields.Many2many(
        comodel_name='res.partner', string='Guarantors')
    pfa_ids = fields.One2many(
        comodel_name='employee.pfa', inverse_name='employee_id', string='PFA')
    hmo_ids = fields.One2many(
        comodel_name='employee.hmo', inverse_name='employee_id', string='HMO')


class HrEmployeePfa(models.Model):
    _name = 'employee.pfa'
    _description = 'Employee PFA Information'

    pfa_id = fields.Many2one('res.partner', string='PFA',
                             domain="[('pfa', '=', True)]")
    pfa_number = fields.Char(string="PFA Number")
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee")


class HrEmployeeHmo(models.Model):
    _name = 'employee.hmo'
    _description = 'Employee PFA Information'

    hmo_id = fields.Many2one('res.partner', string='HMO',
                             domain="[('hmo', '=', True)]")
    hmo_number = fields.Char(string="HMO Number")
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee")
