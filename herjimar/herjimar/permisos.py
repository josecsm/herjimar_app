import frappe
import json

@frappe.whitelist(allow_guest=True)
def tiene_permiso(permiso):
    
    return permiso in frappe.get_roles()
