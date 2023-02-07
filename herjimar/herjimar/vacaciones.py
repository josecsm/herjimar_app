from erpnext.hr.doctype.leave_application.leave_application import OverlapError
import frappe
import subprocess
import os
from datetime import date, timedelta, datetime


@frappe.whitelist(allow_guest=True)
def resumen_excel(empleado,ejercicio):

    log=frappe.logger("herjimar")
    args = 'cd /var/www/html/erpnext && php artisan resumen:excel_vacaciones "'+empleado+'" "'+ejercicio+'"'
    log.error("ejecuto:"+args)
    salida = os.popen(args).read()
    log.error("salida es "+salida)
    return salida
    
@frappe.whitelist(allow_guest=True)
def desglose(empleado,desde,hasta):

    log=frappe.logger("herjimar")
    args = 'cd /var/www/html/erpnext && php artisan desglosa:permisos "'+empleado+'" "'+desde+'" "'+hasta+'"'
    log.error("ejecuto:"+args)
    salida = os.popen(args).read()
    log.error("salida es "+salida)
    return salida
    

@frappe.whitelist(allow_guest=True)
def nueva_solicitud_app(empleado,desde,hasta,razon):

    try:
        oempleado=frappe.db.get_value('Employee',{'user_id':empleado},'name')
        emp = frappe.get_doc('Employee', oempleado)
        
        vaca = frappe.new_doc('Leave Application')
        vaca.from_date=desde
        vaca.to_date=hasta
        vaca.naming_series="HR-LAP-.YYYY.-"
        vaca.leave_type="Vacaciones"
        vaca.subtipo="Vacaciones"
        vaca.employee=emp.name
        vaca.employee_name=emp.name
        vaca.department=emp.department
        vaca.numero_empleado=emp.employee_number
        vaca.description=razon
        vaca.dias_reales=0

        if (emp.leave_approver):
            ojefe=frappe.db.get_value('Employee',{'user_id':emp.leave_approver},'name')
            vaca.leave_approver=emp.leave_approver
            vaca.leave_approver_name=ojefe
        
        vaca.insert()

        return "OK"
    except OverlapError:
        return "Overlap"