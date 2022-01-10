from odoo import models, fields, api,  _


class UniversityEmploi(models.Model):
    _name = 'university.emploi'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _description = 'Gestion des emplois '
    # _rec_name = 'f_name'
    reference = fields.Char(string='Emploi reference', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))
    emploi_name = fields.Char(string='Emploi Name', tracking = True)
    emploi_code = fields.Char(string='Emploi Class',tracking = True)
    emploi_date_creation = fields.Datetime(string='Date Creation')
    # seance_ids = fields.Onetomany(comodel_name='university.seance', string='Seances')
    seance_ids = fields.One2many(comodel_name='university.seance', inverse_name='seance_id', string="Seances")
    seance_count = fields.Integer(string='Seance', compute='get_seance_count')
    class_id = fields.Many2one(comodel_name='university.class', string='Classe')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('university.emploi.seq') or _('New')
        result = super(UniversityEmploi, self).create(vals)
        return result

    def get_seance_count(self):
        count = self.env['university.seance'].search_count([('seance_id', '=', self.id)])
        self.seance_count = count

    def action_open_emploi_seance(self):
        return {
            'name': _('Seances'),
            'domain': [('seance_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'university.seance',
            'view_id': False,
            'view_mode': 'calendar,tree,form',
            'type': 'ir.actions.act_window',
        }
