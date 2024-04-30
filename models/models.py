# -*- coding: utf-8 -*-
import base64
import random
import io
import xlsxwriter
from odoo import models, fields, api


class vendorForcastService(models.Model):

    # create vendor forcast model
    _name = 'vendor.forecast'
    _description = 'forcast sales'


    # define fields
    product_id = fields.Many2one('product.product', 'Product Name')
    expected_quantity = fields.Integer("Expected Quantity")
    forcast_date = fields.Date('Forecast Date')

    # server action function to download pdf report
    def print_vendor_forcast_report(self, data=None):
        if data:
            data_bin = self.env['ir.actions.report']._render_qweb_pdf('vendor_self_service_portal.action_report_vendor_cert', res_ids=data)
            data_bin1 = base64.b64encode(data_bin[0])
            randnum = random.randint(1, 10000)
            attachment_id = self.env['ir.attachment'].sudo().create({'name': 'Forcast_Report_'+str(randnum)+'.pdf', 'type': 'binary', 'datas': data_bin1, 'store_fname': 'Forcast_Report_'+str(randnum)+'.pdf', 'public': True, 'mimetype': 'application/x-pdf'})
            download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
            return download_url
        return self.env.ref('vendor_self_service_portal.action_report_vendor_cert').report_action(self, data=data)

    # function to get lines for excel download
    def _get_report_lines(self, options):
        lines = []
        report_data = self.env['vendor.forecast'].browse(options)
        for report in report_data:
            line = {
            'product_name': report.product_id.name, 
            'expected_quantity': report.expected_quantity, 
            'forcast_date': report.forcast_date,
            }
            lines.append(line)
        return lines

    # utilize excel function to write data to excel file
    def get_excel_report(self, options, response):

        try:
            report_lines = self.env['vendor.forecast']._get_report_lines(options)
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet('product demand forcast')
            def_style = workbook.add_format({'font_name': 'Arial'})
            date_style = workbook.add_format({'font_name': 'Arial', 'num_format': 'yyyy-mm-dd'})
            num_style = workbook.add_format({'font_name': 'Arial', 'num_format': '#,##0'})
            title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2})
            sheet.set_column(0, 0, 25)  # Set the first column width to 15
            sheet.set_column(1, 1, 25)  # Set the second column width to 15
            sheet.set_column(2, 2, 25)  # Set the third column width to 15

            row = 1

            sheet.write(row, 0, "Product Name", title_style)
            sheet.write(row, 1, "Expected Quantity", title_style)
            sheet.write(row, 2, "Forcast Date", title_style)
            for d in report_lines:
                row += 1
                sheet.write(row, 0, str(d['product_name']), def_style)
                sheet.write(row, 1, d['expected_quantity'], num_style)
                sheet.write(row, 2, d['forcast_date'], date_style)

            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()

        except Exception as e:

            print("Exception: ", e)




class vendorAdjustmentRequestService(models.Model):

    # create vendor adjustment request model
    _name = 'vendor.adjustment.request'
    _description = 'Order adjustment '
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin'] # inherit models to be used in chatter to know user that created record

    # define fields
    name = fields.Char("Name", compute='_compute_name', store=True)
    order_id = fields.Many2one('sale.order', 'Sale Order')
    adjustment_detail = fields.Text("Adjustment Details")
    comment = fields.Text('Comment')


    # crud method create for ORM
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            order = self.env['sale.order'].sudo().search([('id', '=', vals.get('order_id'))], limit=1)
            vals['name'] = order.name

            # send email to all users in procurement team
            email_values = {'portal_user_name': self.env.user.name, 'sale_order_number': order.name}

            # mail template details
            template_id = self.env.ref('vendor_self_service_portal.mail_template_sale_adjust_notify').id
            template = self.env['mail.template'].browse(template_id)

            #  get all users and filter out users with procurement group. I assume these are users managing stock
            all_users = self.env['res.users'].sudo().search([])
            for user in all_users:
                if user.has_group('stock.group_stock_user'):
                    print("User has group: ", user.name)
                    # send email to stock user using template
                    template.with_context(email_values).send_mail(user.id, force_send=True)

        return super().create(vals_list)


class VendorForcastReport(models.AbstractModel):

    # report model
    _name = 'report.vendor_self_service_portal.report_vendor'
    _description = 'Vendor Forcast Report'

    # api to pass data from model to report template
    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'vendor.forecast'
        docs = self.env[model].browse(self.env.context.get('active_ids', docids))

        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }

class ResUsers(models.Model):
    # inherit so we reference in mail template
    _inherit = 'res.users'

