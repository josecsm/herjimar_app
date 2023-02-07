import frappe
import json

@frappe.whitelist(allow_guest=True)
def importar_odfs_xgest_js(name):
	doc = frappe.get_doc('Hoja Verde', name)
	doc.importar_odfs_xgest()


@frappe.whitelist(allow_guest=True)
def get_odfs(doctype, name, links):
	'''Get open count for given transactions and filters

	:param doctype: Reference DocType
	:param name: Reference Name
	:param transactions: List of transactions (json/dict)
	:param filters: optional filters (json/list)'''

	frappe.has_permission(doc=frappe.get_doc(doctype, name), throw=True)
	meta = frappe.get_meta(doctype)
	links = frappe._dict({
		'fieldname': 'hoja_verde',
		'transactions': [
			{
				'label': 'Task',
				'items': ['Task']
			},
		]
	})
	items = []
	for group in links.transactions:
		items.extend(group.get('items'))

	out = []
	for d in items:
		
		data = {'name': d}
		#total = len(frappe.get_all(d, fields='name',
			#filters={fieldname: name}, limit=100, distinct=True, ignore_ifnull=True))
		data['count'] = frappe.db.count('Task', {'hoja_verde': name})
		out.append(data)

	out = {
		'count': out,
	}

	#module = frappe.get_meta_module(doctype)
	#if hasattr(module, 'get_timeline_data'):
	#	out['timeline_data'] = module.get_timeline_data(doctype, name)
    
	return out
