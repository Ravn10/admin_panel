from __future__ import unicode_literals
from frappe import _


def get_data():
	bench_setup = {
		"label": _("SAAS Setup"),
		"icon": "octicon octicon-briefcase",
		"items": [
			{
				"name": "SAAS Settings",
				"type": "doctype",
				"label": _("SAAS Settings"),
				"description": _("SAAS Settings")
			},
			{
				"name": "Site Info",
				"type": "doctype",
				"label": _("Site Info"),
				"description": _("Site Info")
			}
		]
	}

	return [
		bench_setup
	]
