from odoo import fields, models, api


class TeacherGrade(models.TransientModel):
    _name = "teacher.grade"
    grade = fields.Text('new grade')

    @api.onchange('grade')
    def onchange_grade(self):
        if self.grade in ['PESHC', 'peshc', 'pes', 'PES']:
            self.grade = self.grade.upper() + '  GOOD LUCK :) '
        # else:
        #     self.grade =self.grade.upper() + 'ce grade est inconnu'

