import frappe

@frappe.whitelist(allow_guest=True)
def eliminar_posesion(equipo,fecha):
    doc = frappe.get_doc('Equipo', equipo)
    anterior=doc.responsable
    doc.responsable =""
    for linea in doc.responsables:
        if not linea.hasta:
            linea.hasta=fecha
    doc.save()

    if (anterior!=None) and (anterior!=""):
        doc3 = frappe.get_doc('Employee', anterior)
        for linea in doc3.prestamos:
            if linea.equipo==equipo:
                if not linea.hasta:
                    linea.hasta=fecha
        doc3.save()
    frappe.db.commit()

    
@frappe.whitelist(allow_guest=True)
def crear_posesion_masiva(posesion):
    
    doc = frappe.get_doc('Asignacion Equipo', posesion)
    ret=""
    for linea in doc.get("equipos"):
        ret=ret+"-linea"
        if (doc.tipo=="Asignación de equipos"):
            ret=ret+"-asigno:"+linea.equipo+","+doc.nuevo_responsable+","+doc.fecha.strftime("%Y-%m-%d")
            crear_posesion(linea.equipo,doc.nuevo_responsable,doc.fecha.strftime("%Y-%m-%d"))
        else:
            ret=ret+"-desasigno:"+linea.equipo+","+doc.fecha.strftime("%Y-%m-%d")
            eliminar_posesion(linea.equipo,doc.fecha.strftime("%Y-%m-%d"))
    return ret

@frappe.whitelist(allow_guest=True)
def crear_posesion(equipo,nuevo_responsable,fecha):

    doc = frappe.get_doc('Equipo', equipo)
    anterior=doc.responsable
    doc.responsable = nuevo_responsable
    for linea in doc.responsables:
        if not linea.hasta:
            linea.hasta=fecha
    doc.append('responsables', {
        'empleado': nuevo_responsable,
        'desde': fecha,
    })
    doc.save()

    doc2 = frappe.get_doc('Employee', nuevo_responsable)
    doc_equipo = frappe.get_doc('Equipo', equipo)
    doc2.append('prestamos', {
        'equipo': equipo,
        'códigohm': doc_equipo.código_herjimar,
        'tipo': doc_equipo.clase_de_equipo+" "+doc_equipo.tipo_de_equipo,
        'desde': fecha,
    })
    doc2.save()

    if (anterior!=None)and (anterior!=""):
        doc3 = frappe.get_doc('Employee', anterior)
        for linea in doc3.prestamos:
            if linea.equipo==equipo:
                if not linea.hasta:
                    linea.hasta=fecha
        doc3.save()


    frappe.db.commit()
    return nuevo_responsable
