from odoo import models, fields, api
from odoo.exceptions import AccessError

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    approval_required = fields.Boolean(string="Approval Required", compute="_compute_approval_required", store=True)
    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Approval State", default="draft", tracking=True)

    @api.depends('total_amount')
    def _compute_approval_required(self):
        """Automatically mark an expense as requiring approval if above a threshold (e.g., 10,000 PKR)."""
        for record in self:
            record.approval_required = record.total_amount > 10000

    def action_submit_for_approval(self):
        """Change state to 'Waiting for Approval' and notify the manager."""
        for record in self:
            if record.approval_required:
                record.approval_state = 'waiting'
                record.send_manager_notification()
            else:
                record.approval_state = 'approved'

    def action_approve_expense(self):
        """Manager approves the expense."""
        for record in self:
            record.approval_state = 'approved'

    def action_reject_expense(self):
        """Manager rejects the expense."""
        for record in self:
            record.approval_state = 'rejected'

    def send_manager_notification(self):
        """Send an email notification to the manager for approval."""
        template = self.env.ref('expense_approval_workflow.email_template_expense_approval')
        if template:
            template.send_mail(self.id, force_send=True)

    def action_approve_expense(self):
        """Only managers can approve expenses."""
        if not self.env.user.has_group('hr_expense.group_hr_expense_manager'):
            raise AccessError("Only managers can approve expenses.")
        super(HrExpense, self).action_approve_expense()



