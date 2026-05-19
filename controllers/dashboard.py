from odoo import http
from odoo.http import request
from datetime import date


class RequisitionPortal(http.Controller):
    @http.route('/dashboard', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)
        products = request.env['product.product'].sudo().search([])

        values = {
            'sl_number' : requisition.name,
            'products': products,
            'name': name,
            'designation': employee.job_id.name or '—',
            'department': employee.department_id.name or '—',
            'hr_id': employee.barcode or '—',
            'work_email': employee.work_email or '—',
            'employee_image': employee.image_128,
            'today': date.today().strftime('%Y-%m-%d'),
        }

        return request.render('purchase_requisition_tds.portal_requisition_dashboard', values)