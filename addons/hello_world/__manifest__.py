{
    'name': 'Hello World',
    'version': '19.0.1.0.0',
    'summary': 'A simple Hello World module',
    'description': 'A simple Hello World module for testing.',
    'category': 'Extra Tools',
    'author': 'Kerrick',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hello_world_views.xml',
    ],
    'installable': True,
    'application': True,
}
