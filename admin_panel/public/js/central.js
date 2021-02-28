let controller;

frappe.ready(() => {
	controller = new SignupController("user-signup", {
		// will load the last step the user was on after page reload
		save_state: true,
	});

	// get subdomain is set in url and show first form
	set_subdomain_from_url();

	// load country, currency, language select options
	load_dropdowns();
});

// this needs to be on global scope
var field_validators = {
	subdomain: (value) => {
		let MIN_LENGTH = 4;
		let MAX_LENGTH = 20;
		if (value.length < MIN_LENGTH) {
			return `Site name cannot have less than ${MIN_LENGTH} characters`;
		}
		if (value.length > MAX_LENGTH) {
			return `Site name cannot have more than ${MAX_LENGTH} characters`;
		}
		if (!/^[a-z0-9][a-z0-9-]*[a-z0-9]$/.test(value)) {
			return "Site name should contain lowercase alphabets, numbers, and hyphens";
		}
	},
	phone_number: (value) => {
		let regExp = /[a-zA-Z]/g;
		if (regExp.test(value)) {
			return "Phone number cannot contain alphabets";
		}
	},
	email: (value) => {
		if (!valid_email(value)) {
			return "Invalid email";
		}
	},
	password: (value) => {
		return value.length < 6 ? "Password must be atleast 6 characters" : "";
	},
	terms_check: (value) => {
		if (!value) {
			return "You must agree to terms and conditions";
		}
	},
	otp: (value) => {
		if (!value) {
			return "Verification Code cannot be blank";
		}
	},
	users: (value) => {
		if (value < window.minimum_user_count) {
			return (
				"Number of users must be greater than " +
				window.minimum_user_count
			);
		}
		if (value > 100000) {
			return "Number of users must be less than 100000";
		}
	},
	designation: (value) => {
		if (!value) {
			return "Designation cannot be blank";
		}
	},
	referral_source: (value) => {
		if (!value) {
			return "Referral source cannot be blank";
		}
	},
};

function validate_and_submit_personal_details($form, values) {
	goog_report_conversion();

	let location_params = localStorage.getItem("urlKeywordParams");
	if (location_params) {
		let url_params = new URLSearchParams(location_params);
		let ga_params = {
			keyword: url_params.get("utm_keyword"),
			utm_source: url_params.get("utm_source"),
			campaignid: url_params.get("utm_campaign"),
			adgroupid: url_params.get("adgroupid"),
			loc_physical_ms: url_params.get("utm_loc_physical_ms"),
			vertical: url_params.get("vertical"),
		};
		values["ga_params"] = ga_params;
	}

	return call(
		"central.www.signup.signup",
		{
			first_name: values.first_name,
			last_name: values.last_name,
			email: values.email,
			phone_number: values.phone_number,
			subdomain: values.subdomain,
			passphrase: values.password,
			ga_params: values.ga_params,
			plan: frappe.utils.get_url_arg("plan") || "",
			partner:
				frappe.utils.get_url_arg("referral-id") ||
				get_if_not_expired("referral_id"),
		},
		$form
	).then((r) => {
		if (r.message.reference) {
			localStorage.setItem("account_request", r.message.reference);
			$(".verify-otp-email").text(r.message.email);
		}
	});
}

function verify_otp($form, values) {
	return call(
		"central.www.prepare_site.verify_account_request",
		{
			otp: values.otp,
			id: localStorage.getItem("account_request"),
		},
		$form
	);
}

function regional_settings($form, values) {
	return call(
		"central.www.prepare_site.update_account_request",
		{
			id: localStorage.getItem("account_request"),
			country: values.country,
			domain: values.domain,
			currency: values.currency,
			language: values.language,
			timezone: values.timezone,
		},
		$form
	);
}

function business_settings($form, values) {
	return call(
		"central.www.prepare_site.update_account_request",
		{
			id: localStorage.getItem("account_request"),
			company: values.company,
			users: values.users,
			designation: values.designation,
			referral_source: values.referral_source,
			signup_referrer: get_if_not_expired("referral_id")
				? "Partner Referral"
				: "",
		},
		$form
	).then((r) => {
		redirect_to_prepare_site();
	});
}

function resend_otp(e) {
	e.preventDefault();
	return frappe.call({
		method: "central.www.prepare_site.resend_otp",
		args: {
			id: localStorage.getItem("account_request"),
		},
		btn: e.target,
	});
}

function set_subdomain_from_url() {
	let query_params = frappe.utils.get_query_params();
	if (query_params.domain) {
		let subdomain = query_params.domain.replace(
			"." + window.signup_domain,
			""
		);
		$('input[name="subdomain"]').val(subdomain).trigger("change");
	}
}

function call(method, args, $form) {
	return frappe
		.call({
			method,
			args,
			type: "POST",
			btn: $form.find("button.btn-primary"),
		})
		.then((r) => {
			if (r.exc) {
				console.error("An error occurred", r.exc);
				return;
			}
			return r;
		});
}

function validate_subdomain(input) {
	let $input = $(input);
	let subdomain = $input.val();
	let error = controller.validate_value("subdomain", subdomain);
	if (error) {
		controller.show_input_error("subdomain", error);
	} else {
		check_if_available(subdomain).then((available) => {
			controller.show_input_error(
				"subdomain",
				!available ? `${subdomain}.erpnext.com is already taken` : ""
			);
		});
	}
}

function load_dropdowns() {
	frappe.call({
		method: "central.www.signup.load_dropdowns",
		callback: function (r) {
			let $country_select = $("select[name=country]").append(
				r.message.countries
					.map((country_name) => {
						return `<option>${country_name}</option>`;
					})
					.join("")
			);

			let $language_select = $("select[name=language]");
			r.message.languages.forEach((language) => {
				//language[0] is for language code and language[1] is for language name
				$language_select.append(
					$("<option />").val(language[0]).text(language[1])
				);
			});

			let $timezone_select = $("select[name=timezone]");
			r.message.all_timezones.forEach((timezone) => {
				$timezone_select.append(
					$("<option />").val(timezone).text(timezone)
				);
			});

			let $currency_select = $("select[name=currency]");
			r.message.currencies.forEach((currency) => {
				$currency_select.append(
					$("<option />").val(currency).text(currency)
				);
			});

			let country_info = r.message.country_info;

			$country_select.on("change", function () {
				let country = $(this).val();
				$timezone_select.val(country_info[country].timezones[0]);
				$currency_select.val(country_info[country].currency);
			});

			$language_select.val("en");
			if (r.message.default_country) {
				$country_select.val(r.message.default_country);
			} else {
				$country_select.val("India");
			}
			$country_select.trigger("change");
		},
	});
}

function check_if_available(subdomain) {
	return frappe
		.call({
			method: "central.www.signup.check_subdomain_availability",
			args: { subdomain },
			type: "POST",
		})
		.then((r) => {
			if (!r.message) {
				return true;
			}
			return false;
		});
}

function get_if_not_expired(key) {
	const value = localStorage.getItem(key);
	if (!value) {
		return null;
	}

	const value_obj = JSON.parse(value);
	const now = new Date();
	if (now.getTime() > value_obj.expiry) {
		localStorage.removeItem(key);
		return null;
	}
	return value_obj.value;
}

function redirect_to_prepare_site() {
	window.location.href = "/prepare_site";
}