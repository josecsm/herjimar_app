import frappe
import subprocess
import os
from datetime import date, timedelta, datetime

from numpy import size


@frappe.whitelist(allow_guest=True)
def get_reportado(usuario, asignacion):

    empleado=frappe.db.get_value('Employee',{'user_id':usuario},'name')

    lineas=frappe.db.get_list('Timesheet Detail',
    filters={
        'asignacion': asignacion,
    },fields=['name','hours','parent','from_time','to_time','docstatus'])

    resultado=[]
    for linea in lineas:
        parte=frappe.get_doc('Timesheet', linea.parent) 
        if ((parte.employee==empleado) and (parte.docstatus!=2)):
            resultado.append(linea)
    
    return resultado

@frappe.whitelist(allow_guest=True)
def nuevo_parte_app(usuario, asignacion,fecha,desde,hasta,terminado,observaciones):

    empleado=frappe.db.get_value('Employee',{'user_id':usuario},'name')

    antes=frappe.db.get_list('Timesheet',
    filters={
        'status': 'Draft',
        'employee': empleado,
        'start_date':   fecha,
        'end_date':  fecha 
    })
    parte=""
    if (len(antes)==0):
        parte = frappe.new_doc('Timesheet')
        emp = frappe.get_doc('Employee', empleado)
        parte.title = empleado
        parte.naming_series="TS-.YYYY.-"
        parte.employee = empleado
        parte.employee_name = empleado
        parte.proyecto_empleado = emp.proyecto
        parte.coste_directo_indirecto = emp.tipo_recurso
        parte.company="Metalmecánicas HERJIMAR"
        parte.start_date = fecha
        parte.end_date = fecha
        parte.total_hours=0
        parte.total_billable_hours=0
        parte.total_billed_hours=0
        parte.total_costing_amount=0
        parte.total_billable_amount=0
        parte.total_billed_amount=0
        parte.per_billed=0
        parte.time_logs={}
        parte.insert()  
    else:
        parte=antes[0]
    
    doc = frappe.get_doc('Timesheet', parte.name)
    doc_asignacion = frappe.get_doc('Asignacion', asignacion)
    
    log=frappe.logger("herjimar")
   
    if (doc_asignacion.tarea!=None):
        log.info("es una tarea")
        doc_tarea = frappe.get_doc('Task', doc_asignacion.tarea)
        if (doc_tarea.is_group):
            log.info("es una tarea con hijos")
            duracion=datetime.strptime(fecha+" "+hasta,"%Y-%m-%d %H:%M")-datetime.strptime(fecha+" "+desde,"%Y-%m-%d %H:%M")
            minutos=duracion/timedelta(minutes=1)

            filters = [['docstatus', '<', '2'],['parent_task', '=',doc_asignacion.tarea ]]
            hijos = frappe.get_list('Task', fields=[
		        'name'] , filters=filters, order_by='name')
            
            partes=1+len(hijos)
            log.info("es una tarea con "+str(len(hijos))+" hijos")
            duracion_parte=minutos/partes
            #añado una linea por el padre
            inicio=datetime.strptime(fecha+" "+desde,"%Y-%m-%d %H:%M")
            doc.append("time_logs",{
                    "activity_type":doc_asignacion.actividad,
                    "expected_hours":0.0,
                    "hours":0,
                    "billing_hours":0,
                    "billing_rate":0.0,
                    "billing_amount":0.0,
                    "costing_rate":0.0,
                    "costing_amount":0.0,
                    "task":doc_asignacion.tarea,
                    "project":doc_tarea.project,
                    "completed":terminado,
                    "es_incidencia":0,
                    "billable":0,
                    "descripción":observaciones,
                    "from_time":inicio,
                    "to_time":inicio+timedelta(minutes=duracion_parte),
                    "asignacion": asignacion
                    })
            #añado un alinea por cada hijo
            for hijo in hijos:
                log.info("añado hijo")
                inicio=inicio+timedelta(minutes=duracion_parte)
                doc.append("time_logs",{
                    "activity_type":doc_asignacion.actividad,
                    "expected_hours":0.0,
                    "hours":0,
                    "billing_hours":0,
                    "billing_rate":0.0,
                    "billing_amount":0.0,
                    "costing_rate":0.0,
                    "costing_amount":0.0,
                    "task":hijo.name,
                    "project":doc_tarea.project,
                    "completed":terminado,
                    "es_incidencia":0,
                    "billable":0,
                    "descripción":observaciones,
                    "from_time":inicio,
                    "to_time":inicio+timedelta(minutes=duracion_parte),
                    "asignacion": asignacion
                    })
        else:
            log.info("NO TIENE HIJOS")
            doc.append("time_logs",{
                    "activity_type":doc_asignacion.actividad,
                    "expected_hours":0.0,
                    "hours":0,
                    "billing_hours":0,
                    "billing_rate":0.0,
                    "billing_amount":0.0,
                    "costing_rate":0.0,
                    "costing_amount":0.0,
                    "task":doc_asignacion.tarea,
                    "project":doc_tarea.project,
                    "completed":terminado,
                    "es_incidencia":0,
                    "billable":0,
                    "descripción":observaciones,
                    "from_time":datetime.strptime(fecha+" "+desde,"%Y-%m-%d %H:%M"),
                    "to_time":datetime.strptime(fecha+" "+hasta,"%Y-%m-%d %H:%M"),
                    "asignacion": asignacion
                    })
        doc.save()
        frappe.db.commit()
    else:
        if (doc_asignacion.incidencia!=None):
            doc_incidencia = frappe.get_doc('Incidencia', doc_asignacion.incidencia)
            doc.append("time_logs",{
                    "activity_type":doc_asignacion.actividad,
                    "expected_hours":0.0,
                    "hours":0,
                    "billing_hours":0,
                    "billing_rate":0.0,
                    "billing_amount":0.0,
                    "costing_rate":0.0,
                    "costing_amount":0.0,
                    "incidencia":doc_asignacion.incidencia,
                    "project":doc_incidencia.proyecto,
                    "completed":terminado,
                    "es_incidencia":1,
                    "billable":0,
                    "descripción":observaciones,
                    "from_time":datetime.strptime(fecha+" "+desde,"%Y-%m-%d %H:%M"),
                    "to_time":datetime.strptime(fecha+" "+hasta,"%Y-%m-%d %H:%M"),
                    "asignacion": asignacion
                    })
            doc.save()
            frappe.db.commit()
    return "OK"


@frappe.whitelist(allow_guest=True)
def validar_partes_app(usuario, fecha):

    empleado=frappe.db.get_value('Employee',{'user_id':usuario},'name')

    partes=frappe.db.get_list('Timesheet',
    filters={
        'employee': empleado,
        'status': 'Draft',
        'start_date':  fecha,
        'end_date':  fecha
    })
    log=frappe.logger("herjimar")
   
    for parte in partes:
        log.info("validando parte "+parte.name)
        parteo=frappe.get_doc('Timesheet', parte.name)
        parteo.docstatus=1
        parteo.save() 
        log.info("parte validado")
    
    return "OK"

@frappe.whitelist(allow_guest=True)
def generar_recibo_nomina(empleado,mes,ejercicio):
    args = 'cd /var/www/html/erpnext && php artisan generar:recibo_nomina "'+empleado+'" "'+mes+'" "'+ejercicio+'"'
    so = os.popen(args).read()
    return so

@frappe.whitelist(allow_guest=True)
def generar_resumen(empleado,mes,ejercicio):
    args = 'cd /var/www/html/erpnext && php artisan generar:resumen_hora "'+empleado+'" "'+mes+'" "'+ejercicio+'"'
    so = os.popen(args).read()
    return so

@frappe.whitelist(allow_guest=True)
def enviar_correo(fecha="",jefe="",copia=""):
    if (len(fecha)==0):
        yesterday = date.today() - timedelta(days=1)
        fecha=yesterday.strftime('%Y-%m-%d')
    if (len(jefe)==0):
        jefe="*"
    if (len(copia)==0):
        copia="*"

    args = 'cd /var/www/html/erpnext && php artisan envia:informediario "'+fecha+'" "'+jefe+'" "'+copia+'"'
    so = os.popen(args).read()
    
    return "hola "+args+"->"+so