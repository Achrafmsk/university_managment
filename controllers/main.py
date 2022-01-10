from odoo import http
from odoo.http import request

from odoo import http
from odoo.http import request

class University_student(http.Controller):
    @http.route('/university/student/', type="http", website=True, auth='public')
    def university_student(self, **kw):
        # return "Thanks for watching"

        # http.request.env['university.student'].sudo().create(kw)
        return http.request.render("university_managment.student_page", {
        })

    @http.route('/creer/student', type="http", auth='public', website=True)
    def creeruser_student(self, **kw):
        http.request.env['university.student'].sudo().create(kw)
        return http.request.render('university_managment.student_page_thanks', {})


class University_teacher(http.Controller):

    # creation dans la base de données



    @http.route('/university/teacher/', type="http", website=True, auth='public')
    def university_teacher(self, **kw):
        # return "Thanks for watching"
        print("aziz")
        # http.request.env['university.student'].sudo().create(kw)
        return http.request.render("university_managment.teacher_page", {

        })



    # creation dans la base de données
    @http.route('/creer/teacher', type="http", auth='public', website=True)
    def creeruser_teacher(self, **kw):
        print("aziz")
        http.request.env['university.teacher'].sudo().create(kw)
        return http.request.render('university_managment.student_page_thanks', {})