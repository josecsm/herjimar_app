import frappe
import datetime

@frappe.whitelist(allow_guest=True)
def cancelar(equipo,fecha,tipo,operario=None,obs=None):
    frappe.db.sql("delete from `tabRevision Equipo` where parent = %s and fecha= %s and operario=%s and obs=%s", equipo, fecha, tipo)			
    doc = frappe.get_doc('Equipo', equipo)
    doc.save()
    frappe.db.commit()
    return "cancelar"

@frappe.whitelist(allow_guest=True)
def crear_hijo_equipo(equipo,fecha,tipo,operario=None,obs=None):
    frappe.logger().info("Zzzzzzzzzz")
			
    doc = frappe.get_doc('Equipo', equipo)
    if doc.fecha_última_acción_realizada is "" or doc.fecha_última_acción_realizada is None or doc.fecha_última_acción_realizada.strftime("%Y-%m-%d")<fecha:
        doc.fecha_última_acción_realizada=fecha
        doc.última_acción_realizada=tipo
        frappe.logger().info("Ultima accion vacia ahora rellena")
    else:
        frappe.logger().info("Ultima accion NO vacia")
    proxima=bool(False)
    for x in doc.acciones:
        frappe.logger().info("accion")
        frappe.logger().info(x.acción)
        if (x.acción==tipo):
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            if (x.periodicidad=="Anual"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 1)
                proxima=bool(True)
            if (x.periodicidad=="Bianual"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 2)
                proxima=bool(True)
            if (x.periodicidad=="Bienal"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 2)
                proxima=bool(True)
            if (x.periodicidad=="Trienal"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 3)
                proxima=bool(True)
            if (x.periodicidad=="Cuatrienal"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 4)
                proxima=bool(True)
            if (x.periodicidad=="Quinquenal"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 5)
                proxima=bool(True)
            if (x.periodicidad=="Decenal"):
                fecha_obj=fecha_obj.replace(year = fecha_obj.year + 10)
                proxima=bool(True)
            if (x.periodicidad=="Semestral"):
                nuevomes=fecha_obj.month+6
                if (nuevomes>12):
                    nuevomes=nuevomes-12
                fecha_obj=fecha_obj.replace(month = nuevomes)
                proxima=bool(True)
            if (x.periodicidad=="Cuatrimestral"):
                nuevomes=fecha_obj.month+4
                if (nuevomes>12):
                    nuevomes=nuevomes-12
                fecha_obj=fecha_obj.replace(month = nuevomes)
                proxima=bool(True)
    if (proxima):
        if doc.fecha_próxima_acción is "" or doc.fecha_próxima_acción is None or doc.fecha_próxima_acción<fecha_obj.date():
            doc.fecha_próxima_acción=fecha_obj.date()
            doc.proxima_acción=tipo
    doc.append('revisiones', {
        'fecha': fecha,
        'operario': operario,
        'tipo': tipo,
        'observaciones': obs,
    })


    doc.save()
    frappe.db.commit()
    return ""
    