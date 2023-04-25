from __future__ import unicode_literals
import frappe
import locale
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
import json
import os


@frappe.whitelist()
def revision_soldadura(valores, maquina):
    parametros = json.loads(valores) 
    log=frappe.logger("herjimar")
    log.info(parametros['horas'])
    doc = frappe.new_doc('Revision Equipamiento')
    doc2 = frappe.get_doc('Equipamiento', maquina)
    doc.equipo = maquina
    doc.horas=parametros['horas']
    doc.empleado=parametros['empleado']
    doc.tipo='Equipos de Soldadura'
    doc.fecha=parametros['fecha']
    doc.intensidad1=parametros['imedida1']
    doc.intensidad2=parametros['imedida2']
    doc.intensidad3=parametros['imedida3']
    doc.voltaje1=parametros['vmedido1']
    doc.voltaje2=parametros['vmedido2']
    doc.voltaje3=parametros['vmedido3']

    coeficiente=doc2.parámetro_de_seguridad
    coeficiente = int(coeficiente[:-1])

    todo_ok=1

    imar1=doc2.intensidad_marcada_1
    imed1=float(doc.intensidad1)
    x=100*imed1/imar1
    e1=abs(x-100)
    if (e1>coeficiente):
        todo_ok=0

    imar2=doc2.intensidad_marcada_2
    imed2=float(doc.intensidad2)
    x=100*imed2/imar2
    e2=abs(x-100)
    if (e2>coeficiente):
        todo_ok=0

    imar3=doc2.intensidad_marcada_3
    imed3=float(doc.intensidad3)
    x=100*imed3/imar3
    e3=abs(x-100)
    if (e3>coeficiente):
        todo_ok=0

    vmar1=doc2.voltaje_marcado_1
    vmed1=float(doc.voltaje1)
    x=100*vmed1/vmar1
    e1=abs(x-100)
    if (e1>coeficiente):
        todo_ok=0

    vmar2=doc2.voltaje_marcado_2
    vmed2=float(doc.voltaje2)
    x=100*vmed2/vmar2
    e2=abs(x-100)
    if (e2>coeficiente):
        todo_ok=0

    vmar3=doc2.voltaje_marcado_3
    vmed3=float(doc.voltaje3)
    x=100*vmed3/vmar3
    e3=abs(x-100)
    if (e3>coeficiente):
        todo_ok=0



    if (todo_ok>0):
        #OK
        doc.apto=1
        if (doc2.operario == None):
            doc2.estado = "Almacén"
        else:
            doc2.estado = "En uso"
    else:
        #NO OK
        doc2.estado = "Baja temporal"
        doc.apto=0


    if 'observaciones' in parametros:
        doc.observaciones=parametros['observaciones']
    doc.insert()
# actualizar maquina
    doc2.fecha_última_acción_preventiva =  parametros['fecha']
    log.info(">"+doc2.periodicidad_revisiones_meses+"<")
    if (doc2.periodicidad_revisiones_meses=="1 mes"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+1)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
        log.info(">"+date.strftime("%Y-%m-%d")+"<")
    if (doc2.periodicidad_revisiones_meses=="3 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+3)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="6 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+6)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="12 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+12)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="24 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+24)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="36 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+36)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="48 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+48)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    doc2.save()
    #frappe.db.commit()
    # generar excel y enviarlo por mail y sharepoint
    #args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_soldadura '+doc.name
    #so = os.popen(args).read() 
    #log.info(so)
    pass


@frappe.whitelist()
def revision_estufa(valores, maquina):
    parametros = json.loads(valores) 
    log=frappe.logger("herjimar")
    log.info(parametros['horas'])
    doc = frappe.new_doc('Revision Equipamiento')
    doc2 = frappe.get_doc('Equipamiento', maquina)
    doc.equipo = maquina
    doc.horas=parametros['horas']
    doc.fecha=parametros['fecha']
    doc.empleado=parametros['empleado']
    doc.tipo='Estufas'

    doc.medidas80=parametros['medidas1']
    doc.medidas100=parametros['medidas2']
    doc.medidas110=parametros['medidas3']

    

    medidas1=parametros['medidas1'].split(',')
    temp1=0.0
    for medida in medidas1:
        temp1+=float(medida)
    temp1=temp1/len(medidas1)

    medidas2=parametros['medidas2'].split(',')
    temp2=0.0
    for medida in medidas2:
        temp2+=float(medida)
    temp2=temp2/len(medidas2)

    medidas3=parametros['medidas3'].split(',')
    temp3=0.0
    for medida in medidas3:
        temp3+=float(medida)
    temp3=temp3/len(medidas3)



    if (temp1>=80) and (temp2>=80) and (temp3>=80) and (temp1<=150) and (temp2<=150) and (temp3<=150):
        #OK
        doc.apto=1
        if (doc2.operario == None):
            doc2.estado = "Almacén"
        else:
            doc2.estado = "En uso"
    else:
        #NO OK
        doc2.estado = "Baja temporal"
        doc.apto=0



    if 'observaciones' in parametros:
        doc.observaciones=parametros['observaciones']
    doc.insert()
# actualizar maquina
   
    #doc2.estado = parametros['nuevo_estado']
    doc2.fecha_última_acción_preventiva =  parametros['fecha']
    log.info(">"+doc2.periodicidad_revisiones_meses+"<")
    if (doc2.periodicidad_revisiones_meses=="1 mes"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+1)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
        log.info(">"+date.strftime("%Y-%m-%d")+"<")
    if (doc2.periodicidad_revisiones_meses=="3 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+3)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="6 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+6)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="12 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+12)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="24 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+24)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="36 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+36)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="48 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+48)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    doc2.save()
    frappe.db.commit()
    # generar excel y enviarlo por mail y sharepoint
    #args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_estufa '+doc.name
    #so = os.popen(args).read() 
    #log.info(so)
    pass


@frappe.whitelist()
def revision_horno(valores, maquina):
    parametros = json.loads(valores) 
    log=frappe.logger("herjimar")
    log.info(parametros['horas'])
    doc = frappe.new_doc('Revision Equipamiento')
    doc2 = frappe.get_doc('Equipamiento', maquina)
    doc.equipo = maquina
    doc.horas=parametros['horas']
    doc.fecha=parametros['fecha']

    doc.empleado=parametros['empleado']
    doc.tipo='Hornos'

    doc.medidas120=parametros['medidas1']
    doc.medidas150=parametros['medidas2']

    medidas=parametros['medidas2'].split(',')
    temp=0.0
    for medida in medidas:
        temp+=float(medida)
    temp=temp/len(medidas)
    if (temp>=120):
        #OK
        doc.apto=1
        if (doc2.operario == None):
            doc2.estado = "Almacén"
        else:
            doc2.estado = "En uso"
    else:
        #NO OK
        doc.apto=0
        doc2.estado = "Baja temporal"
    if 'observaciones' in parametros:
        doc.observaciones=parametros['observaciones']
    doc.insert()
# actualizar maquina
    
    #doc2.estado = parametros['nuevo_estado']
    doc2.fecha_última_acción_preventiva = parametros['fecha']
    log.info(">"+doc2.periodicidad_revisiones_meses+"<")
    if (doc2.periodicidad_revisiones_meses=="1 mes"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+1)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
        log.info(">"+date.strftime("%Y-%m-%d")+"<")
    if (doc2.periodicidad_revisiones_meses=="3 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+3)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="6 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+6)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="12 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+12)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="24 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+24)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="36 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+36)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="48 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+48)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    doc2.save()
    frappe.db.commit()
    # generar excel y enviarlo por mail y sharepoint
    #args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_horno '+doc.name
    #so = os.popen(args).read() 
    #log.info(so)
    pass

@frappe.whitelist()
def revision_generica(valores, maquina):
    parametros = json.loads(valores) 
    log=frappe.logger("herjimar")
    log.info(parametros['horas'])
    doc = frappe.new_doc('Revision Equipamiento')
    doc2 = frappe.get_doc('Equipamiento', maquina)
    doc.equipo = maquina
    doc.horas=parametros['horas']
    doc.fecha=parametros['fecha']

    doc.empleado=parametros['empleado']
    doc.tipo='Genérica'

    doc.actuacion=parametros['actuacion']
    doc.resultado=parametros['resultado']

    if (doc.resultado=="Ok"):
        #OK
        doc.apto=1
        if (doc2.operario == None):
            doc2.estado = "Almacén"
        else:
            doc2.estado = "En uso"
    else:
        #NO OK
        doc.apto=0
        doc2.estado = "Baja temporal"

    if 'observaciones' in parametros:
        doc.observaciones=parametros['observaciones']
    doc.insert()
# actualizar maquina
    #doc2.estado = parametros['nuevo_estado']
    doc2.fecha_última_acción_preventiva = parametros['fecha']
    log.info(">"+doc2.periodicidad_revisiones_meses+"<")
    if (doc2.periodicidad_revisiones_meses=="1 mes"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+1)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
        log.info(">"+date.strftime("%Y-%m-%d")+"<")
    if (doc2.periodicidad_revisiones_meses=="3 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+3)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="6 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+6)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="12 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+12)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="24 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+24)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="36 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+36)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    if (doc2.periodicidad_revisiones_meses=="48 meses"):
        date = datetime.strptime(parametros['fecha'], "%Y-%m-%d")
        date = date + relativedelta(months=+48)
        doc2.fecha_próxima_acción = date.strftime("%Y-%m-%d")
    doc2.save()
    frappe.db.commit()
    # generar excel y enviarlo por mail y sharepoint
    #args = 'cd /var/www/html/erpnext && php artisan genera:excel_mantenimiento_generica '+doc.name
    #so = os.popen(args).read() 
    #log.info(so)
    pass


@frappe.whitelist()
def cargatabla(codigo="",clase="", responsable=""):
    
    log=frappe.logger("herjimar")
    maquinas=[]
    filtro=[["fecha_próxima_acción","<=",datetime.now().strftime("%Y-%m-%d")]]
    if (len(codigo)>0):
        filtro.append(["name","=",codigo])
    if (len(clase)>0):
        filtro.append(["clase","=",clase])
    if (len(responsable)>0):
        filtro.append(["operario","=",responsable])
    maquinas=frappe.db.get_list('Equipamiento',
    filters=filtro,
    fields=['name','clase','tipo_de_equipo','operario','fecha_próxima_acción','marca','modelo','número_de_serie','plantilla_excel','intensidad_marcada_1','intensidad_marcada_2','intensidad_marcada_3','voltaje_marcado_1','voltaje_marcado_2','voltaje_marcado_3','primera_medida','segunda_medida','tercera_medida','código_mh','operación_a_realizar'],
    order_by='name asc'
    )
    out = {
		'maquinas': maquinas
	}
    return out