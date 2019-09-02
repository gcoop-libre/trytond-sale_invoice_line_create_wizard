# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.sale_invoice_line_create_wizard.tests.test_sale_invoice_line_create_wizard import suite
except ImportError:
    from .test_sale_invoice_line_create_wizard import suite

__all__ = ['suite']
