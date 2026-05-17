from odoo import http
from odoo.http import request


class RequisitionPortal(http.Controller):

    @http.route('/requisition', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        user = request.env.user

        # ── Employee record  ──
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        values = {
            'name': employee.name,
            'designation': employee.job_id.name or '—',
            'department': employee.department_id.name or '—',
            'hr_id': employee.barcode or '—',
            'mobile': employee.mobile_phone or '—',
            'work_email': employee.work_email or '—',
            'company': employee.company_id.name or '—',
            'manager': employee.parent_id.name or '—',
            'join_date': employee.create_date.strftime('%Y-%m-%d') if employee.create_date else '—',
            'employee_image': '/web/image/hr.employee/%s/image_128' % employee.id if employee else '',
        }

        return request.render('purchase_requisition_tds.portal_requisition_form', values)