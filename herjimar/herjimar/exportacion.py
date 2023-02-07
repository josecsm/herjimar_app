import frappe
import subprocess
import os


@frappe.whitelist(allow_guest=True)
def exportar(plantilla,objeto):
    args = 'cd /var/www/html/erpnext && php artisan generar:plantilla "'+plantilla+'" "'+objeto+'"'
    so = os.popen(args).read()
    return so


@frappe.whitelist(allow_guest=True)
def exportarlista(plantilla,objetos):
    args = 'cd /var/www/html/erpnext && php artisan generar:plantillalista "'+plantilla+'" "'+objetos+'"'
    so = os.popen(args).read()
    return so
