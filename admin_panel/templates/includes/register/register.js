function myFunction(){
	frappe.msgprint("Hello there")
};

function create_customer(){
	frappe.call({
		method: "admin_panel.www.register.create_customer",
		args: {
			"firstname": $("#first_name").val(),
			"lastname": $("#last_name").val(),
			"email": $("#email_id").val(),
			"mobile_no": $("#phone_number").val(),
			// "sponser": $("#input-sponser").val(),
			// "address1": $("#input-address-1").val(),
			// "address2": $("#input-address-2").val(),
			// "zone": $("#input-zone").val(),
			// "city": $("#input-city").val(),
			// "postcode": $("#input-postcode").val(),
			// "country": $("#input-country").val(),
			// "password": $("#input-password").val(),
			// "redirect_to": frappe.utils.get_url_arg("redirect-to") || ''
		},
		freeze:true,
		callback: function(r) {
			console.log(r.message)
			if (r.message) {
				window.location.href="success?message="+r.message;
				window.location.href="signup-flow-2?message="+r.message;
			}
		}
	});
}
