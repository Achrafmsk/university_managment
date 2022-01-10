# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversitySubject(models.Model):
    _name = 'university.subject'
    _description = 'Subject description'


    name = fields.Char()
    code = fields.Char()
    # reference = fields.Char(string='subject reference', required=True, copy=False, readonly=True,
    #                         default=lambda self: _('New'))


    professor_ids = fields.Many2many(comodel_name='university.teacher',
                                         relation='subject_proff_rel',
                                         column1='name',
                                         column='f_name')


# @api.model
# def create(self, vals):
#     if vals.get('reference', _('New')) == _('New'):
#         vals['reference'] = self.env['ir.sequence'].next_by_code('university.subject.seq') or _('New')
#     result = super(UniversitySubject, self).create(vals)
#     return result