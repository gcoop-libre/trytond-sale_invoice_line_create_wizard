# This file is part of the sale_invoice_line_create_wizard module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    sale_party = fields.Function(fields.Many2One('party.party', 'Party',
        context={'company': Eval('company', -1)}, depends={'company'}),
        'get_sale_party', searcher='search_sale_party')
    sale_agent = fields.Function(fields.Many2One('party.party', 'Agent',
        context={'company': Eval('company', -1)}, depends={'company'}),
        'get_sale_agent', searcher='search_sale_agent')

    def get_sale_party(line, name):
        if line.sale:
            return line.sale.party.id
        return None

    def get_sale_agent(line, name):
        if line.sale and line.sale.agent:
            return line.sale.agent.id
        return None

    @classmethod
    def search_sale_party(self, name, domain):
        return [('sale.party',) + tuple(domain[1:])]

    @classmethod
    def search_sale_agent(self, name, domain):
        return [('sale.agent',) + tuple(domain[1:])]
