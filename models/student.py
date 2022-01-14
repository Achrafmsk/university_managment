from odoo import models, fields,api,_
from odoo.exceptions import ValidationError
import re,random,string
from datetime import datetime

# self.env.user.has_group('base.group_user') # Check for Internal User
#     self.env.user.has_group('base.group_portal') # Check for Portal User
#     self.env.user.has_group('base.group_public') # Check for Public User
#
# class ResPartners(models.Model):
#     _inherit = 'res.partner'
#
#     @api.model
#     def create(self, vals_list):
#         res = super(ResPartners, self).create(vals_list)
#         print("yes working")
#         # do the custom coding here
#         return res


class UniversityStudent(models.Model):
    _name = 'university.student'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _description = 'student inscription'
    _rec_name = 'f_name'


    _sql_constraints = [
        ('cin_pass_uniq', 'unique(identity_card)', 'Numero de cin/passeport existe déja'),
        ('e_mail_uniq', 'unique(e_mail)', 'Email existe déja'),
     ]

    reference = fields.Char(string='student reference', required=True, copy=False, readonly=True,
                             default=lambda self: _('New'))
    student_id = fields.Many2one('res.users', ondelete='set null', string="User", index=True)
    class_id = fields.Many2one(comodel_name='university.class', string='Classe' )

    f_name = fields.Char(string="Prenom",required = True )
    l_name = fields.Char(string='Nom',tracking = True ,required = True)
    date_of_birth = fields.Date(string='Date de Naissance', required=True)
    e_mail = fields.Char('E-mail', tracking=True , required = True)
    identity_card = fields.Char(string='Carte Identité',required = True,tracking = True)
    phone = fields.Char(string='Téléphone' ,required = True)
    gender = fields.Selection([('male','Male'),('female','Female')] )
    rue = fields.Char('Rue')
    ville = fields.Char('Ville')
    code_postale = fields.Char('Code postale')
    date_inscription = fields.Datetime(string='Date Inscription' , default=fields.Datetime.now, readonly=True)
    image = fields.Binary(string="Image", attachment=True)
    image_cv= fields.Binary(string="CV", attachment=True)
    password = fields.Char(string='Password', required=True)
    date = fields.Date(default=datetime.today())
    date_paiement = fields.Datetime(string='Date Prochain Paiement', default=fields.Datetime.now)
    state = fields.Selection([
        ('nouveau', 'Nouveau Inscrit'),
        ('attente', 'En attente'),
        ('affecte', 'Affecté'),
        ('paiment_reg', 'Paiement effectué'),
        ('mail_sended', 'Mail sended')
    ], string='Status', readonly=True, default='nouveau')

    def action_administration(self):
        self.env.ref('university_managment.group_university_student').write({'users': [(4, self.student_id.id)]})
        self.env.ref('university_managment.group_university_teacher').write({'users': [(3, self.student_id.id)]})
        self.env.ref('university_managment.group_university_administrateur').write({'users': [(3, self.student_id.id)]})

    def action_en_attente(self):
        self.state = 'attente'

    def action_affecte(self):
        self.state = 'affecte'

    def action_paiement_reg(self):
        self.state = 'paiment_reg'

    def action_mail_send(self):
        self.sudo().write({'state': 'mail_sended'})
        template_mail_id = self.env.ref('university_managment.student_inscription_email').id
        vals = {
            'email_from': self.env.user.partner_id.email,
            'email_to': self.e_mail
        }
        self.env['mail.template'].browse(template_mail_id).send_mail(self.id, email_values=vals, force_send=True)

    @api.model
    def create(self, values):
        password = ''
        for pwd in range(8):
            password += random.SystemRandom().choice(string.ascii_letters + string.digits)
        values.update(password=password)
        if self.env['res.users'].sudo().search([('login', '=', values.get('e_mail'))]):
            user_id = self.env['res.users'].search([('login', '=', values.get('e_mail'))])
            values.update(student_id=user_id.id)
        else:
            vals_user = {
                'name': values.get('f_name'),
                'login': values.get('e_mail'),
                'password': password,
                # other required field
            }
            user_id = self.env['res.users'].sudo().create(vals_user)
            values.update(student_id=user_id.id)
        res = super(UniversityStudent, self).create(values)
        return res

    @api.constrains('e_mail')
    def validate_email(self):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.e_mail) == None:
            raise ValidationError("Vérifier votre adresse mail  : %s" % self.e_mail)
        return True

    @api.constrains('phone')
    def check_name(self):
        if len(self.phone) != 8:
            raise ValidationError(_('Numéro de tel doit contenir seulement 8 chiffres'))
        if len(self.identity_card) != 8:
            raise ValidationError(_('Numéro  de cin/passeport doit contenir seulement 8 chiffres'))

