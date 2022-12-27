from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    guarantor = fields.Boolean('Is Guarantor')
    hmo = fields.Boolean('Is HMO')
    pfa = fields.Boolean('Is PFA')
    relationship_id = fields.Many2one(
        comodel_name='guarantor.type', string="Relationship with employee")
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee')
