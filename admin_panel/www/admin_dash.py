import frappe

def get_context(context):
    context.no_cache = 1
    # innovation_category = frappe.sql_list('''select name from `tabInnovation Category` ''')
    path = frappe.form_dict
    print(path)
    context.users = frappe.db.sql_list(''' select full_name from tabUser''')
    context.data = frappe.db.sql('''select name, owner, creation, subject, count(*) as nos from `tabActivity Log`  group by creation order by creation  limit 300''',as_dict=1)
    if "gender" in frappe.form_dict:
        context.gender = frappe.form_dict.gender

def get_data_range(month):
    pass