from odoo import http
from odoo.http import request
from datetime import date
from .base import BasePortalController


class DashboardController(BasePortalController,http.Controller):
    @http.route('/dashboard', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):
        # import from base
        values = self._get_user_data()

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''
        base_domain = [ ('create_uid', '=', user.id)]

        # all requisitions
        requisitions = request.env['local.purchase.requisition'].sudo().search(base_domain)
        # Forwarded
        forwarded_count = request.env['local.purchase.requisition'].sudo().search_count([
            *base_domain,
            '|',
            '|',
            ('state', '=', 'draft'),
            ('state', '=', 'forwarded'),
            ('state', '=', 'recommended')
        ])
        approved_count = request.env['local.purchase.requisition'].sudo().search_count([
            *base_domain,
            '|',
            ('state', '=', 'supplied'),
            ('state', '=', 'approved')
        ])
        cancelled_count = request.env['local.purchase.requisition'].sudo().search_count(base_domain + [('state', '=', 'cancelled')])
        # products = request.env['product.product'].sudo().search([])

        values.update({
            # 'products': products,
            'name': name,
            'today': date.today().strftime('%Y-%m-%d'),
            'requisitions':requisitions,
            'forwarded_count':forwarded_count,
            'approved_count': approved_count,
            'cancelled_count':cancelled_count,
        })

        return request.render('purchase_requisition_tds.portal_requisition_dashboard', values)