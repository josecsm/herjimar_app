import frappe
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def nueva_evaluacion_app(jefe,empleado,estrellas,observaciones):

	log=frappe.logger('herjimar')
	log.info('evaluacion de '+jefe)
	ojefe=frappe.db.get_value('Employee',{'user_id':jefe},'name')
	log.info('evaluacion de (name) '+ojefe)
	log.info('evaluacion para '+empleado)
	try:
	    doc=frappe.new_doc('Valoracion Encargado')
	    doc.encargado=ojefe
	    doc.empleado=empleado
	    doc.valoracion=estrellas
	    doc.observaciones=observaciones
	    doc.fecha=datetime.now()
	    log.info("voy a insertar "+str(doc));
	    doc.insert()
	    log.info("todo creado correctamente");
	    return "OK"
	except Exception as e:
	    s=str(e)
	    return "ERROR"