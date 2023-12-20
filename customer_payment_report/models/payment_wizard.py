from odoo import api, fields, models, _
from datetime import date, datetime

class PaymentWizard(models.TransientModel):
    _name = "customer.payment.report"

    date_from = fields.Date(string="From :")
    date_to = fields.Date(string="To :")

    def action_print_report(self):
        print('something----')
        return {
            'type': 'ir.actions.report',
            'report_name': 'customer_payment_report.customer_payment_report_template',
            'model': 'customer.payment.report',
            'report_type': "qweb-pdf",
        }

    def get_customer_payments(self):
        # payments = self.env['account.payment'].search([])
        # query = """
        #     SELECT *, rp.name as partner_name
        #     FROM account_payment ap
        #     Left join res_partner rp on rp.id = ap.partner_id
        # """
        # params = {
        #     'start_date': self.date_from,
        #     'end_date': self.date_to,
        # }
        # start_date = datetime.combine(self.date_from, datetime.min.time())
        start_date = self.date_from.strftime("%Y-%m-%d")
        end_date = self.date_to.strftime("%Y-%m-%d")
        # end_date = datetime.combine(self.date_to, datetime.min.time())
        # params = (datetime.combine(self.date_from, datetime.min.time()),datetime.combine(self.date_to, datetime.min.time()))
        # query = """SELECT
        #         rp.id AS customer_id,
        #         rp.name AS customer_name,
        #         COUNT(DISTINCT so.id) AS total_sale_orders,
        #         MIN(so.date_order) AS first_sale_order_date,
        #         SUM(sol.price_subtotal) AS total_amount,
        #         SUM(sol.price_total) AS total_paid_amount,
        #         SUM(sol.price_total) - SUM(p.amount) AS balance_amount
        #         FROM
        #             res_partner rp
        #         LEFT JOIN   
        #             sale_order so ON rp.id = so.partner_id
        #         LEFT JOIN
        #             sale_order_line sol ON so.id = sol.order_id
        #         LEFT JOIN
        #             account_payment p ON c.id = p.partner_id
        #         WHERE
        #         c.customer_rank > 0
        #             AND so.date_order >= %s
        #             AND so.date_order <= %s
        #         GROUP BY
        #             c.id, c.name
        #         ORDER BY
        #             c.name;
        #     """

        query = """ SELECT
                p.name AS customer_name,
                COUNT(m.id) AS total_sale_orders,
                SUM(m.amount_total) AS total_amount,
                MIN(m.invoice_date) AS first_sale_order_date,
                SUM(CASE WHEN m.move_type IN ('out_invoice', 'out_refund') THEN m.amount_total ELSE 0 END) AS total_amount
            FROM
                account_move m
            JOIN
                res_partner p ON m.partner_id = p.id
            WHERE
                m.invoice_date BETWEEN %s AND %s
                AND m.move_type IN ('out_invoice', 'out_refund')
            GROUP BY
                p.name"""

        print(start_date,end_date, '\n',query)
        params = (start_date, end_date)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        print('-------------', result)
        return result
