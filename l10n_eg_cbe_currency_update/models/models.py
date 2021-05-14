# -*- coding: utf-8 -*-

import logging
from odoo import models, api, fields, exceptions
from odoo.addons.iap import jsonrpc
from odoo.addons.iap.models import iap


DEFAULT_ENDPOINT = 'https://cbe-currency-update-service-tmz24rud7q-lz.a.run.app/api/v2/jsonrpc'
_logger = logging.getLogger(__name__)


class CBECurrencyUpdate(models.Model):
    _name = 'cbe.currency.update'
    _description = "CBE Currency Updater"

    @api.model
    def cbe_currency_update(self):
        _logger.info('Fetching currency update from CBE')
        user_token = self.env['iap.account'].get('cbe_currency_updates')
        supported_currencies = (
            'USD', 'EUR', 'GBP', 'CAD', 'DKK', 'NOK',
            'SEK', 'CHF', 'JPY', 'SAR', 'KWD', 'AED',
            'AUD', 'BHD', 'OMR', 'QAR', 'JOD', 'CNY'
        )
        params = {
            'account_token': user_token.account_token,
        }
        endpoint = self.env['ir.config_parameter'].sudo().get_param(
            'currency.endpoint', DEFAULT_ENDPOINT)
        try:
            result = jsonrpc(endpoint + '/call', params=params)
        except iap.InsufficientCreditError:
            raise exceptions.ValidationError("Insufficient Credit. Please buy credits from General Settings menu!")
        for index in range(len(supported_currencies)):
            currency = supported_currencies[index]
            currency_obj = self.env['res.currency'].search([
                ('name', '=', currency), ('active', '=', True)
            ], limit=1)
            if currency_obj:
                rate_id = currency_obj.rate_ids.filtered(lambda x: x.name == fields.Date.today())
                if not rate_id:
                    _logger.info('No rates for today {}. Updating!'.format(fields.Date.today()))

                    result = result['result']
                    # buy_price = 1.0 / round(float(span[0].text), 9)
                    sell_price = 1.0 / round(float(result[currency]), 9)
                    _logger.info('Updated currency {} with rate: {}'.format(
                        currency_obj.name, float(result[currency])))
                    try:
                        self.env['res.currency.rate'].create({
                            'name': fields.Date.today(),
                            'rate': sell_price,
                            'currency_id': currency_obj.id,
                        })
                    except Exception:
                        _logger.warning('Error creating new rate for today {}'.format(fields.Date.today()))
                        self.env.cr.commit()
                        pass
