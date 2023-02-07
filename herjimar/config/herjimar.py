# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": "Activos",
            "items": [
				{
					"type": "doctype",
					"name": "Equipo",
                },
				{
					"type":"doctype",
					"name":"Asignacion Equipo",
				},
				{
					"type": "doctype",
					"name": "Tipo de Equipo",
                },
				{
					"type": "doctype",
					"name": "Clase de Equipo",
                },
				{
					"type": "doctype",
					"name": "Location",
                    "label": _("Location")
                },
				{
					"type": "page",
					"name": "mantenimiento-preven",
					"label": _("Mantenimiento Preventivo"),
					"icon": "fa fa-bar-chart",
					"onboard": 1,
				}
			]
		},
		{
			"label": "Gestión de Proyectos",
			"items": [
				{
					"type":"doctype",
					"name":"Incidencia",
				},
				{
					"type":"doctype",
					"name":"Tipo de Incidencia",
				},
				{
					"type":"doctype",
					"name":"Ordenes de cambio",
				},
				{
					"type":"doctype",
					"name":"Componente",
				}
			]
		}
	]