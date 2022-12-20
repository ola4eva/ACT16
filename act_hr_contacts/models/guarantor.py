from odoo import models, fields


class GuarantorType(models.Model):
    _name = 'guarantor.type'
    _description = 'Guarantor Type'

    name = fields.Char('Type')
