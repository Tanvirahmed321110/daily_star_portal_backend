from odoo import http, SUPERUSER_ID
from odoo.http import request
from datetime import date
from odoo.addons.web.controllers.home import Home

class RequisitionPortal(Home):
    # =============== Default Route Odoo  ==================
    @http.route('/web/login', type='http', auth='public', website=True, sitemap=False)
    def web_login(self, redirect=None, **kw):

        # Odoo original login
        response = super().web_login(redirect=redirect, **kw)

        # POST request এ login হলে (actual login submit)
        if request.httprequest.method == 'POST' and request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                return request.redirect('/requisition')

        return response




    #=============== For Portal Main Controller  ==================
    @http.route('/requisition', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):

        user = request.env.user

        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''
        print(employee)

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)
        products = request.env['product.product'].sudo().search([])

        values = {
            'requisition': requisition,
            'products': products,
            'name': name,
            'designation': employee.job_id.name or '—',
            'department': employee.department_id.name or '—',
            'hr_id': employee.barcode or '—',
            'work_email': employee.work_email or '—',
            'employee_image': employee.image_128 if employee and employee.image_128 else False,
            'today': date.today().strftime('%Y-%m-%d'),
        }

        return request.render('purchase_requisition_tds.portal_requisition_form', values)





    #=============  For Data Submit  =============
    @http.route('/requisition/submit',type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def submit_requisition(self, **post):

        # ================= EMPLOYEE =================
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
        name = employee.name or ''


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

        return request.render('purchase_requisition_tds.success-template',{
            'name': name,
            'requisition':requisition,
            'work_email': employee.work_email or '—',
            'employee_image': employee.image_128 if employee and employee.image_128 else False,
            'designation': employee.job_id.name or '—',
            'department': employee.department_id.name or '—',
            'hr_id': employee.barcode or '—',
        })
