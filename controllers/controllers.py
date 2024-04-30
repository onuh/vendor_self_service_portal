# -*- coding: utf-8 -*-
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.portal.controllers.portal import CustomerPortal

# self service controller for vendors
class VendorSelfServicePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        vals = super()._prepare_home_portal_values(counters)
        vals['order_adjust'] = 'N/A';
        vals['product_forcast'] = 'N/A';
        return vals

    @http.route('/my/product_forcast', auth='user', website=True)
    def get_forcast_data(self, **kw):

        if kw and request.httprequest.method == 'POST':
            return {'success': True}

        #  search forcast from today to three months time which is a quater
        present = date.today()
        quarter_period = present + relativedelta(months=3)
        search_forcast = request.env['vendor.forecast'].sudo().search(['&', ('forcast_date', '>=', present),('forcast_date', '<=', quarter_period )])
        return request.render('vendor_self_service_portal.product_forcast_table', {'page_name': 'product_forcast', 'forcast_data': search_forcast})


    @http.route('/my/product_forcast_report', auth='user', csrf=False, website=True)
    def get_forcast_data_report(self, **kw):

        if kw and request.httprequest.method == 'POST':
            
            if kw['report_type'] == 'excel_report_many':

                # routine to download excel report
                response = request.make_response(None, headers=[('Content-Type', 'application/vnd.ms-excel'),('Content-Disposition', content_disposition('Forcast_Report' + '.xlsx'))])
                report_ids = json.loads(kw['report_ids'])
                report = request.env['vendor.forecast'].get_excel_report(report_ids, response)
                token = 'tfyiuohbugicv65tvfgu'
                response.set_cookie('fileToken', token)
                return response

            if kw['report_type'] == 'pdf_report_many':

                # convert javascript variable to python list to download pdf
                report_ids = json.loads(kw['report_ids'])
                report = request.env['vendor.forecast'].print_vendor_forcast_report(report_ids)
                return report

    # create adjustment to sale order request
    @http.route('/my/order_adjustment', auth='user', website=True)
    def create_adjustment(self, **kw):
        partner = request.env.user.partner_id
        sale_request = request.env['sale.order'].sudo().search([('partner_id', '=', partner.id)])
        return request.render('vendor_self_service_portal.order_adjustment_step_form', {'order_id': sale_request, 'page_name': 'order_adjust_request'})

    @http.route("/my/submit_order_adjustment", type="json", auth="public", website=True)
    def submit_details(self, **kw):
        submission_model = request.env['vendor.adjustment.request'].sudo()
        create = submission_model.create(kw)
        if create.id:
            return {'success': True}
        else:
            return {'success': False}
