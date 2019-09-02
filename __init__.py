# This file is part of the sale_invoice_line_create_wizard module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice

__all__ = ['register']


def register():
    Pool.register(
        invoice.CreateInvoicesStart,
        module='sale_invoice_line_create_wizard', type_='model')
    Pool.register(
        invoice.CreateInvoices,
        module='sale_invoice_line_create_wizard', type_='wizard')
