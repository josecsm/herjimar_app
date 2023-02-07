import frappe
import os
import json

@frappe.whitelist(allow_guest=True)
def get_sharepoint(oc):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:sharepointeq "'+oc+'"'
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

