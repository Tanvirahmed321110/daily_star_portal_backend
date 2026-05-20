from odoo import http
from odoo.http import request
from .base import _get_user_data


class RequisitionDetailsController(http.Controller):
    @http.route('/dashboard/requisition_details/<int:req_id>', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def requisition_form(self, req_id,**kw):

        # import from base
        values = _get_user_data()

        # user = request.env.user
        # employee = request.env['hr.employee'].sudo().search([
        #     ('user_id', '=', user.id)
        # ], limit=1)

        requisition = request.env['local.purchase.requisition'].sudo().browse(req_id)
        # requisition lines fetch
        requisition_lines = request.env['local.purchase.requisition.line'].sudo().search([
            ('requisition_id', '=', req_id)
        ])

        breadcrumb = [
            {'name': 'Dashboard', 'url': '/dashboard'},
            {'name': 'Requisition Details', 'url': False},
        ]

        values.update({
            'breadcrumb': breadcrumb,
            'requisition': requisition,
            'requisition_lines':requisition_lines,
        })

        return request.render('purchase_requisition_tds.portal_requisition_details',values)
