import frappe
import json
import subprocess
import os


@frappe.whitelist(allow_guest=True)
def get_sharepoint(proyecto):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:sharepoint_proyecto "'+proyecto+'"'
	so = os.popen(args).read()
	html="<ul>"
	if (len(so)>1):
		try:
			obj = json.loads(so)	
			for item in obj:
				if (item["tipo"]=="C") :
					html=html+"<li><i class='fa fa-folder'></i>&nbsp;<a target='_blank' href='"+item["url"]+"'>"+item["nombre"]+"</a></li>"
				else:
					html=html+"<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class='fa fa-file'></i>&nbsp;<a target='_blank' href='"+item["url"]+"'>"+item["nombre"]+"</a></li>"
		except json.decoder.JSONDecodeError:
			pass
	html=html+"</ul><BR><BR>"
	return html

@frappe.whitelist(allow_guest=True)
def importar_odfs_xgest_js(name):

	for hv in frappe.db.get_list('Hoja Verde',filters={
        'proyecto': name
    }):
		doc = frappe.get_doc('Hoja Verde', hv.name)
		doc.importar_odfs_xgest()

@frappe.whitelist(allow_guest=True)
def get_hojas_verdes(doctype, name, links):
	'''Get open count for given transactions and filters

	:param doctype: Reference DocType
	:param name: Reference Name
	:param transactions: List of transactions (json/dict)
	:param filters: optional filters (json/list)'''

	frappe.has_permission(doc=frappe.get_doc(doctype, name), throw=True)
	meta = frappe.get_meta(doctype)
	links = frappe._dict({
		'fieldname': 'proyecto',
		'transactions': [
			{
				'label': 'Hoja Verde',
				'items': ['Hoja Verde']
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
		data['count'] = frappe.db.count('Hoja Verde', {'proyecto': name})
		out.append(data)

	out = {
		'count': out,
	}

	#module = frappe.get_meta_module(doctype)
	#if hasattr(module, 'get_timeline_data'):
	#	out['timeline_data'] = module.get_timeline_data(doctype, name)
    
	return out
