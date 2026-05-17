from odoo import http
from odoo.http import request
from datetime import date  # ← add করো


class RequisitionPortal(http.Controller):

    @http.route('/requisition', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        user = request.env.user

        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        name = employee.name or ''
        words = name.split()
        if len(words) >= 2:
            initials = (words[0][0] + words[1][0]).upper()
        else:
            initials = words[0][0].upper() if words else ''

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)
        products = request.env['product.product'].sudo().search([])

        values = {
            'requisition':    requisition,
            'products':products,
            'name':           name,
            'initials':       initials,
            'designation':    employee.job_id.name or '—',
            'department':     employee.department_id.name or '—',
            'hr_id':          employee.barcode or '—',
            'work_email':     employee.work_email or '—',
            'employee_image': '/web/image/hr.employee/%s/image_128' % employee.id if employee else '',
            'today':          date.today().strftime('%Y-%m-%d'),
        }

        return request.render('purchase_requisition_tds.portal_requisition_form', values)