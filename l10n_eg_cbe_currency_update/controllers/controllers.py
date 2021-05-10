# -*- coding: utf-8 -*-
from odoo import http

# class CbeCurrencyUpdate(http.Controller):
#     @http.route('/l10n_eg_cbe_currency_update/l10n_eg_cbe_currency_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_eg_cbe_currency_update/l10n_eg_cbe_currency_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_eg_cbe_currency_update.listing', {
#             'root': '/l10n_eg_cbe_currency_update/l10n_eg_cbe_currency_update',
#             'objects': http.request.env['l10n_eg_cbe_currency_update.l10n_eg_cbe_currency_update'].search([]),
#         })

#     @http.route('/l10n_eg_cbe_currency_update/l10n_eg_cbe_currency_update/objects/<model("l10n_eg_cbe_currency_update.l10n_eg_cbe_currency_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_eg_cbe_currency_update.object', {
#             'object': obj
#         })