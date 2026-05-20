from odoo import http
from odoo.http import request
from datetime import date
from .base import _get_user_data


class RequisitionPortal(http.Controller):
    @http.route('/dashboard/requisition', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        # import from base
        values = _get_user_data()

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)
        products = request.env['product.product'].sudo().search([])

        breadcrumb = [
            {'name': 'Dashboard', 'url': '/dashboard'},
            {'name': 'Create New Requisition', 'url': False},
        ]

        values.update({
            'sl_number' : requisition.name or 'Empty',
            'products': products,
            'name': name,
            'today': date.today().strftime('%Y-%m-%d'),
            'breadcrumb' :breadcrumb,
        })

        return request.render('purchase_requisition_tds.portal_requisition_form', values)


    # =============  For Data Submit  =============
    @http.route('/requisition/submit', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def submit_requisition(self, **post):
        # import from base
        values = _get_user_data()

        # ================= EMPLOYEE =================
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
        # name = employee.name or ''

        priority = post.get('priority')
        request_date = post.get('request_date') or False

        # ================= MAIN REQUISITION =================
        requisition = request.env['local.purchase.requisition'].sudo().create({
            'priority': priority,
            'requisitioned_by': request.env.user.id,
            'request_date': request_date,

            'department_id': employee.department_id.id if employee else False,
            'designation': employee.job_title if employee else '',
            'hr_id': employee.barcode if employee else '',
        })

        # ================= LINE DATA =================
        product_ids = request.httprequest.form.getlist('product_id')
        descriptions = request.httprequest.form.getlist('description')
        quantities = request.httprequest.form.getlist('required_qty')
        required_dates = request.httprequest.form.getlist('required_on')
        remarks_list = request.httprequest.form.getlist('remarks')

        # ================= LINE CREATE =================
        line_vals = []

        for i in range(len(product_ids)):

            product_id = product_ids[i]
            description = descriptions[i]

            #  skip only if BOTH empty
            if not product_id and not description:
                continue

            line_vals.append((0, 0, {
                'product_id': int(product_id) if product_id else False,
                'description': description or '',
                'required_qty': float(quantities[i] or 0),
                'required_on': required_dates[i] or False,
                'remarks': remarks_list[i] or '',
            }))

        # ================= WRITE LINES =================
        if line_vals:
            requisition.write({
                'line_ids': line_vals
            })

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)

        values.update({
            'requisition': requisition,
        })

        return request.render('purchase_requisition_tds.success-template', values)
