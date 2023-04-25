frappe.pages['mantenimiento-preven'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Mantenimiento Preventivo',
		single_column: true
	});


	$(frappe.render_template('marco_principal')).appendTo(page.body);
	page.content = $(page.body).find('.principal');

	page.filtrocodigo = $(page.body).find('.filtro-codigo');
	page.filtroclase = $(page.body).find('.filtro-clase');
	page.filtroresponsable = $(page.body).find('.filtro-responsable');

	this.selectcodigo = frappe.ui.form.make_control({
		'parent': page.filtrocodigo,
		'df': {
			'label': 'Indique Codigo HM',
			'fieldname': 'Codigo',
			'fieldtype': 'Link',
			'options': 'Equipamiento',
			'onchange': () => {
					frappe.pages.mantenimiento_preven.refrescartabla();
			},


		},
		'render_input': true,
	});

	this.selectclase = frappe.ui.form.make_control({
		'parent': page.filtroclase,
		'df': {
			'label': 'Seleccione Clase',
			'fieldname': 'Clase',
			'fieldtype': 'Link',
			'options': 'Clase de Equipo',
			'onchange': () => {
				frappe.pages.mantenimiento_preven.refrescartabla();
			},

		},
		'render_input': true,
	});

	this.selectresponsable = frappe.ui.form.make_control({
		'parent': page.filtroresponsable,
		'df': {
			'label': 'Seleccione Responsable',
			'fieldname': 'Responsable',
			'fieldtype': 'Link',
			'options': 'Employee',
			'onchange': () => {
				frappe.pages.mantenimiento_preven.refrescartabla();
			},

		},
		'render_input': true,
	});

	frappe.pages.mantenimiento_preven.refrescartabla();
}

frappe.pages.mantenimiento_preven=frappe.pages['mantenimiento-preven'];

frappe.pages['mantenimiento-preven'].realizar_mantenimiento = function (evento) {
	
	var page = frappe.pages.mantenimiento_preven.page;
	
	if (page.called) return;

	var maquina=evento.target.getAttribute("data-maquina");
	var plantilla=evento.target.getAttribute("data-plantilla");

	if (plantilla=="Grupos de Soldar"){
		var intensidades=evento.target.getAttribute("data-intensidad").split("_");
		var voltajes=evento.target.getAttribute("data-voltaje").split("_");
		frappe.pages['mantenimiento-preven'].formSoldar(maquina,intensidades[0],intensidades[1],intensidades[2],voltajes[0],voltajes[1],voltajes[2]);
	}else if (plantilla=="Estufas"){
		var medidas=evento.target.getAttribute("data-medidas").split("_");
		frappe.pages['mantenimiento-preven'].formEstufas(maquina,medidas[0],medidas[1],medidas[2]);
	}else if (plantilla=="Hornos"){
		var medidas=evento.target.getAttribute("data-medidas").split("_");
		frappe.pages['mantenimiento-preven'].formHornos(maquina,medidas[0],medidas[1]);
	}else if (plantilla=="Genérica"){
		frappe.pages['mantenimiento-preven'].formGenerica(maquina,evento.target.getAttribute("data-hacer"));
	}else{
	
		frappe.throw(__('Plantilla Desconocida:'+plantilla));
	}
};


frappe.pages['mantenimiento-preven'].formGenerica = function (maquina,hacer) {

	d = new frappe.ui.Dialog({
		title: 'Mantenimiento Genérico '+maquina,
		fields: [
			{
				label: 'Fecha',
				fieldname: 'fecha',
				fieldtype: 'Date',
				reqd: 1
			},
			{
				label: 'Horas',
				fieldname: 'horas',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: "Empleado",
				fieldname: "empleado",
				fieldtype: "Link",
				options: "Employee",
				reqd: 1
			},
			{
				label: 'Actuación',
				fieldname: 'actuacion',
				fieldtype: 'Text',
				default: hacer,
			},
			{
				label: 'Resultado',
				fieldname: 'resultado',
				fieldtype: 'Select',
				options: [
					'Ok',
					'No Ok'
				],
				reqd: 1
			},
			{
				label: 'Observaciones',
				fieldname: 'observaciones',
				fieldtype: 'Small Text',
			},
		],
		primary_action_label: 'Guardar',
		primary_action(values) {
			frappe.call({
				method: 'herjimar.herjimar.page.mantenimiento_preven.mantenimiento_preven.revision_generica',
				args: {
					valores: values,
					maquina: maquina
				},
				callback: function (r) {
					d.hide();
					frappe.pages['mantenimiento-preven'].refrescartabla();
				},
				error: function (r) {
					page.called = false;
					alert(r.message);
				}
			});
		}
	});
	//d.fields_dict.actuacion.val(hacer);
	
	/*d.fields_dict.actuacion.$wrapper.html('<div class="clearfix">									<label class="control-label" style="padding-right: 0px;">Acción a realizar</label>							</div>		<div class="control-input-wrapper">									<div class="control-input" style="display: block;">				<div class="link-field ui-front" style="position: relative; line-height: 1;">								<div class="awesomplete">						<textarea rows="10" id="mytextarea" class="input-with-feedback form-control bold" autocomplete="off" wrap="off" style="overflow:auto">'+hacer+'</textarea>					</div>							</div>			</div>								</div>		');
	$('#mytextarea').keypress(function(event){
		event.preventDefault();
	});*/
	d.show();
}

frappe.pages['mantenimiento-preven'].formHornos = function (maquina,m1,m2) {

	d = new frappe.ui.Dialog({
		title: 'Mantenimiento Hornos '+maquina,
		fields: [
			{
				label: 'Fecha',
				fieldname: 'fecha',
				fieldtype: 'Date',
				reqd: 1
			},
			{
				label: 'Horas',
				fieldname: 'horas',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: "Empleado",
				fieldname: "empleado",
				fieldtype: "Link",
				options: "Employee",
				reqd: 1
			},
			{
				label: 'Medidas tras precalentamiento ('+m1+'º)',
				fieldname: 'medidas1',
				fieldtype: 'Data',
				reqd: 1,
				description: 'Separar los valores por coma , '
			},
			{
				label: 'Medidas tras 1 horas de precalentamiento ('+m2+'º)',
				fieldname: 'medidas2',
				fieldtype: 'Data',
				reqd: 1,
				description: 'Separar los valores por coma , '
			},
			{
				label: 'Observaciones',
				fieldname: 'observaciones',
				fieldtype: 'Small Text',
			},
		],
		primary_action_label: 'Guardar',
		primary_action(values) {
			frappe.call({
				method: 'herjimar.herjimar.page.mantenimiento_preven.mantenimiento_preven.revision_horno',
				args: {
					valores: values,
					maquina: maquina
				},
				callback: function (r) {
					d.hide();
					frappe.pages['mantenimiento-preven'].refrescartabla();
				},
				error: function (r) {
					page.called = false;
					alert(r.message);
				}
			});
		}
	});

	d.show();
}

frappe.pages['mantenimiento-preven'].formEstufas = function (maquina,m1,m2,m3) {

	d = new frappe.ui.Dialog({
		title: 'Mantenimiento Estufas '+maquina,
		fields: [
			{
				label: 'Fecha',
				fieldname: 'fecha',
				fieldtype: 'Date',
				reqd: 1
			},
			{
				label: 'Horas',
				fieldname: 'horas',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: "Empleado",
				fieldname: "empleado",
				fieldtype: "Link",
				options: "Employee",
				reqd: 1
			},
			{
				label: 'Medidas tras precalentamiento (80º)',
				fieldname: 'medidas1',
				fieldtype: 'Data',
				reqd: 1,
				description: 'Separar los valores por coma , '
			},
			{
				label: 'Medidas tras 1 horas de precalentamiento (100º)',
				fieldname: 'medidas2',
				fieldtype: 'Data',
				reqd: 1,
				description: 'Separar los valores por coma , '
			},
			{
				label: 'Medidas tras 2 horas precalentamiento (110º)',
				fieldname: 'medidas3',
				fieldtype: 'Data',
				reqd: 1,
				description: 'Separar los valores por coma , '
			},
			{
				label: 'Observaciones',
				fieldname: 'observaciones',
				fieldtype: 'Small Text',
			},
		],
		primary_action_label: 'Guardar',
		primary_action(values) {
			frappe.call({
				method: 'herjimar.herjimar.page.mantenimiento_preven.mantenimiento_preven.revision_estufa',
				args: {
					valores: values,
					maquina: maquina
				},
				callback: function (r) {
					d.hide();
					frappe.pages['mantenimiento-preven'].refrescartabla();
				},
				error: function (r) {
					page.called = false;
					alert(r.message);
				}
			});
		}
	});

	d.show();
}

frappe.pages['mantenimiento-preven'].formSoldar = function (maquina,i1,i2,i3,v1,v2,v3) {

	d = new frappe.ui.Dialog({
		title: 'Mantenimiento Grupo de Soldar '+maquina,
		fields: [
			{
				label: 'Fecha',
				fieldname: 'fecha',
				fieldtype: 'Date',
				reqd: 1
			},
			{
				label: 'Horas',
				fieldname: 'horas',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: "Empleado",
				fieldname: "empleado",
				fieldtype: "Link",
				options: "Employee",
				reqd: 1
			},
			{
				label: 'Intensidad Medida para '+i1,
				fieldname: 'imedida1',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Intensidad Medida para '+i2,
				fieldname: 'imedida2',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Intensidad Medida para '+i3,
				fieldname: 'imedida3',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Voltaje Medido para '+v1,
				fieldname: 'vmedido1',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Voltaje Medido para '+v2,
				fieldname: 'vmedido2',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Voltaje Medido para '+v3,
				fieldname: 'vmedido3',
				fieldtype: 'Float',
				reqd: 1
			},
			{
				label: 'Observaciones',
				fieldname: 'observaciones',
				fieldtype: 'Small Text',
			},
		],
		primary_action_label: 'Guardar',
		primary_action(values) {
			frappe.call({
				method: 'herjimar.herjimar.page.mantenimiento_preven.mantenimiento_preven.revision_soldadura',
				args: {
					valores: values,
					maquina: maquina
				},
				callback: function (r) {
					d.hide();
					frappe.pages['mantenimiento-preven'].refrescartabla();
				},
				error: function (r) {
					page.called = false;
					alert(r.message);
				}
			});
		}
	});

	d.show();
}

frappe.pages['mantenimiento-preven'].refrescartabla = function () {
	var page = frappe.pages.mantenimiento_preven.page;

	// don't call if already waiting for a response
	if (page.called) return;

	const codigo = this.selectcodigo.get_value();
	const clase = this.selectclase.get_value();
	const responsable = this.selectresponsable.get_value();
	
	page.called = true;
	frappe.call({
		method: 'herjimar.herjimar.page.mantenimiento_preven.mantenimiento_preven.cargatabla',
		args: {
			codigo: codigo,
			clase: clase,
			responsable: responsable
		},
		callback: function (r) {
			page.called = false;
			page.body.find('.div_main').remove();
			console.log(r.message);
			$(frappe.render_template('tabla', { maquinas: r.message.maquinas })).appendTo(page.content);
			//$(".celda").click(function () { frappe.pages.planificacion.nuevaentrada($(this).attr("data-empleado"), $(this).attr("data-fecha")); });
			//$(".progress").click(function (event) { frappe.pages.planificacion.editarentrada($(this).attr("data-asignacion")); event.stopPropagation(); });
			//$(".fa-trash").click(function (event) { frappe.pages.planificacion.borrarentrada($(this).attr("data-asignacion")); event.stopPropagation(); });
			//$(".boton-informe").click(function (event) { frappe.pages.planificacion.imprimir(); event.stopPropagation(); });
			
		},
		error: function (r) {
			page.called = false;
			alert(r.message);
		}
	});
};

