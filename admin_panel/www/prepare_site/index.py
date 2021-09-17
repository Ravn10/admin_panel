no_cache = 1

import frappe
from frappe.core.doctype.user.user import get_timezones
from erpnext.shopping_cart.cart import get_party, get_cart_quotation
from admin_panel.site_utils import create_site_for_saas
from bench_manager.bench_manager.utils import verify_whitelisted_call, safe_decode

def get_context(context):
    context.company_domain = frappe.db.get_single_value("SAAS Settings","saas_domain")
    context.countries = frappe.db.sql_list('''select name from `tabCountry`''')
    # context.currencies = frappe.db.sql_list('''select name from `tabCurrency`''')
    # context.languages = frappe.db.sql_list('''select language_name from `tabLanguage`''')
    # context.timezones = get_timezones()['timezones']
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
        try:
            request_args = {
                'site':frappe.form_dict.subdomain,
                'subdomain':frappe.form_dict.subdomain,
                'domain':frappe.form_dict.domain,
                'company':frappe.form_dict.company,
                'country':frappe.form_dict.country,
                'source':frappe.form_dict.source,
                'customer':get_party().get('name'),
                'user':frappe.session.user,
                'company':frappe.form_dict.company,
                'no_of_users':frappe.form_dict.users
            }
        except:
            pass
        if request_args:
            prepare_site_request(request_args)

@frappe.whitelist()
def get_party_():
    return get_party()

# create site preparation request
@frappe.whitelist(allow_guest=True)
def prepare_site_request(args):
    psr = frappe.get_doc({"doctype":"Prepare Site Request"})
    psr.update(args)
    psr.insert(ignore_permissions=True)