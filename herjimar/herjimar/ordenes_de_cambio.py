import frappe
import os
import json

@frappe.whitelist(allow_guest=True)
def get_sharepoint(oc):
	
	args = 'cd /var/www/html/erpnext && php artisan generar:sharepointoc "'+oc+'"'
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
def get_enlaces(oc):
    head='<div class="form-grid">'
    head = head + '<div class="grid-heading-row">'
    head = head+'   <div class="grid-row">'
    head = head+'       <div class="data-row row">'
    head = head+'           <div class="col grid-static-col col-xs-3 " data-fieldname="task" data-fieldtype="Link">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Tipo de Objecto</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-3  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Nombre</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-3  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Total Coste de la Incidencia</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-3  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">Impacto en horas</div>'
    head = head+'           </div>'
    head = head+'       </div>'
    head = head+'   </div>'
    head = head+' </div>'

    head = head+'            <div class="grid-body">'
    head = head+'			    <div class="rows">'
    head = head+'                    <div class="grid-row" data-name="77ac1d7632" data-idx="1">'
    
    tipos_list=frappe.db.get_list('DocField', filters={
        'fieldtype': 'Link',
        'options': 'Ordenes de Cambio'
    },fields=['name', 'parent','fieldname'])
    total_coste=0
    total_horas=0
    for tipo in tipos_list:
        isTable = frappe.db.get_value('DocType', tipo["parent"], 'istable')
        subtipos_list=frappe.db.get_list(tipo["parent"], filters={
            tipo["fieldname"]: oc
            },fields=['name','parent','parenttype','total_coste_de_la_incidencia','impacto_horas'])        
        
        for subtipo in subtipos_list:
            if (isTable==0):
                total_coste+=subtipo["total_coste_de_la_incidencia"]
                total_horas+=subtipo["impacto_horas"]
                head = head+'                       <div class="data-row row">'
                head = head+'                           <div class="col grid-static-col col-xs-3 " data-fieldname="acción" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis">'+tipo["parent"]+'</div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+tipo["parent"]+'/'+subtipo["name"]+'">'+subtipo["name"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+tipo["parent"]+'/'+subtipo["name"]+'">'+str(subtipo["total_coste_de_la_incidencia"])+'&euro;</a></div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+tipo["parent"]+'/'+subtipo["name"]+'">'+str(subtipo["impacto_horas"])+'</a></div>'
                head = head+'                            </div>'
                head = head+'                        </div>'
            else:
                head = head+'                       <div class="data-row row">'
                head = head+'                           <div class="col grid-static-col col-xs-3 " data-fieldname="acción" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis">'+subtipo["parenttype"]+'</div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+subtipo["parenttype"]+'/'+subtipo["parent"]+'">'+subtipo["parent"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+subtipo["parenttype"]+'/'+subtipo["parent"]+'">'+subtipo["parent"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                            <div class="col grid-static-col col-xs-3 " data-fieldname="periodicidad" data-fieldtype="Select">'
                head = head+'                                <div class="field-area" style="display: none;"></div>'
                head = head+'                                <div class="static-area ellipsis"><a href="/desk#Form/'+subtipo["parenttype"]+'/'+subtipo["parent"]+'">'+subtipo["parent"]+'</a></div>'
                head = head+'                            </div>'
                head = head+'                        </div>'

   # head = head + '<div class="grid-heading-row">'
   # head = head+'   <div class="grid-row">'
    head = head+'       <div class="data-row row">'
    head = head+'           <div class="col grid-static-col col-xs-6 " data-fieldname="task" data-fieldtype="Link">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">TOTAL</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-3  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">'+str(total_coste)+'&euro;</div>'
    head = head+'           </div>'
    head = head+'           <div class="col grid-static-col col-xs-3  grid-overflow-no-ellipsis" data-fieldname="subject" data-fieldtype="Text">'
    head = head+'               <div class="field-area" style="display: none;"></div>'
    head = head+'               <div class="static-area ellipsis">'+str(total_horas)+'</div>'
    head = head+'           </div>'
    head = head+'       </div>'
   # head = head+'   </div>'
   # head = head+' </div>'

    
    head = head+'                    </div>'
    head = head+'                </div>'
    head = head+'		    </div>'





    head = head+'</div>'
    return head