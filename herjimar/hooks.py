# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "herjimar"
app_title = "Herjimar"
app_publisher = "Herjimar"
app_description = "Modificaciones para Herjimar"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "erp@herjimar.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/herjimar/css/herjimar.css"
app_include_js = ["/assets/herjimar/js/herjimar.js","/assets/herjimar/js/timesheet_list.js","/assets/herjimar/js/riesgo_list.js","/assets/herjimar/js/evaluacion_list.js"]

# include js, css files in header of web template
# web_include_css = "/assets/herjimar/css/herjimar.css"
# web_include_js = "/assets/herjimar/js/herjimar.js"

# include js in page
# page_js = {"page" : "public/js/file.js"} 

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {
    "Timesheet": "public/js/timesheet_list.js",
    "Riesgo": "public/js/riesgo_list.js",
    "Evaluacion del Desempeno": "public/js/evaluacion_list.js"
}
#    "Timesheet": "public/js/timesheet_list.js",

# # doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "herjimar.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "herjimar.install.before_install"
# after_install = "herjimar.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "herjimar.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
    "Incidencia":{
        "after_insert": "herjimar.crud_events.after_insert_Incidencia",
        "on_update": "herjimar.crud_events.on_update_Incidencia"
    },
    "Hoja Verde":{
        "after_insert": "herjimar.crud_events.after_insert_HV",
        "on_update": "herjimar.crud_events.on_update_HV"
    },
    "Task":{
        "on_update": "herjimar.crud_events.on_update_Task"
    },
    "Project":{
        "after_insert": "herjimar.crud_events.after_insert_proyecto",
         "on_update": "herjimar.crud_events.on_update_proyecto"
    },
    "Quotation":{
        "before_save": "herjimar.crud_events.before_save_quotation",
       # "after_save": "herjimar.crud_events.on_update_quotation",
       # "on_update": "herjimar.crud_events.on_update_quotation"
    },
    "Shift Request":{
        "on_submit": "herjimar.crud_events.on_submit_shift_request", 
    },
    "Leave Application":{
        "on_submit": "herjimar.crud_events.on_submit_leave_application", 
    },
    "Revision Equipamiento":{
        "after_insert":"herjimar.crud_events.after_insert_revision_equipamiento",
    },
    #"Task":{
    #    "before_insert": "herjimar.crud_events.before_insert_task"
    #},
    #"Task":{
    #    "before_insert": "herjimar.crud_events.after_insert_File",
    ##    "after_insert": "herjimar.crud_events.after_insert_File",
    #    "before_save": "herjimar.crud_events.after_insert_File",
    #    "on_update": "herjimar.crud_events.after_insert_File"
    #},
    #"File": {
  	#	"before_insert": "pibiapp.nextcloud.nextcloud_link.nextcloud_before_insert",
 	#	"after_insert": "pibiapp.nextcloud.nextcloud_link.nextcloud_insert",
 	#	"on_trash": "pibiapp.nextcloud.nextcloud_link.nextcloud_before_delete",
 	#	"after_delete": "pibiapp.nextcloud.nextcloud_link.nextcloud_delete",
 	#	"get_content": "pibiapp.nextcloud.nextcloud_link.get_content"
	#},
    "Issue":{
        "after_insert": "herjimar.crud_events.after_insert_Issue",
    },
    "Employee":{
         "on_update": "herjimar.crud_events.on_update_employee",
    },
    "File":{
    #    "before_insert": "herjimar.crud_events.after_insert_File",
        "after_insert": "herjimar.crud_events.after_insert_File",
        "after_delete": "herjimar.crud_events.after_delete_File",
    #    "before_save": "herjimar.crud_events.after_insert_File",
    #    "on_update": "herjimar.crud_events.after_insert_File"
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"herjimar.tasks.all"
# 	],
# 	"daily": [
# 		"herjimar.tasks.daily"
# 	],
# 	"hourly": [
# 		"herjimar.tasks.hourly"
# 	],
# 	"weekly": [
# 		"herjimar.tasks.weekly"
# 	]
# 	"monthly": [
# 		"herjimar.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "herjimar.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "herjimar.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "herjimar.task.get_dashboard_data"
# }
override_doctype_dashboards = {
#    "Hoja Verde": "herjimar.herjimar.hoja_verde_dashboard"
}

fixtures = ["DocType","DocField","Custom Field","Custom DocPerm","Custom Script","Property Setter","Print Format"]