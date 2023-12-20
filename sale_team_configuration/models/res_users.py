from odoo import api, fields, models, _


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    lead_ids = fields.One2many('crm.team', 'user_id')