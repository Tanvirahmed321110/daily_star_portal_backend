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
            'requisition': requisition,
            'products': products,
            'name': name,
            'initials': initials,
            'designation': employee.job_id.name or '—',
            'department': employee.department_id.name or '—',
            'hr_id': employee.barcode or '—',
            'work_email': employee.work_email or '—',
            'employee_image': '/web/image/hr.employee/%s/image_128' % employee.id if employee else '',
            'today': date.today().strftime('%Y-%m-%d'),
        }

        return request.render('purchase_requisition_tds.portal_requisition_form', values)


    #=============  For Data Submit  =============
    @http.route('/submit/requisition',type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def submit_requisition(self, **post):

        # ================= EMPLOYEE =================
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

        priority = post.get('priority')
        request_date = post.get('request_date') or False

        # ================= MAIN REQUISITION =================
        requisition = request.env['local.purchase.requisition'].sudo().create({
            'priority': priority,
            'requisitioned_by': request.env.user.id,
            'request_date': request_date,

            # EMPLOYEE DATA
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

            # 👉 skip only if BOTH empty
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

        return request.redirect('/requisition')
