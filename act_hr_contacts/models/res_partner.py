from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    guarantor = fields.Boolean('Guarantor')
    relationship_id = fields.Many2one(comodel_name='guarantor.type', string="Relationship with employee")