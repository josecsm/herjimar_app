import frappe
import json
import subprocess
import os

@frappe.whitelist(allow_guest=True)
def informe(values):

    obj = json.loads(values)
   
    args = 'cd /var/www/html/erpnext && php artisan generar:plantilla_riesgos "'+obj["proyecto"]+'"'
    so = os.popen(args).read()
    return so
