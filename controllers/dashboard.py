from odoo import http
from odoo.http import request
from datetime import date
from .base import BasePortalController


class DashboardController(BasePortalController):
    @http.route('/dashboard', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):
        # import from base
        values = self._get_user_data()

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''

        requisition = request.env['local.purchase.requisition'].sudo().search([], limit=1)
        products = request.env['product.product'].sudo().search([])

        values.update({
            'sl_number' : requisition.name,
            'products': products,
            'name': name,
            'today': date.today().strftime('%Y-%m-%d'),
        })

        return request.render('purchase_requisition_tds.portal_requisition_dashboard', values)