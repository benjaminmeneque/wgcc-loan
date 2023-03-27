# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LoanAmortization(models.Model):
    _name = 'wgcc.amortization'

    name = fields.Many2one('hr.employee', string='employee ID')
    loan_type = fields.Many2one('wgcc.loan.type', string="Loan Type")
    loan_amount = fields.Float('Loan Amount')
    gross_amount = fields.Float('Gross Amount')
    interest_rate = fields.Many2one('interest.rate', string='Interest Rate')
    term_of_months = fields.Integer('Term of Months')

    monthly_payment = fields.Float('Monthly Payment')
    number_of_payment = fields.Integer('No. of Payments')
    total_payment = fields.Integer('Total Payment')
    total_interest = fields.Float('Total Interest')

    share_capital = fields.Float('Share Capital')
    description = fields.Text('Description')
    other_loans = fields.Char('Other Loans') #OPTIONAL: SELECTION FIELD
    amount = fields.Float('Amount')
    savings = fields.Float('Savings')

    description = fields.Text('Description')
    amount = fields.Float('Amount')
   
    preview = fields.Html('')

    @api.onchange('term_of_months')
    def _onchange_(self):
        if self.term_of_months > self.loan_type.maximum_loan_term:
            raise ValidationError("Terms of months should not be greater than maximum term")
        if self.term_of_months < self.loan_type.minimum_loan_term:
             raise ValidationError("Terms of months should not be less than minimum term")

    @api.multi
    def generate_preview(self):
        report_name = 'loan.loan_amortization_report_template'
        report = self.env.ref(report_name)
        if not report:
            raise UserError(_('Report %s not found') % report_name)

        # Get the data to be passed to the report
        docids = self.ids
        docs = self.env['wgcc.amortization'].browse(docids)
        data = {'docs': docs}

        # Add the company_name field to the data dictionary
        # for doc in docs:
        #     data.update({
        #         'company_name': doc.company_name,
        #     })

        # Render the report and save the result in the preview field
        html = report.render(data)
        self.preview = html
        return True
    
    def clear(self):
        self.preview = ""
       


class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def name_get(self):
        res = []
        for employee in self:
            name = employee.identification_id or employee.name
            res.append((employee.id, name))
        return res