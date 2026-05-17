{
    'name': 'Purchase Requisition TDS',
    'version': '0.1',
    'category': 'Purchase',
    'summary': 'Internal Purchase Requisition',
    'author': 'A.T.M Shamiul Bashir',
    'depends': [
        'base',
        'mail',
        'hr',
        'product',
        'purchase',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/requisition_views.xml',

       # Portal Templates Here
        'templates/index.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
    'images': ['static/src/img/icon.png'],
    'icon': "/purchase_requisition_tds/static/src/img/icon.png",
}
