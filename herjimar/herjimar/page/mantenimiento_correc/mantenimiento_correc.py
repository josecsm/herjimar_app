from __future__ import unicode_literals
import frappe
import locale
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
import json
import os

@frappe.whitelist()
def nueva(valores):
    parametros = json.loads(valores) 
    doc = frappe.new_doc('Revision Correctivo')
    doc.equipo=parametros['maquina']
    doc.empleado=parametros['empleado']
    doc.terminado=0
    doc.creado=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc.descripcion_entrada=parametros['descripcion']
    if 'observaciones' in parametros:
        doc.observaciones_entrada=parametros['observaciones']
    doc.insert()

    doc2 = frappe.get_doc('Equipamiento', parametros['maquina'])
    doc2.estado='En mantenimiento correctivo'
    doc2.save()
    destinos=[]
    destinos.append('jose.carlossanchez@gmail.com')
    destinos.append('anieto@herjimar.com')
    email_args = {
        "recipients":destinos,
        "message": "Se ha creado una nueva solicitud de mantenimiento correctivo (<a href='https://erp.herjimar.com/desk#Form/Revision%20Correctivo/"+doc.name+"'>"+doc.name+"</a>) . Ver información adjunta",
        "subject": 'Nuevo mantenimiento correctivo',
        "attachments": [frappe.attach_print(doc.doctype, doc.name, lang='es', file_name=doc.name)],
        "reference_doctype": doc.doctype,
        "reference_name": doc.name
    }
    
    frappe.enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
    pass

@frappe.whitelist()
def guardar(valores,revision):
    parametros = json.loads(valores) 

    doc = frappe.get_doc('Revision Correctivo', revision)
    doc.terminado=1
    doc.arreglado= parametros['fecha']
    doc.horas=parametros['horas']
    doc.empleado2=parametros['empleado']
    doc.solucion=parametros['solucion']
    doc.resultado=parametros['resultado']

    doc2 = frappe.get_doc('Equipamiento', doc.equipo)
    doc2.fecha_última_acción_correctiva= parametros['fecha']
    
    if (doc.resultado=="Ok"):
        #OK
        if (doc2.operario == None):
            doc2.estado = "Almacén"
        else:
            doc2.estado = "En uso"
    else:
        #NO OK
        doc2.estado = "Baja temporal"
    doc2.save()

    if 'observaciones' in parametros:
        doc.observaciones_salida=parametros['observaciones']
    doc.save()
    pass


@frappe.whitelist()
def cargatabla():
    
    log=frappe.logger("herjimar")

    filtro=[["terminado","=",0]]
    maquinas={}
    revisiones=frappe.db.get_list('Revision Correctivo',
    filters=filtro,
    fields=['name','equipo','descripcion_entrada','creado'],
    order_by='creado asc'
    )
    for revision in revisiones:
        maquinas[revision.equipo]=frappe.get_doc('Equipamiento', revision.equipo)
    out = {
		'revisiones': revisiones,
        'maquinas': maquinas
	}
    return out