from odoo import models, fields,api,_

class UniversityClass(models.Model):
    _name = 'university.class'
    _rec_name = 'class_name'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _description = 'Gestion de classes'

    reference = fields.Char(string='class reference', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))
    class_name = fields.Char(string='Class Name', tracking = True)
    class_code = fields.Char(string='Code Class',tracking = True)
    date_creation = fields.Datetime(string='Date Creation')
    student_ids = fields.One2many(comodel_name='university.student', inverse_name='class_id', string="Students")
    professor_ids = fields.Many2many('university.teacher', 'prof_class_rel', 'class_name', 'f_name', string='Professeur')
    subject_ids = fields.Many2many(comodel_name='university.subject',
                                   relation='class_subject_rel',
                                   column1='class_name',
                                   column='name')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('university.class.seq') or _('New')
        result = super(UniversityClass, self).create(vals)
        return result
    #
    # @api.depends('f_name','gender')
    # def whoIs(self):
    #     if self.gender=='male':
    #         print('he is a man')
    #     else:
    #         print('she is a woman')