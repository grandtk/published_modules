from unittest.mock import patch

from odoo import fields
from odoo.tests import TransactionCase, tagged

MODEL = 'odoo.addons.l10n_eg_cbe_currency_update.models.cbe_currency_update.CBECurrencyUpdate'


@tagged('post_install', '-at_install')
class TestCBECurrencyUpdate(TransactionCase):

    def setUp(self):
        super().setUp()
        self.egp = self.env.ref('base.EGP')
        self.egp.active = True
        self.company = self.env['res.company'].create({
            'name': 'EG Co', 'currency_id': self.egp.id})
        self.usd = self.env.ref('base.USD')
        self.usd.active = True
        self.eur = self.env.ref('base.EUR')
        self.eur.active = True

    def _run(self, rates):
        with patch(MODEL + '._cbe_fetch_rates', return_value=rates):
            self.env['cbe.currency.update'].cbe_currency_update()

    def _rate(self, currency):
        return self.env['res.currency.rate'].search([
            ('currency_id', '=', currency.id),
            ('company_id', '=', self.company.id),
            ('name', '=', fields.Date.today())])

    def test_creates_rates_for_several_currencies(self):
        self._run({'USD': 50.0, 'EUR': 25.0})
        self.assertAlmostEqual(self._rate(self.usd).rate, 1 / 50.0)
        self.assertAlmostEqual(self._rate(self.eur).rate, 1 / 25.0)

    def test_idempotent_and_bad_values_skipped(self):
        self._run({'USD': 50.0, 'EUR': 0})
        self._run({'USD': 60.0})
        self.assertEqual(len(self._rate(self.usd)), 1)
        self.assertAlmostEqual(self._rate(self.usd).rate, 1 / 50.0)
        self.assertFalse(self._rate(self.eur))
