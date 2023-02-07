import frappe
import os
import re
import json
from frappe import enqueue, utils


def on_submit_leave_application(doc, method=None):

    frappe.db.commit()
    args = 'cd /var/www/html/erpnext && php artisan actualiza:bajas'
    so = os.popen(args).read()
    return True

def on_submit_shift_request(doc, method=None):
    
    empleados=frappe.db.get_list('Employee',
            filters={
                'solicitud_de_turnos':1
            }
            , fields = ["user_id"]
        )
    destinos=[]
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for empleado in empleados:
        email=frappe.db.get_value("User", empleado.user_id, 'email')
        if(re.fullmatch(regex, email)):
            destinos.append(email)
    if (len(destinos)>0):
        email_args = {
            "recipients":destinos,
            "message": "Se ha validado una nueva peticion de turno. Ver solicitud adjunta",
            "subject": 'Nueva Solicitud de Turno',
            "attachments": [frappe.attach_print(doc.doctype, doc.name, lang='es', file_name=doc.name)],
            "reference_doctype": doc.doctype,
            "reference_name": doc.name
        }
        
        frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    return True

def before_save_task(doc, method=None):

    if (len(doc.hoja_verde)>9):
        codhv=doc.hoja_verde[4:10]
        hv=frappe.get_doc('Hoja Verde', doc.hoja_verde)
        cliente=frappe.get_doc('Customer', hv.cliente)
        
        args = 'cd /var/www/html/erpnext && php artisan generar:proximaodf '+cliente.código_xgest+' '+codhv+' '+doc.sector        
        proxima_odf = os.popen(args).read()

    return doc

def before_save_quotation(doc, method=None):
    
    #doc.total=doc.numero_unidades*doc.importe_total
    #doc.grand_total=doc.numero_unidades*doc.importe_total
    #doc.rounded_total=doc.numero_unidades*doc.importe_total
    return doc

def on_update_quotation(doc, method=None):
    
    #doc.total=doc.numero_unidades*doc.importe_total
    #doc.grand_total=doc.numero_unidades*doc.importe_total
    #doc.rounded_total=doc.numero_unidades*doc.importe_total
    #doc.save()
    return doc


def on_update_proyecto(doc, method=None):

    hvs=frappe.db.get_list('Hoja Verde',
        filters={
            'proyecto': doc.name
        }
        , fields = ["name"])

    for hv in hvs:
        doc2=frappe.get_doc('Hoja Verde', hv.name)
        if ((doc.status=='Completed') or (doc.status=='Cancelled')):
            doc2.terminado = 1
        doc2.nombre_del_proyecto=doc.project_name
        doc2.responsable_proyecto=doc.responsable_del_proyecto
        doc2.linea_de_negocio=doc.línea_de_negocio
        doc2.save()

    incs=frappe.db.get_list('Incidencia',
        filters={
            'proyecto': doc.name
        }
        , fields = ["name"])

    for inc in incs:
        doc3=frappe.get_doc('Incidencia', inc.name)
        doc3.nombre_del_proyecto=doc.project_name
        doc3.save()

    return doc

def after_insert_revision_equipamiento(doc, method=None):

    frappe.db.commit()
    log=frappe.logger("herjimar")
    if (doc.tipo=="Equipos de Soldadura"):
         args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_soldadura '+doc.name
    if (doc.tipo=="Estufas"):
         args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_estufa '+doc.name
    if (doc.tipo=="Hornos"):
         args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_horno '+doc.name
    if (doc.tipo=="Genérica"):
         args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_generica '+doc.name
    
    os.popen(args)
#    log.info(so)
    pass

def after_insert_Issue(doc, method=None):

    responsable=frappe.get_doc('Employee', doc.responsable)
        
    email_args = {
        "recipients":responsable.prefered_email,
        "message": "Se ha creado una nueva solicitud de soporte (<a href='https://erp.herjimar.com/desk#Form/Issue/"+doc.name+"'>"+doc.name+"</a>) de la que usted es responsable. Ver incidencia adjunta",
        "subject": 'Nueva Solicitud de Sorporte',
        "attachments": [frappe.attach_print(doc.doctype, doc.name, lang='es', file_name=doc.name)],
        "reference_doctype": doc.doctype,
        "reference_name": doc.name
    }
    
    frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)

    pass

def after_insert_proyecto(doc, method=None):
    
    args = 'cd /var/www/html/erpnext && php artisan generar:proximahv "'+doc.obra_interna+'"'
    proxima_hv = os.popen(args).read()
    
    args = 'cd /var/www/html/erpnext && php artisan generar:proximopresupuesto "'+doc.oferta_previa+'"'
    presupuesto = os.popen(args).read()
    
    doc2 = frappe.new_doc('Hoja Verde')
    doc2.número = proxima_hv
    doc2.presupuesto = presupuesto
    doc2.fecha = utils.today()
    doc2.cliente = doc.customer
    doc2.proyecto = doc.name
    doc2.objeto = doc.name
    doc2.servicio = doc.descripción
    doc2.observaciones_internas = doc.descripción
    doc2.obra_interna = doc.obra_interna
    doc2.oferta_previa = doc.oferta_previa
    doc2.sector = doc.sector
    doc2.nombre_del_proyecto=doc.project_name
    doc2.responsable_proyecto=doc.responsable_del_proyecto
    doc2.linea_de_negocio=doc.línea_de_negocio
    doc2.insert()

    pass

def on_update_Task(doc, method=None):

    if (not(hasattr(doc,'script')) or (doc.script==0)):
        
        frappe.db.commit()
        args = 'cd /var/www/html/erpnext && php artisan actualiza:odf "'+doc.name+'"'
        so = os.popen(args).read()  

    pass

def on_update_HV(doc, method=None):

    log=frappe.logger('herjimar')
    log.info("on_update_hoja_verde "+doc.name)
    if (not(hasattr(doc,'script')) or (doc.script==0)):
        log.info("on_update_hoja_verde no es script "+doc.name)
        frappe.db.commit()
        args = 'cd /var/www/html/erpnext && php artisan crea:hojaverde '+doc.name
        log.info("on_update_hoja_verde ejecuto "+args)
        so = os.popen(args).read()  
        log.info("on_update_hoja_verde devuelve "+so)

def after_insert_HV(doc, method=None):


    if (not(hasattr(doc,'script')) or (doc.script==0)):
        frappe.db.commit()
        args = 'cd /var/www/html/erpnext && php artisan crea:hojaverde '+doc.name
        so = os.popen(args).read()


        doc2 = frappe.new_doc('Task')
        doc2.sector = doc.sector
        doc2.subject = doc.objeto
        doc2.hoja_verde = doc.name
        doc2.project = doc.proyecto
        hoja_verde=doc.name
        codhv=hoja_verde[4:10]
        hv=frappe.get_doc('Hoja Verde', hoja_verde)
        cliente=frappe.get_doc('Customer', hv.cliente)
            
        args = 'cd /var/www/html/erpnext && php artisan generar:proximaodf '+cliente.código_xgest+' '+codhv+' '+doc.sector        
        proxima_odf = os.popen(args).read()
        doc2.orden_de_fabricacion=cliente.código_xgest+"-"+codhv.lstrip("0")+"-"+doc.sector+"-"+proxima_odf
        doc2.sincronizar_xgest=1
        doc2.horas_presupuestadas=1
        doc2.insert()
    pass

def on_update_Incidencia(doc, method=None):
    if (doc.estado=="Completado") or (doc.estado=="Validado") or (doc.estado=="Cancelado") or (doc.estado=="Reclamado") or (doc.estado=="Rechazado"):
        args = 'cd /var/www/html/erpnext && php artisan actualiza:incidencia "'+doc.name+'" "S"'
        so = os.popen(args).read()
    else:
        args = 'cd /var/www/html/erpnext && php artisan actualiza:incidencia "'+doc.name+'" "N"'
        so = os.popen(args).read()
    pass

def after_insert_Incidencia(doc, method=None):
    #if (doc.incidencia_interna==0) and ( (doc.reclamable_cliente==1) or (doc.reclamable_proveedor==1)):
    pro=frappe.get_doc('Project', doc.proyecto)
           
    if doc.hoja_verde_enlazada is None:
        args = 'cd /var/www/html/erpnext && php artisan nueva:incidencia "'+doc.name+'" "'+doc.titulo+'" "NONE" "'+str(doc.estimación_de_horas)+'" "'+pro.project_name+'" "'+str(doc.reclamable_cliente)+'" "'+str(doc.reclamable_proveedor)+'" "'+str(doc.incidencia_interna)+'"'
        so = os.popen(args).read()
    else:
        args = 'cd /var/www/html/erpnext && php artisan nueva:incidencia "'+doc.name+'" "'+doc.titulo+'" "'+doc.hoja_verde_enlazada+'" "'+str(doc.estimación_de_horas)+'" "'+pro.project_name+'" "'+str(doc.reclamable_cliente)+'" "'+str(doc.reclamable_proveedor)+'" "'+str(doc.incidencia_interna)+'"'
        so = os.popen(args).read()
    pass

def after_insert_File(doc, method=None):
    if (doc.attached_to_doctype=='Task'):
        args = 'cd /var/www/html/erpnext && php artisan archiva:task_sharepoint "'+doc.attached_to_name+'" "'+doc.file_url+'"'
        so = os.popen(args).read()
        if ((len(so)>0) and (so[0:4]=='http')):
            doc.file_url=so
            doc.file_size=0
            doc.is_private=0
            doc.save()
    if (doc.attached_to_doctype=='Ordenes de Cambio'):
        args = 'cd /var/www/html/erpnext && php artisan archiva:task_sharepointoc "'+doc.attached_to_name+'" "'+doc.file_url+'"'
        so = os.popen(args).read()
        if ((len(so)>0) and (so[0:4]=='http')):
            doc.file_url=so
            doc.file_size=0
            doc.is_private=0
            doc.save()
    pass

def after_delete_File(doc, method=None):
    if ((doc.attached_to_doctype=='Task') and (doc.file_url[0:49]=='https://herjimar.sharepoint.com/sites/ProgramaS80')):
        args = 'cd /var/www/html/erpnext && php artisan borra:task_sharepoint "'+doc.file_url+'"'
        so = os.popen(args).read()
    pass
