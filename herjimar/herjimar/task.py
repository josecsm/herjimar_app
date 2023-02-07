import frappe
import json
import subprocess
import os


@frappe.whitelist(allow_guest=True)
def enviardocumentacion():
	args = 'cd /var/www/html/erpnext && php artisan monitor:documentacion'
	so = os.popen(args).read()
	return so

@frappe.whitelist(allow_guest=True)
def hazhijos(padre,hijos):

	dpadre = frappe.get_doc('Task', padre)
	log=frappe.logger('herjimar')
	log.info("haciendo padre a "+padre)
	dpadre.is_group=1
	dpadre.save()
	frappe.db.commit()
	log.info('padre hecho')
	obj = json.loads(hijos)
	out = []
	for parten in obj:
		log.info("haciendo hijo a "+parten)
		doc = frappe.get_doc('Task', parten)
		doc.parent_task = padre
		doc.save()
		frappe.db.commit()
		log.info("hijo "+parten+" hecho")
		

@frappe.whitelist(allow_guest=True)
def get_ncc_cliente(doctype, name, links):
	'''Get open count for given transactions and filters

	:param doctype: Reference DocType
	:param name: Reference Name
	:param transactions: List of transactions (json/dict)
	:param filters: optional filters (json/list)'''

	frappe.has_permission(doc=frappe.get_doc(doctype, name), throw=True)
	meta = frappe.get_meta(doctype)
	links = frappe._dict({
		'fieldname': 'odf',
		'transactions': [
			{
				'label': 'NCC Cliente',
				'items': ['NCC Cliente']
			},
		]
	})
	items = []
	for group in links.transactions:
		items.extend(group.get('items'))

	out = []
	for d in items:
		
		data = {'name': d}
		#total = len(frappe.get_all(d, fields='name',
			#filters={fieldname: name}, limit=100, distinct=True, ignore_ifnull=True))
		data['count'] = frappe.db.count('NCC Cliente', {'odf': name})
		out.append(data)

	out = {
		'count': out,
	}

	#module = frappe.get_meta_module(doctype)
	#if hasattr(module, 'get_timeline_data'):
	#	out['timeline_data'] = module.get_timeline_data(doctype, name)
    
	return out

@frappe.whitelist(allow_guest=True)
def get_componentes(doctype, name, links):
	'''Get open count for given transactions and filters

	:param doctype: Reference DocType
	:param name: Reference Name
	:param transactions: List of transactions (json/dict)
	:param filters: optional filters (json/list)'''

	frappe.has_permission(doc=frappe.get_doc(doctype, name), throw=True)
	meta = frappe.get_meta(doctype)
	links = frappe._dict({
		'fieldname': 'odf',
		'transactions': [
			{
				'label': 'Componente',
				'items': ['Componente']
			},
		]
	})
	items = []
	for group in links.transactions:
		items.extend(group.get('items'))

	out = []
	for d in items:
		
		data = {'name': d}
		#total = len(frappe.get_all(d, fields='name',
			#filters={fieldname: name}, limit=100, distinct=True, ignore_ifnull=True))
		data['count'] = frappe.db.count('Componente', {'odf': name})
		out.append(data)

	out = {
		'count': out,
	}

	#module = frappe.get_meta_module(doctype)
	#if hasattr(module, 'get_timeline_data'):
	#	out['timeline_data'] = module.get_timeline_data(doctype, name)
    
	return out


@frappe.whitelist(allow_guest=True)
def get_nombre_odf(hoja_verde,sector='N'):
	
	codhv=hoja_verde[4:10]
	hv=frappe.get_doc('Hoja Verde', hoja_verde)
	cliente=frappe.get_doc('Customer', hv.cliente)
        
	args = 'cd /var/www/html/erpnext && php artisan generar:proximaodf '+cliente.código_xgest+' '+codhv+' '+sector        
	proxima_odf = os.popen(args).read()
	return cliente.código_xgest+"-"+codhv.lstrip("0")+"-"+sector+"-"+proxima_odf

@frappe.whitelist(allow_guest=True)
def get_proxima_hv(interna):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:proximahv "'+interna+'"'
	so = os.popen(args).read()
	return so

@frappe.whitelist(allow_guest=True)
def get_proximo_presupuesto(oferta_previa):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:proximopresupuesto "'+oferta_previa+'"'
	so = os.popen(args).read()
	return so


@frappe.whitelist(allow_guest=True)
def get_sharepoint(tarea):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:sharepoint "'+tarea+'"'
	so = os.popen(args).read()
	html="<ul>"
	if (len(so)>1):
		try:
			obj = json.loads(so)	
			for item in obj:
				if (item["tipo"]=="C") :
					html=html+"<li><i class='fa fa-folder'></i>&nbsp;<a target='_blank' href='"+item["url"]+"'>"+item["nombre"]+"</a></li>"
				else:
					html=html+"<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class='fa fa-file'></i>&nbsp;<a target='_blank' href='"+item["url"]+"'>"+item["nombre"]+"</a></li>"
		except json.decoder.JSONDecodeError:
			pass
	html=html+"</ul><BR><BR>"
	return html

@frappe.whitelist(allow_guest=True)
def get_enlaces(tarea):
    head='<div class="form-grid">'
    head = head + '<div class="grid-heading-row">'
    head = head+'   <div class="grid-row">'
    head = head+'       <div class="data-row row">'
    head = head+'           <div class="col grid-static-col col-xs-3 " data-fieldname="task" data-fieldtype="Link">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Tipo de Objecto</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-9  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Nombre</div>'
    head = head+'           </div>'
    head = head+'       </div>'
    head = head+'   </div>'
    head = head+' </div>'

    head = head+'            <div class="grid-body">'
    head = head+'			    <div class="rows">'
    head = head+'                    <div class="grid-row" data-name="77ac1d7632" data-idx="1">'
    
    tipos_list=frappe.db.get_list('DocField', filters={
        'fieldtype': 'Link',
        'options': 'Task'
    },fields=['name', 'parent','fieldname'])
    for tipo in tipos_list:
        isTable = frappe.db.get_value('DocType', tipo["parent"], 'istable')
        subtipos_list=frappe.db.get_list(tipo["parent"], filters={
            tipo["fieldname"]: tarea
            },fields=['name','parent','parenttype'])        
        for subtipo in subtipos_list:
            if (isTable==0):
                head = head+'                       <div class="data-row row">'
                head = head+'                           <div class="col grid-static-col col-xs-3 " data-fieldname="acción" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis">'+tipo["parent"]+'</div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-9 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+tipo["parent"]+'/'+subtipo["name"]+'">'+subtipo["name"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                        </div>'
            else:
                head = head+'                       <div class="data-row row">'
                head = head+'                           <div class="col grid-static-col col-xs-3 " data-fieldname="acción" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis">'+subtipo["parenttype"]+'</div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-9 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+subtipo["parenttype"]+'/'+subtipo["parent"]+'">'+subtipo["parent"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                        </div>'


    
    head = head+'                    </div>'
    head = head+'                </div>'
    head = head+'		    </div>'
    head = head+'</div>'
    return head