from odoo import models, fields, api, _
import re


class UniversityTeacher(models.Model):
    _name = 'university.teacher'
    _description = 'Teacher management'
    _rec_name = 'f_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    f_name = fields.Char(string="Prenom", required=True)
    l_name = fields.Char(string='Nom', tracking=True, required=True)
    date_of_birth = fields.Date(string='Date de Naissance', required=True)
    e_mail = fields.Char('E-mail', tracking=True, required=True)
    identity_card = fields.Char(string='Carte Identité', required=True, tracking=True)
    phone = fields.Char(string='Téléphone', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    rue = fields.Char('Rue')
    ville = fields.Char('Ville')
    code_postale = fields.Char('Code postale')
    date_inscription = fields.Datetime(string='Date Inscription', default=fields.Datetime.now, readonly=True)
    date_start = fields.Datetime('Date of start', default=fields.Datetime.now, readonly=True)
    image = fields.Binary(string="Image", attachment=True)
    image_cv = fields.Binary(string="CV", attachment=True)


    teacher_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    subject_id = fields.Many2one(comodel_name='university.subject', string='Matiere')
    class_ids = fields.Many2many('university.class', 'prof_class_rel', 'f_name', 'class_name', string='Classe')
    state = fields.Selection([
        ('enregistre', 'Enregistre'),
        ('en_cours', 'Encours'),
    ], string='Status', readonly=True, default='enregistre')

    def action_administration(self):
        student_group = self.env.ref('university_managment.group_university_student')
        student_group.write({'users':[(3,self.teacher_id.id)]})
        teacher_group = self.env.ref('university_managment.group_university_teacher')
        teacher_group.write({'users':[(4,self.teacher_id.id)]})
        admin_group = self.env.ref('university_managment.group_university_administrateur')
        admin_group.write({'users':[(3,self.teacher_id.id)]})

    @api.model
    def create(self, values):
        if self.env['res.users'].sudo().search([('login', '=', values.get('e_mail'))]):
            user_id = self.env['res.users'].search([('login', '=', values.get('e_mail'))])
            values.update(teacher_id=user_id.id)
        else:
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

    def action_enregsitre(self):
        for rec in self:
            rec.state = 'enregistre'


    def action_en_cours(self):
        for rec in self:
            rec.state = 'en_cours'

    @api.constrains('e_mail')
    def validate_email(self):
        for obj in self:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.e_mail) == None:
                raise ValidationError("Vérifier votre adresse mail  : %s" % obj.e_mail)

        return True

    @api.constrains('phone')
    def check_name(self):
        for rec in self:
            if len(self.phone) != 8:
                raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))
            if len(self.identity_card) != 8:
                raise ValidationError(_('Numéro  de cin/passeport doit contenir seulement 8 chiffres'))

