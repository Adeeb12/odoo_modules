{
    'name': 'Payment Report',
    'version': '1.0',
    'summary': 'Customer Payment Details',
    'category': '',
    'license': '',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'report/payment_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
