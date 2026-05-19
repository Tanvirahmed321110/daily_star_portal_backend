from odoo import http
from odoo.http import request
from datetime import date


class RequisitionDetailsController(http.Controller):
    @http.route('/dashboard/requisition_details', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''

        breadcrumb = [
            {'name': 'Dashboard', 'url': '/dashboard'},
            {'name': 'Requisition Details', 'url': False},
        ]

        return request.render('purchase_requisition_tds.portal_requisition_details', {
            'breadcrumb': breadcrumb,
            'name':name,
            'employee_image': employee.image_128,
            'work_email': employee.work_email or '—',
        })
