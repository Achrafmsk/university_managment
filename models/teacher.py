from odoo import models, fields, api, _
import re


class UniversityTeacher(models.Model):
    _name = 'university.teacher'
    _description = 'Teacher management'
    _rec_name = 'f_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    date_start = fields.Datetime('Date of start', tracking=True)
    teacher_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    f_name = fields.Char(string='First Name', tracking=True, required=True)
    l_name = fields.Char(string='Last Name', tracking=True, required=True)
    identity_card = fields.Char(string='Identity card', required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    date_of_birth = fields.Date(string='Date of birth', required=True)
    date_start = fields.Datetime('Date of start', default=fields.Datetime.now, readonly=True)
    e_mail = fields.Char('E-mail', tracking=True,required = True)
    phone = fields.Char('Phone number', tracking=True,required = True)
    rue = fields.Char('Rue')
    ville = fields.Char('Ville')
    code_postale = fields.Char('Code postale')
    suggestions = fields.Text('Suggestions')
    subject_id = fields.Many2one(comodel_name='university.subject', string='Matiere')
    class_ids = fields.Many2many('university.class', 'prof_class_rel', 'f_name', 'class_name', string='Classe')

    # reference = fields.Char(string='teacher reference', required=True, copy=False, readonly=True,
    #                         default=lambda self: _('New'))

    # _sql_constraints = [
    #     ('cin_pass_uniq', 'unique(identity_card)', 'Numero de cin/passeport existe déja'),
    #     ('e_mail_uniq', 'unique(e_mail)', 'Email existe déja'),
    # ]
    @api.model
    def create(self, values):
        # if values.get('reference', _('New')) == _('New'):
        #     values['reference'] = self.env['ir.sequence'].next_by_code('university.teacher.seq') or _('New')
        # res = super(UniversityTeacher, self).create(values)

        vals_user = {
            'name': values.get('f_name'),
            'login': values.get('e_mail'),
            # 'password': values.get('mot_passe'),
            # other required field
        }
        user_id = self.env['res.users'].sudo().create(vals_user)
        values.update(teacher_id=user_id.id)
        res = super(UniversityTeacher, self).create(values)

        return res

    # @api.constrains('e_mail')
    # def validate_email(self):
    #     for obj in self:
    #         if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.e_mail) == None:
    #             raise ValidationError("Vérifier votre adresse mail  : %s" % obj.e_mail)
    #
    #     return True
    #
    # @api.constrains('phone')
    # def check_name(self):
    #     for rec in self:
    #         if len(self.phone) != 8:
    #             raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))
    #         if len(self.identity_card) != 8:
    #             raise ValidationError(_('Numéro  de cin/passeport doit contenir seulement 8 chiffres'))