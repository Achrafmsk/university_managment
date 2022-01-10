from odoo import models, fields,api,_

class UniversitySeance(models.Model):
    _name = 'university.seance'
    _rec_name = 'matiere'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _description = 'Gestion des seances '
    reference = fields.Char(string='Seance reference', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))
    seance_code = fields.Char(string='Seance Code',tracking = True)
    matiere = fields.Many2one(string = 'Matière',comodel_name = 'university.subject')
    seance_date_debut = fields.Datetime(string='Date Debut')
    seance_date_fin = fields.Datetime(string='Date fin')
    seance_id = fields.Many2one(comodel_name='university.emploi', string='Emploi', readonly=True)
    teacher_id = fields.Many2one(comodel_name='university.teacher', string='Professeur')


    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('university.seance.seq') or _('New')
        result = super(UniversitySeance, self).create(vals)
        return result
    #
    # @api.depends('f_name','gender')
    # def whoIs(self):
    #     if self.gender=='male':
    #         print('he is a man')
    #     else:
    #         print('she is a woman')