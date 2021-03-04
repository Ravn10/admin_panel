import frappe

def get_context(context):
    context.site = "aniket.snaturalc.in"
    customer_details = get_site_details(context.site)
    context.trial = 1
    context.trial_expiry = "Today"

def get_site_details(site):
    customer = frappe.get_all("Customer",filters={'site':site},fields=['name'])[0]
    subscription = frappe.get_all("Subscription",filters={'party':customer.name},fields=['name'])

def get_subcription_plans():
    pass