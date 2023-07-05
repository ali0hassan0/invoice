from datetime import datetime

from odoo import models, fields, api
import json


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_totals(self):
        for rec in self:
            return json.loads(rec.tax_totals_json)['amount_total']

    def get_date(self):
        for rec in self:
            return rec.invoice_payments_widget.get('date')

    def get_source(self):
        for rec in self:
            if rec.request:
                return rec.request
            elif rec.invoice_origin:
                so = self.env['sale.order'].search([('name', '=', rec.invoice_origin)])
                if so:
                    return so.name
            return False

    def get_invoice_payments_amount(self):
        for rec in self:
            invoice_payments_widget = rec.invoice_payments_widget
            if invoice_payments_widget:
                payments_dict = json.loads(invoice_payments_widget)
                content_list = payments_dict.get('content', [])
                if content_list:
                    first_payment = content_list[0]
                    amount = first_payment.get('amount', 0.0)
                    return amount
        return 0.0

    def get_invoice_payments_date(self):
        for rec in self:
            invoice_payments_widget = rec.invoice_payments_widget
            if invoice_payments_widget:
                payments_dict = json.loads(invoice_payments_widget)
                content_list = payments_dict.get('content', [])
                if content_list:
                    first_payment = content_list[0]
                    date_str = first_payment.get('date')
                    if date_str:
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        formatted_date = date.strftime('%m/%d/%Y')
                        return formatted_date
        return False

    def get_invoice_payment_type(self):
        for rec in self:
            invoice_payments_widget = rec.invoice_payments_widget
            if invoice_payments_widget:
                payments_dict = json.loads(invoice_payments_widget)
                content_list = payments_dict.get('content', [])
                if content_list:
                    first_payment = content_list[0]
                    account_payment_id = first_payment.get('account_payment_id')
                    if account_payment_id:
                        payment = self.env['account.payment'].browse(account_payment_id)
                        payment_type = payment.journal_id.type
                        return payment_type
        return ''

