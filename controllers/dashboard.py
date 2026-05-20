from odoo import http
from odoo.http import request
from datetime import date
from .base import _get_user_data


class DashboardController(http.Controller):
    @http.route('/dashboard', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, **kw):
        # import from base
        values = _get_user_data()

        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        name = employee.name or ''
        base_domain = [ ('create_uid', '=', user.id)]

        # all requisitions
        requisitions = request.env['local.purchase.requisition'].sudo().search(base_domain)
        # requisition_count = {}
        # for requisition in requisitions:
        #     count = len(requisition.line_ids)
        #     count = request.env["local.purchase.requisition.lines"].sudo().search_cout([("requisition_id", '=', requisition.id)])
        #     requisition_count[requisition.id] = count
        #     {
        #         1 : 5,
        #         2 : 7
        #
        #     }

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