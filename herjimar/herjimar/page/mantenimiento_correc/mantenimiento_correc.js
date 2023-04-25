frappe.pages['mantenimiento-correc'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Mantenimiento Correctivo',
		single_column: true
	});

	$(frappe.render_template('marco_principal')).appendTo(page.body);
	page.content = $(page.body).find('.principal');


	page.zona_nuevo = $(page.body).find('.zona_nuevo');
/*
	this.boton_nuevo = frappe.ui.form.make_control({
		'parent': page.zona_nuevo,
		'df': {
			'label': 'Añadir nuevo equipo',
			'fieldname': 'Codigo',
			'fieldtype': 'Button',
			btn_size: 'lg', // xs, sm, lg
			'click': () => {
					frappe.pages.mantenimiento_correc.nuevo();
			},


		},
		'render_input': true,
	});*/

	frappe.pages['mantenimiento-correc'].refrescartabla();
}

frappe.pages.mantenimiento_correc=frappe.pages['mantenimiento-correc'];

frappe.pages['mantenimiento-correc'].refrescartabla = function (evento) 
{
	var page = frappe.pages.mantenimiento_correc.page;

	// don't call if already waiting for a response
	if (page.called) return;
	
	page.called = true;
	frappe.call({
		method: 'herjimar.herjimar.page.mantenimiento_correc.mantenimiento_correc.cargatabla',
		args: {
			
		},
		callback: function (r) {
			page.called = false;
			page.body.find('.div_main').remove();
			console.log(r.message);
			$(frappe.render_template('tabla', { revisiones: r.message.revisiones, maquinas: r.message.maquinas })).appendTo(page.content);
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


frappe.pages['mantenimiento-correc'].realizar_mantenimiento = function (evento) {
	
	var page = frappe.pages.mantenimiento_correc.page;
	
	if (page.called) return;

	var maquina=evento.target.getAttribute("data-maquina");
	var revision=evento.target.getAttribute("data-revision");

	d = new frappe.ui.Dialog({
		title: 'Realizar Mantenimiento Correctivo '+maquina,
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
				label: 'Solución',
				fieldname: 'solucion',
				fieldtype: 'Select',
				options: [
					'Cambio escobilla',
					'Reparación y/o sustitución de cable',
					'Cambio rodamiento',
					'Cambio engranaje',
					'Cambio porta fresa',
					'Limpieza y engrase',
					'Otro',
					'Baja'
				],

				reqd: 1
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
				method: 'herjimar.herjimar.page.mantenimiento_correc.mantenimiento_correc.guardar',
				args: {
					valores: values,
					revision: revision						
				},
				callback: function (r) {
					d.hide();
					page.called = false;
					frappe.pages['mantenimiento-correc'].refrescartabla();
				},
				error: function (r) {
					page.called = false;
					alert(r.message);
				}
			});
		}
	});
	
	d.show();
};

frappe.pages['mantenimiento-correc'].nuevo = function (evento) {
		d = new frappe.ui.Dialog({
			title: 'Nuevo Mantenimiento Correctivo',
			fields: [
				{
					label: "Máquina",
					fieldname: "maquina",
					fieldtype: "Link",
					options: "Equipamiento",
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
					label: 'Descripción',
					fieldname: 'descripcion',
					fieldtype: 'Text',
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
					method: 'herjimar.herjimar.page.mantenimiento_correc.mantenimiento_correc.nueva',
					args: {
						valores: values						
					},
					callback: function (r) {
						d.hide();
						page.called = false;
						frappe.pages['mantenimiento-correc'].refrescartabla();
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
