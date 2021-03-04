import frappe
from frappe.model.document import Document
from subprocess import check_output, Popen, PIPE
import os, re, json, time, pymysql, shlex
from bench_manager.bench_manager.utils import verify_whitelisted_call, safe_decode
from frappe.utils.password import get_decrypted_password
from bench_manager.bench_manager.doctype.site.site import create_site
import subprocess
from bench_manager.bench_manager.utils import run_command

@frappe.whitelist()
def create_site_for_saas(site_name, install_erpnext, key, domain):
    mysql_password = get_decrypted_password("SAAS Settings","SAAS Settings","db_password")
    admin_password = get_decrypted_password("SAAS Settings","SAAS Settings","admin_password")
    custom_domain = domain + "."+ frappe.db.get_single_value("SAAS Settings","saas_domain")
    # site_domain_map = frappe.get_doc({
    #                             "doctype":"Site Domain Map",
    #                             "site":site_name,
    #                             "domain":custom_domain
    #                         })
    # site_domain_map.insert()
    frappe.db.commit()
    create_site(site_name, install_erpnext, mysql_password, admin_password, key)

def update_custom_domain(doc, method=None):
    key =str(frappe.utils.datetime.datetime.now())
    domain = doc.domain
    site_name = doc.name
    doctype = "SAAS Settings"
    commands = ["bench setup add-domain {domain} --site {site_name}".format(domain=domain, site_name=site_name)]
    run_command(commands, doctype, key, cwd='..', docname=' ')
    frappe.msgprint(commands)
    subprocess.call("sudo service nginx reload", shell=True)

def send_email_on_site_creation(doc,method=None):
    if doc.status == "Success":
        pass
    pass