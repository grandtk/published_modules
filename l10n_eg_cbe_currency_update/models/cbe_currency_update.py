import logging

from odoo import api, fields, models
from odoo.addons.iap.tools import iap_tools

_logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = 'https://cbe-currency-update-service-tmz24rud7q-lz.a.run.app/api/v2/jsonrpc'
IAP_SERVICE_NAME = 'cbe_currency_updates'
SUPPORTED_CURRENCIES = (
    'USD', 'EUR', 'GBP', 'CAD', 'DKK', 'NOK',
    'SEK', 'CHF', 'JPY', 'SAR', 'KWD', 'AED',
    'AUD', 'BHD', 'OMR', 'QAR', 'JOD', 'CNY',
)


class CBECurrencyUpdate(models.AbstractModel):
    _name = 'cbe.currency.update'
    _description = "CBE Currency Updater"

    @api.model
    def _cbe_fetch_rates(self):
        """Return {currency_code: EGP per 1 unit of currency} from the IAP service."""
        account = self.env['iap.account'].get(IAP_SERVICE_NAME)
        endpoint = self.env['ir.config_parameter'].sudo().get_param(
            'currency.endpoint', DEFAULT_ENDPOINT)
        response = iap_tools.iap_jsonrpc(
            endpoint + '/call', params={'account_token': account.account_token})
        # iap_jsonrpc already unwraps the JSON-RPC envelope; the CBE service
        # nests the rates under a further 'result' key (as the 12/14 code assumed).
        if isinstance(response, dict) and isinstance(response.get('result'), dict):
            response = response['result']
        return response or {}

    @api.model
    def cbe_currency_update(self):
        _logger.info('Fetching currency update from CBE')
        rates = self._cbe_fetch_rates()
        if not rates:
            _logger.warning('CBE service returned no rates')
            return False

        today = fields.Date.today()
        egp = self.env.ref('base.EGP', raise_if_not_found=False)
        companies = self.env['res.company'].sudo().search(
            [('currency_id', '=', egp.id)] if egp else [])
        currencies = self.env['res.currency'].search([
            ('name', 'in', SUPPORTED_CURRENCIES), ('active', '=', True)])
        Rate = self.env['res.currency.rate'].sudo()

        for company in companies:
            for currency in currencies:
                try:
                    value = float(rates[currency.name])
                    if value <= 0:
                        raise ValueError('non-positive rate')
                except (KeyError, TypeError, ValueError):
                    _logger.warning('No valid CBE rate for %s, skipping', currency.name)
                    continue
                if Rate.search_count([
                    ('currency_id', '=', currency.id),
                    ('name', '=', today),
                    ('company_id', '=', company.id),
                ]):
                    continue
                try:
                    with self.env.cr.savepoint():
                        Rate.create({
                            'name': today,
                            'rate': 1.0 / value,
                            'currency_id': currency.id,
                            'company_id': company.id,
                        })
                    _logger.info('Updated %s for %s with rate %s',
                                 currency.name, company.name, value)
                except Exception:
                    _logger.exception('Error creating rate for %s on %s', currency.name, today)
        return True
