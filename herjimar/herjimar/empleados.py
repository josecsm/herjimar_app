from argparse import _SubParsersAction
import frappe
import subprocess
import os
import json

@frappe.whitelist(allow_guest=True)
def obtener_roles():
    return frappe.get_roles(frappe.user)

@frappe.whitelist(allow_guest=True)
def generar_ids(empleados):
    so=""
    json_data = json.loads(empleados)
    for x in json_data:
       so=so+'@@'+x['name']
    args = 'cd /var/www/html/erpnext && php artisan generar:recibo_ids "'+so+'"'
    so = os.popen(args).read()
    return so

@frappe.whitelist(allow_guest=True)
def ver_informe():
    args = 'cd /var/www/html/erpnext && php artisan generar:listado_empleados'
    so = os.popen(args).read()
    return so

@frappe.whitelist(allow_guest=True)
def ver_informe_vacaciones(desde,hasta):
    args = 'cd /var/www/html/erpnext && php artisan generar:informe_vacaciones "'+desde+'" "'+hasta+'"'
    so = os.popen(args).read()
    return so


@frappe.whitelist(allow_guest=True)
def getempleados(term=None,_type=None,q=None):
    if ((term == None) or (term =='')) :
        return {"results":[]}
    else:
        out = []
        odfs=frappe.db.get_list('Employee', page_length=20,filters={
        'name': ['like', '%'+term+'%'],
        'status': ["!=", "Left"]
        },fields=['name'])
        for odf in odfs:
            
            out.append({
            "id": odf.name,
            "text": odf.name,
        })
        return {"results":out}
