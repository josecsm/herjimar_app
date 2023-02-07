import frappe
import json
import time
import os
from datetime import datetime, date, time, timedelta


@frappe.whitelist(allow_guest=True)
def enviarxgest(partes):
    obj = json.loads(partes)
    out = []
    log=frappe.logger("herjimar")
    for parten in obj:
        parte=frappe.get_doc('Timesheet', parten)
        log.info("parte "+parten)
        if (parte.status=="Draft"):
            out.append({"id":parten,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Parte no confirmado"})
        else:
            lpartes=frappe.db.get_all('Timesheet Detail',filters={
                "parent":parten,
                "docstatus":1
            }, fields=['name', 'task','xgest','incidencia','from_time','to_time','hours','activity_type','descripción'])
            for lparte in lpartes:
                log.info("linea de parte "+lparte.name)
                if lparte.xgest is None:
                    log.info("linea de parte "+lparte.name+" no tiene xgest relleano")
                    if ((lparte.task is None) or(lparte.task=='')):
                        log.info("linea de parte "+lparte.name+" no tiene task, sera incidencia")
                        if ((lparte.incidencia is None) or (lparte.incidencia=='')):
                            out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Parte sin tarea/incidencia"})
                        else:
                            #sincronizar por incidencia
                            log.info("buscando incidencia "+lparte.incidencia);
                            incidencia=frappe.get_doc('Incidencia', lparte.incidencia)
                            if incidencia.hoja_verde_enlazada is None:
                                out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Incidencia sin hoja verde:"+lparte.incidencia})
                            else:
                                if incidencia.proyecto is None:
                                    out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Incidencia sin proyecto:"+lparte.incidencia})
                                else:
                                    proyecto=frappe.get_doc('Project', incidencia.proyecto)
                                    empleado=frappe.get_doc('Employee', parte.employee) 
                                    fecha=str(lparte.from_time)[0:10]
                                    desde=str(lparte.from_time)[11:16]
                                    hasta=str(lparte.to_time)[11:16]
                                    descripcion=lparte.descripción.replace("-",".")
                                    args = 'cd /var/www/html/erpnext && php artisan envia:parte_xgest "'+lparte.name+'" "'+str(incidencia.hoja_verde_enlazada)+'" "'+incidencia.name+'" "'+str(proyecto.coste_hora)+'" "'+empleado.employee_number+'" "'+fecha+'" "'+desde+'" "'+hasta+'" "'+str(lparte.hours)+'" "31" "'+descripcion+'"'
                                    
                                    log.info("ejecuto:"+args)
                                    salida = os.popen(args).read()
                                    osalida = json.loads(salida)
                                    if (osalida["resultado"]):
                                        #actualizar la linea
                                        out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 1,"msg":osalida["msg"]})
                                    else:
                                        out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":osalida["msg"]})
                    else:
                        #sincronizar por ODF
                        tarea=frappe.get_doc('Task', lparte.task)
                        if tarea.hoja_verde is None:
                             out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Tarea sin hoja verde:"+lparte.task})
                        else:
                            if tarea.project is None:
                                out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Tarea sin proyecto:"+lparte.task})
                            else:
                                proyecto=frappe.get_doc('Project', tarea.project)
                                empleado=frappe.get_doc('Employee', parte.employee) 
                                fecha=str(lparte.from_time)[0:10]
                                desde=str(lparte.from_time)[11:16]
                                hasta=str(lparte.to_time)[11:16]
                                log=frappe.logger("herjimar")
                                descripcion=lparte.descripción.replace("-",".")
                                args = 'cd /var/www/html/erpnext && php artisan envia:parte_xgest "'+lparte.name+'" "'+str(tarea.hoja_verde)+'" "'+tarea.orden_de_fabricacion+'" "'+str(proyecto.coste_hora)+'" "'+empleado.employee_number+'" "'+fecha+'" "'+desde+'" "'+hasta+'" "'+str(lparte.hours)+'" "31" "'+descripcion+'"'
                                log.error("ejecuto:"+args)
                                salida = os.popen(args).read()
                                log.error("salida es "+salida)
                                osalida = json.loads(salida)
                                if (osalida["resultado"]):
                                    out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 1,"msg":osalida["msg"]})
                                else:
                                    out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":osalida["msg"]})

                else:
                    out.append({"id":parten+"-"+lparte.name,"empleado":parte.employee_name,"fecha":parte.start_date,"result": 0,"msg":"Parte ya sincronizado"})


    return out


@frappe.whitelist(allow_guest=True)
def nuevoparte(values,horas,odfs,incidencias,desde,hasta):
    empleado=frappe.db.get_value('Employee',{'user_id':frappe.session.user},'name')
    
    obj = json.loads(values)
   
  
    antes=frappe.db.get_list('Timesheet',
    filters={
        'status': 'Draft',
        'employee': empleado,
        'start_date':  [ "<=", obj["fecha"] ],
        'end_date':  [ ">=", obj["fecha"] ]
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
        parte.start_date = obj["fecha"]
        parte.end_date = obj["fecha"]
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

    if (obj["reclamable"]==0):

        jodfs = json.loads(odfs)
        num_odfs=len(jodfs)
        delta=timedelta(hours = float(horas)/num_odfs)
        if (desde.endswith(":")):
            desde=desde+"00"
        puntero_inicio=datetime.strptime(obj["fecha"]+" "+desde+":00.000000","%Y-%m-%d %H:%M:%S.%f")
        puntero_fin=puntero_inicio+delta

        for jodf in jodfs:
            task = frappe.get_doc('Task', jodf)
            descripcion="-"
            if obj.get("descripcion"):
                descripcion=obj["descripcion"]
            

            doc.append("time_logs",{
            "activity_type":obj["actividad"],
            "expected_hours":0.0,
            "hours":float( horas)/num_odfs,
            "billing_hours":float( horas)/num_odfs,
            "billing_rate":0.0,
            "billing_amount":0.0,
            "costing_rate":0.0,
            "costing_amount":0.0,
            "task":jodf,
            "project":task.project,
            "completed":obj["terminado"],
            "es_incidencia":obj["reclamable"],
            "billable":0,
            "descripción":descripcion,
            "from_time":puntero_inicio,
            "to_time":puntero_fin,
            })
            doc.save()
            frappe.db.commit()
            puntero_inicio=puntero_fin
            puntero_fin=puntero_inicio+delta
    else:
        jodfs = json.loads(incidencias)
        num_odfs=len(jodfs)
        delta=timedelta(hours = float(horas)/num_odfs)
        if (desde.endswith(":")):
            desde=desde+"00"
        puntero_inicio=datetime.strptime(obj["fecha"]+" "+desde+":00.000000","%Y-%m-%d %H:%M:%S.%f")
        puntero_fin=puntero_inicio+delta

        for jodf in jodfs:
            task = frappe.get_doc('Incidencia', jodf)
            descripcion="-"
            if obj.get("descripcion"):
                descripcion=obj["descripcion"]
            

            doc.append("time_logs",{
            "activity_type":obj["actividad"],
            "expected_hours":0.0,
            "hours":float( horas)/num_odfs,
            "billing_hours":float( horas)/num_odfs,
            "billing_rate":0.0,
            "billing_amount":0.0,
            "costing_rate":0.0,
            "costing_amount":0.0,
            "incidencia":jodf,
            "project":task.proyecto,
            "completed":obj["terminado"],
            "es_incidencia":obj["reclamable"],
            "billable":0,
            "descripción":descripcion,
            "from_time":puntero_inicio,
            "to_time":puntero_fin,
            })
            doc.save()
            frappe.db.commit()
            puntero_inicio=puntero_fin
            puntero_fin=puntero_inicio+delta
        

    doc = frappe.get_doc('Timesheet', parte.name)
    return {"horas":doc.total_hours,"parte":doc.name}

@frappe.whitelist(allow_guest=True)
def gethv(odf):
    if odf=="":
        return ""
    hoja=frappe.db.get_value('Task', odf, 'hoja_verde')
    if hoja==None:
        return "ODF sin Hoja Verde "+odf
    objeto=frappe.db.get_value('Hoja Verde', hoja, 'objeto')
    if objeto==None:
        objeto=""
    return "Hoja Verde:"+hoja+" - "+objeto

@frappe.whitelist(allow_guest=True)
def getodfs(term=None,_type=None,q=None):
    if ((term == None) or (term =='')) :
        return {"results":[]}
    else:
        out = []
        odfs=frappe.db.get_list('Task', page_length=20,filters={
        'name': ['like', '%'+term+'%'],
        'status': ["!=", "Cancelled"],
        'estado_sap': ["not in",["ELIM","ABIE","CTEC","NOTI"]]
        },fields=['name','project'])
        for odf in odfs:
            proyecto=""
            if (odf.project!=None):
                proyecto=odf.project
            out.append({
            "id": odf.name,
            "text": "["+proyecto+"]"+ odf.name,
        })
        return {"results":out}

@frappe.whitelist(allow_guest=True)
def getincidencias(term=None,_type=None,q=None):
    if ((term == None) or (term =='')) :
        return {"results":[]}
    else:
        out = []
        odfs=frappe.db.get_list('Incidencia', page_length=20,filters={
        'name': ['like', '%'+term+'%'],
#        'estado':['not in',['Cerrado','Cancelado','Rechazado','Completado','Reclamado']]
        'estado':['in',['En curso','Registrado']]
        },fields=['name','proyecto'])
        for odf in odfs:
            proyecto=""
            if (odf.proyecto!=None):
                proyecto=odf.proyecto
            out.append({
            "id": odf.name,
            "text": "["+proyecto+"]"+ odf.name,
        })
        return {"results":out}

@frappe.whitelist(allow_guest=True)
def getreportado(fecha):
    if fecha=="":
        return ""
    horas=0
    log=""
    empleado=frappe.db.get_value('Employee',{'user_id':frappe.session.user},'name')
    partes=frappe.db.get_list('Timesheet', filters={
        'employee':empleado,
        'start_date': ['<=', fecha],
        'end_date': ['>=', fecha]
    },fields=['name'])
    for parte in partes:
        log=log+"parte "+parte["name"]+","
        lineas=frappe.db.get_list('Timesheet Detail', filters={
        'parent': parte["name"],
        'from_time': ['>=', fecha+" 00:00:00"],
        'to_time': ['<=', fecha+" 23:59:59"]
        },fields=['name','hours'])
        for linea in lineas:
            log=log+"linea "+linea["name"]+","
            horas=horas+linea["hours"]
    return str(round(horas,2))+" horas ya reportadas"

