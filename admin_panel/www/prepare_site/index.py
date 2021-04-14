no_cache = 1

import frappe
from frappe.core.doctype.user.user import get_timezones
from erpnext.shopping_cart.cart import get_party, get_cart_quotation
from admin_panel.site_utils import create_site_for_saas
from bench_manager.bench_manager.utils import verify_whitelisted_call, safe_decode

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
        customer_doc.customer_detail = str(frappe.form_dict)
        create_site_for_saas(site_name=frappe.form_dict.subdomain,install_erpnext=True,
                    key=format(frappe.utils.datetime.datetime.strftime(frappe.utils.datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")),
                    domain=frappe.form_dict.subdomain)
        context.thanks = "block"
        context.form_3 = "none"
        context.site = frappe.form_dict.subdomain

@frappe.whitelist()
def get_party_():
    return get_party()

# @frappe.whitelist(allow_guest=True)
# def create_site(site_name, install_erpnext, mysql_password, admin_password, key):
# 	verify_whitelisted_call()
# 	commands = ["bench new-site --mariadb-root-password {mysql_password} --admin-password {admin_password} {site_name}".format(site_name=site_name,
# 		admin_password=admin_password, mysql_password=mysql_password)]
# 	if install_erpnext == "true":
# 		with open('apps.txt', 'r') as f:
# 			app_list = f.read()
# 		if 'erpnext' not in app_list:
# 			commands.append("bench get-app erpnext")
# 		commands.append("bench --site {site_name} install-app erpnext".format(site_name=site_name))
# 	frappe.enqueue('bench_manager.bench_manager.utils.run_command',
# 		commands=commands,
# 		doctype="Bench Settings",
# 		key=key
# 	)