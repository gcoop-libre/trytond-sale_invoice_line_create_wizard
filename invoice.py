# This file is part of the sale_invoice_line_create_wizard module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from itertools import groupby

from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.wizard import Wizard, StateView, StateAction, Button

__all__ = ['InvoiceLine', 'CreateInvoicesStart', 'CreateInvoices']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'


class CreateInvoicesStart(ModelView):
    'Create Invoices Start'
    __name__ = 'sale_invoice_line_create_wizard.create_invoices.start'

    date = fields.Date('Date')

    @staticmethod
    def default_date():
        Date = Pool().get('ir.date')
        return Date.today()


class CreateInvoices(Wizard):
    'Create Invoices'
    __name__ = 'sale_invoice_line_create_wizard.create_invoices'
    start = StateView('sale_invoice_line_create_wizard.create_invoices.start',
        'sale_invoice_line_create_wizard.create_invoices_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('OK', 'create_invoices', 'tryton-ok', True),
            ])
    create_invoices = StateAction('account_invoice.act_invoice_form')

    def do_create_invoices(self, action):
        pool = Pool()
        SaleLine = pool.get('sale.line')
        sale_lines = SaleLine.search([
                ('manual_delivery_date', '<=', self.start.date),
                ('invoice_lines', '!=', None),
                ('sale.state', '=', 'processing'),
                ])
        invoice_lines = []
        for sale_line in sale_lines:
            for invoice_line in sale_line.invoice_lines:
                if invoice_line.invoice is None:
                    invoice_lines.append(invoice_line)

        invoices = self._invoice(invoice_lines)

        data = {'res_id': [c.id for c in invoices]}
        if len(invoices) == 1:
            action['views'].reverse()
        return action, data

    @classmethod
    def _group_invoice_key(cls, invoice_line):
        '''
        The key to group invoice_lines by Invoice
        '''
        grouping = [
            ('party', invoice_line.party),
            ('company', invoice_line.company),
            ('currency', invoice_line.currency),
            ('type', invoice_line.invoice_type),
            ('invoice_date', invoice_line.origin.manual_delivery_date),
            ('account', invoice_line.party.account_receivable),
            ]
        return grouping

    @classmethod
    def _get_invoice(cls, keys):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        values = dict(keys)
        values['invoice_address'] = values['party'].address_get('invoice')
        invoice = Invoice(**values)
        invoice.on_change_type()
        return invoice

    @classmethod
    def _invoice(cls, lines):
        pool = Pool()
        Invoice = pool.get('account.invoice')

        if not lines:
            return []
        lines = sorted(lines, key=cls._group_invoice_key)

        invoices = []
        for key, grouped_lines in groupby(lines, key=cls._group_invoice_key):
            invoice = cls._get_invoice(key)
            invoice.lines = (list(getattr(invoice, 'lines', [])) +
                list(x for x in grouped_lines))
            invoices.append(invoice)

        invoices = Invoice.create([x._save_values for x in invoices])
        Invoice.update_taxes(invoices)
        return invoices
