from odoo import models, fields, api
from odoo.exceptions import UserError


class LocalPurchaseRequisition(models.Model):
    _name = 'local.purchase.requisition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Local Purchase Requisition'
    _rec_name = 'name'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        default='New'
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self._default_employee()
    )

    designation = fields.Char(string='Designation')
    department_id = fields.Many2one('hr.department', string='Department')
    hr_id = fields.Char(string='HR ID')

    request_date = fields.Date(
        default=fields.Date.today
    )

    supplied_deadline = fields.Date()

    supplied_date = fields.Date()

    priority = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ], default='medium')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('forwarded', 'Forwarded'),
        ('recommended', 'Recommended'),
        ('approved', 'Approved'),
        ('supplied', 'Supplied'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    line_ids = fields.One2many(
        'local.purchase.requisition.line',
        'requisition_id',
        string='Lines'
    )

    requisitioned_by = fields.Many2one('res.users')
    forwarded_by = fields.Many2one('res.users')
    supplied_by = fields.Many2one('res.users')
    recommended_by = fields.Many2one('res.users')
    approved_by = fields.Many2one('res.users')
    received_by = fields.Many2one('res.users')

    @api.model
    def _default_employee(self):
        return self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ], limit=1)

    @api.onchange('employee_id')
    def _onchange_employee(self):
        for rec in self:
            rec.designation = rec.employee_id.job_title or ''
            rec.department_id = rec.employee_id.department_id.id
            rec.hr_id = rec.employee_id.barcode or ''

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'local.purchase.requisition'
            ) or 'New'
        return super().create(vals)

    def action_forward(self):
        self.write({
            'state': 'forwarded',
            'forwarded_by': self.env.user.id
        })

    def action_recommend(self):
        self.write({
            'state': 'recommended',
            'recommended_by': self.env.user.id
        })

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id
        })

    def action_supply(self):
        self.write({
            'state': 'supplied',
            'supplied_by': self.env.user.id,
            'supplied_date': fields.Date.today()
        })

    def action_reset(self):
        self.state = 'draft'


class LocalPurchaseRequisitionLine(models.Model):
    _name = 'local.purchase.requisition.line'
    _description = 'Requisition Line'

    requisition_id = fields.Many2one(
        'local.purchase.requisition',
        ondelete='cascade'
    )

    sequence = fields.Integer(default=10)

    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )

    description = fields.Char(string='Writing Option')

    required_qty = fields.Float()

    required_on = fields.Date()

    last_supplied_on = fields.Date()

    last_supplied_qty = fields.Float()

    returned_on = fields.Date()

    returned_qty = fields.Float()

    rate = fields.Float()

    value = fields.Float(
        compute='_compute_value',
        store=True
    )

    remarks = fields.Char()

    available_qty = fields.Float(
        string='Available Qty'
    )

    def _compute_value(self):
        for rec in self:
            rec.value = rec.required_qty * rec.rate
