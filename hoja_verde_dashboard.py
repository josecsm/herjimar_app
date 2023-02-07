from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'número',
		'transactions': [
			{
				'label': _('Gestion'),
				'items': ['Task']
			},
		]
	}
