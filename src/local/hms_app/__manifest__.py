{
    "name": "hms_app",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "sequence": -1000,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "views/assets.xml",
        "views/login.xml",
        # Room Management
        # Room Management > Room Types
        "views/room_management/room_types/accommodation_offer_view.xml",
        "views/room_management/room_types/accommodation_photo_view.xml",
        "views/room_management/room_types/room_types_view.xml",
        "views/room_management/room_types/smoking_in_room_views.xml",
        "views/room_management/room_types/amenities/video_and_audio_views.xml",
        "views/room_management/room_types/amenities/electronic_devices_views.xml",
        "views/room_management/room_types/amenities/bathroom_views.xml",
        "views/room_management/room_types/amenities/outdoor_area_and_window_view_views.xml",
        "views/room_management/room_types/amenities/internet_and_telephony_views.xml",
        "views/room_management/room_types/amenities/beds_views.xml",
        "views/room_management/room_types/amenities/furniture_views.xml",
        "views/room_management/room_types/amenities/others_views.xml",
        # Room Management > Rate Plan
        "views/room_management/rate_plan/rate_plan_views.xml",
        "views/room_management/rate_plan/rate_plan_type.xml",
        "views/room_management/rate_plan/rate_plan_currency.xml",
        # Room Management > Rate Plan > Calendar Data
        "views/room_management/rate_plan/calendar_data/closed_views.xml",
        "views/room_management/rate_plan/calendar_data/min_los_views.xml",
        "views/room_management/rate_plan/calendar_data/max_los_views.xml",
        "views/room_management/rate_plan/calendar_data/min_los_arrival_views.xml",
        "views/room_management/rate_plan/calendar_data/max_los_arrival_views.xml",
        "views/room_management/rate_plan/calendar_data/full_parent_los_views.xml",
        "views/room_management/rate_plan/calendar_data/min_adv_booking_views.xml",
        "views/room_management/rate_plan/calendar_data/max_adv_booking_views.xml",
        "views/room_management/rate_plan/calendar_data/cta_views.xml",
        "views/room_management/rate_plan/calendar_data/ctd_views.xml",
        "views/room_management/rate_plan/calendar_data/stay_controls_views.xml",
        "views/room_management/rate_plan/calendar_data/check_in_check_out_views.xml",
        "views/room_management/rate_plan/calendar_data/payment_methods_views.xml",
        "views/room_management/rate_plan/calendar_data/price_views.xml",
        "views/room_management/rate_plan/calendar_data/day_selection_views.xml",
        # "views/room_management/rate_plan/rate_payment_method.xml",
        "views/room_management/rate_plan/rate_plan_pos.xml",
        "views/room_management/rate_plan/cancellation_rule.xml",
        "views/room_management/rate_plan/check_in_check_out.xml",
        "views/room_management/rate_plan/rounding_policy.xml",
        "views/room_management/rate_plan/extras_views.xml",
        # "views/room_management/rate_plan/calendar_data_views.xml",
        "views/room_management/promotion/promotion.xml",
        # "views/room_management/room_types/guest_views.xml",
        # Room Management > Availability
        "views/room_management/availability/availability_view.xml",
        "views/room_management/availability/default_availability.xml",
        "views/room_management/availability/availability_room_type_views.xml",
        "views/room_management/availability/availability_online_sales_role.xml",
        "views/room_management/availability/availability_settings_views.xml",
        # Property Setting
        # ^^ > View
        "views/property_settings/main_settings/main_settings.xml",
        "views/property_settings/payment_methods/payment_method.xml",
        "views/property_settings/main_settings/base_type.xml",
        "views/property_settings/main_settings/state_view.xml",
        "views/property_settings/main_settings/city_view.xml",
        "views/property_settings/main_settings/child_age_range.xml",
        # 'views/dynamic_phone_field_views.xml',
        # "views/property_settings/views.xml",
        "views/property_settings/templates.xml",
        "views/property_settings/comments/comments.xml",
        "views/property_settings/services_setting/services_settings.xml",
        "views/property_settings/services_setting/services_group.xml",
        "views/property_settings/services_setting/services_types.xml",
        "views/property_settings/services_setting/motivator_booking_engine.xml",
        "views/property_settings/services_setting/service_photo_views.xml",
        # Property Setting > Check In Check Out
        "views/property_settings/check_in_check_out/all_time.xml",
        "views/property_settings/check_in_check_out/check_in_check_out_roles.xml",
        "views/property_settings/check_in_check_out/check_in_check_out_time.xml",
        # "views/property_settings/check_in_check_out/surcharge_for_late_check_out.xml",
        "views/property_settings/check_in_check_out/menu_items.xml",
        # Property Setting > Cancellation Terms
        "views/property_settings/cancellation/role.xml",
        "views/property_settings/cancellation/cancellation_terms.xml",
        "views/property_settings/cancellation/menu_items.xml",
        # Property Setting > Transfers
        "views/property_settings/transfers/transfer_type_views.xml",
        "views/property_settings/transfers/vehicles_views.xml",
        "views/property_settings/transfers/transport_companies_views.xml",
        "views/property_settings/transfers/station_views.xml",
        "views/property_settings/transfers/transfers_views.xml",
        "views/property_settings/transfers/menu_items.xml",
        # Property Setting > Rounding rule
        "views/property_settings/rounding_rule/rounding_rule_tree_view.xml",
        "views/property_settings/promo_codes/promo_code_valid_date_views.xml",
        "views/property_settings/promo_codes/promo_code_groups_views.xml",
        "views/property_settings/promo_codes/promo_codes_views.xml",
        "views/property_settings/promo_codes/promo_code_generate_wizard_views.xml",
        # Property Setting > Promotion
        # "views/property_settings/promotion/promotion.xml",
        "views/actions.xml",
        "views/manuitems.xml",
        # Property Management
        "views/property_management/room_inventory_views.xml",
        "views/property_management/housekeeping_views.xml",
        "views/property_management/property_building_views.xml",
        "views/property_management/companies/country_views.xml",
        "views/property_management/guest/guest_views.xml",
        "views/property_management/companies/addition_account_number.xml",
        "views/property_management/companies/responsible_person.xml",
        "views/property_management/guest/legal_representative.xml",
        "views/property_management/guest/email_contact.xml",
        "views/property_management/guest/phone_contact.xml",
        "views/property_management/front_desk/booking.xml",
        "views/property_management/front_desk/booking_accommodation.xml",
        "views/property_management/front_desk/booking_price_detail.xml",
        "views/property_management/front_desk/group_booking.xml",
        "views/property_management/front_desk/group_booking_accommodation.xml",
        "views/property_management/settings_view.xml",
        "views/property_management/references.xml",
        "views/property_management/reception/reception_invoice.xml",
        "reports/reception/report_invoice_template.xml",
        "reports/reception/report_action.xml",
        "reports/reception/report_document.xml",
        # Advisor
        "views/advisor/booking_stats/sales_and_occupancy_views.xml",
        "views/advisor/booking_stats/occupancy_rate.xml",
        "views/advisor/booking_stats/booking_cancellations.xml",
        "views/advisor/booking_stats/booking_window.xml",
        # Accounting
        # "views/accounting/accounting.xml",
        "views/accounting/accounting_calendar.xml",
        "views/accounting/booking_reconciliation_views.xml",
        # "data/accounting.xml",
        "reports/report.xml",
        "reports/report_guest.xml",
        "views/property_management/notes_and_instructions.xml",
        # RECEPTION
        # "views/property_management/reception/arrivals.xml",
        # "views/property_management/reception/occupied.xml",
        # "views/property_management/reception/reception.xml",
        "views/property_management/reception/reception_views.xml",
        "views/property_management/reception/notes.xml",
        "views/property_management/reception/reception_checkin.xml",
        "views/automated_emails/mail_list/welcome_mail.xml",
        "views/automated_emails/mail_list/feedback_mail.xml",
        "views/automated_emails/mail_list/incomplete_booking_for_guest.xml",
        "views/automated_emails/mail_list/incomplete_booking_mail.xml",
        "views/automated_emails/mail_list/send_test_email_form.xml",
        "views/automated_emails/mail_list/mail_list.xml",
        "views/automated_emails/mail_list_temp/temp_mail_list.xml",
        "views/reports/booking_views.xml",
        "views/property_management/front_desk/move_room.xml",
        "views/property_management/reception/reception_payment.xml",
        # "views/property_settings/check_in_check_out/checkin_checkout_settings.xml",
        "views/property_settings/check_in_check_out/checkin_checkout_settings.xml",
        "views/property_management/payments/group_booking_payment.xml",
        "views/property_management/reception/deposit/deposit_views.xml",
        "views/property_management/front_desk/cancellation_frontdesk.xml",
        "views/property_management/companies/company_views.xml",
    ],
    "qweb": [
        "views/qweb/scheduler_template.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css",
            "hms_app/static/src/**/*",
            "hms_app/static/description/*",
        ],
    },
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}
