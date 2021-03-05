no_cache = 1

import frappe
from frappe.core.doctype.user.user import get_timezones
from erpnext.shopping_cart.cart import get_party
from admin_panel.site_utils import create_site_for_saas

def get_context(context):
    context.company_domain = frappe.db.get_single_value("SAAS Settings","saas_domain")
    context.countries = frappe.db.sql_list('''select name from `tabCountry`''')
    context.currencies = frappe.db.sql_list('''select name from `tabCurrency`''')
    context.languages = frappe.db.sql_list('''select language_name from `tabLanguage`''')
    context.timezones = get_timezones()['timezones']
    context.domains = frappe.db.sql_list('''select name from `tabDomain`''')
    context.thanks = "none"
    context.title = frappe.session.user

    if frappe.form_dict.subdomain:
        context.title = frappe.form_dict.subdomain
        customer_doc =  get_party()
        customer_doc.site = frappe.form_dict.subdomain
        customer_doc.customer_detail = str(frappe.form_dict)
        create_site_for_saas(site_name=frappe.form_dict.subdomain,install_erpnext=True,
                    key=format(frappe.utils.datetime.date.today()),
                    domain=frappe.form_dict.subdomain)
        context.thanks = "block"
        context.form_3 = "none"