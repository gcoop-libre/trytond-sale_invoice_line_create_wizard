# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SaleInvoiceLineCreateWizard(ModuleTestCase):
    'Test module'
    module = 'sale_invoice_line_create_wizard'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleInvoiceLineCreateWizard))
    return suite
