from langtools import _

import json
import collections
from kivy.logger import Logger
from ui.peachy_settings import SettingString, SettingNumeric, SettingBoolean

try:
    from VERSION import version, revision
except:
    version = "DEV"
    revision = "DEV"


class SettingsMapper(object):
    email_regex = """[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$"""
    def __init__(self, api):
        self.api = api
        self.configuration_api = self.api.get_configuration_api()

    @property
    def config_info(self):
        return [
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc': _('info_version_number DESCRIPTION'),
                    'title': _('info_version_number TITLE'),
                    'key': 'info_version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc': _('info_serial_number DESCRIPTION'),
                    'title': _('info_serial_number TITLE'),
                    'key': 'info_serial_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc': _('info_hardware_version_number DESCRIPTION'),
                    'title': _('info_hardware_version_number TITLE'),
                    'key': 'info_hardware_version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc': _('info_firmware_version_number DESCRIPTION'),
                    'title': _('info_firmware_version_number TITLE'),
                    'key': 'info_firmware_version_number',
                    'disabled': True
                },
# ----------- BEGIN Options --------------------
                {
                    'type': 'bool',
                    'section': _('Options'),
                    'key': 'options_use_sublayers',
                    'title': _('options_use_sublayers TITLE'),
                    'desc': _('options_use_sublayers DESCRIPTION'),
                    'values': [False, True]
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_sublayer_height_mm',
                    'title': _('options_sublayer_height_mm TITLE'),
                    'desc': _('options_sublayer_height_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'bool',
                    'section': _('Options'),
                    'key': 'options_use_shufflelayers',
                    'title': _('options_use_shufflelayers TITLE'),
                    'desc': _('options_use_shufflelayers DESCRIPTION'),
                    'values': [False, True],
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_shuffle_layers_amount',
                    'title': _('options_shuffle_layers_amount TITLE'),
                    'desc': _('options_shuffle_layers_amount DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'bool',
                    'values': [False, True],
                    'section': _('Options'),
                    'key': 'options_use_overlap',
                    'title': _('options_use_overlap TITLE'),
                    'desc': _('options_use_overlap DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_overlap_amount_mm',
                    'title': _('options_overlap_amount_mm TITLE'),
                    'desc': _('options_overlap_amount_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_laser_thickness_mm',
                    'title': _('options_laser_thickness_mm TITLE'),
                    'desc': _('options_laser_thickness_mm DESCRIPTION'),
                    'value_range': [0, None]
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_scaling_factor',
                    'title': _('options_scaling_factor TITLE'),
                    'desc': _('options_scaling_factor DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },

                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_max_lead_distance_mm',
                    'title': _('options_max_lead_distance_mm TITLE'),
                    'desc': _('options_max_lead_distance_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_pre_layer_delay',
                    'title': _('options_pre_layer_delay TITLE'),
                    'desc': _('options_pre_layer_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_post_fire_delay',
                    'title': _('options_post_fire_delay TITLE'),
                    'desc': _('options_post_fire_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_slew_delay',
                    'title': _('options_slew_delay TITLE'),
                    'desc': _('options_slew_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_wait_after_move_milliseconds',
                    'title': _('options_wait_after_move_milliseconds TITLE'),
                    'desc': _('options_wait_after_move_milliseconds DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_print_queue_delay',
                    'title': _('options_print_queue_delay TITLE'),
                    'desc': _('options_print_queue_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
# ----------- BEGIN EMAIL --------------------
                {
                    'type': 'bool',
                    'section': _('Email'),
                    'key': 'email_on',
                    'title': _('email.on TITLE'),
                    'desc': _('email.on DESCRIPTION'),
                    'values': [False, True]
                },
                {
                    'type': 'numeric',
                    'section': _('Email'),
                    'key': 'email_port',
                    'title': _('email.port TITLE'),
                    'desc': _('email.port DESCRIPTION'),
                    'value_range': [0, 49152],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_host',
                    'title': _('email.host TITLE'),
                    'desc': _('email.host DESCRIPTION'),
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_sender',
                    'title': _('email.sender TITLE'),
                    'desc': _('email.sender DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': self.email_regex
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_recipient',
                    'title': _('email.recipient TITLE'),
                    'desc': _('email.recipient DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': self.email_regex
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_username',
                    'title': _('email.username TITLE'),
                    'desc': _('email.username DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_password',
                    'title': _('email.password TITLE'),
                    'desc': _('email.password DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
# ----------- BEGIN Serial --------------------
                {
                    'type': 'bool',
                    'section': _('Serial'),
                    'key': 'serial_enabled',
                    'title': _('serial_enabled TITLE'),
                    'desc': _('serial_enabled DESCRIPTION'),
                    'values': [False, True]
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_port',
                    'title': _('serial_port TITLE'),
                    'desc': _('serial_port DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_on_command',
                    'title': _('serial_on_command TITLE'),
                    'desc': _('serial_on_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_off_command',
                    'title': _('serial_off_command TITLE'),
                    'desc': _('serial_off_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_layer_started_command',
                    'title': _('serial_layer_started_command TITLE'),
                    'desc': _('serial_layer_started_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_layer_ended_command',
                    'title': _('serial_layer_ended_command TITLE'),
                    'desc': _('serial_layer_ended_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_print_ended_command',
                    'title': _('serial_print_ended_command TITLE'),
                    'desc': _('serial_print_ended_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
# ----------- BEGIN Cure Rate --------------------
                {
                    'type': 'bool',
                    'key': 'cure_rate_use_draw_speed',
                    'section': _('Cure Rate'),
                    'title': _('cure_rate_use_draw_speed TITLE'),
                    'desc': _('cure_rate_use_draw_speed DESCRIPTION'),
                    'values': [False, True]
                },
                {
                    'type': 'numeric',
                    'key': 'cure_rate_draw_speed',
                    'section': _('Cure Rate'),
                    'title': _('cure_rate_draw_speed TITLE'),
                    'desc': _('cure_rate_draw_speed DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [1, None],
                },
                {
                    'type': 'bool',
                    'key': 'cure_rate_override_laser_power',
                    'section': _('Cure Rate'),
                    'title': _('cure_rate_override_laser_power TITLE'),
                    'desc': _('cure_rate_override_laser_power DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'values': [False, True],
                },
                {
                    'type': 'numeric',
                    'key': 'cure_rate_override_laser_power_amount',
                    'section': _('Cure Rate'),
                    'title': _('cure_rate_override_laser_power_amount TITLE'),
                    'desc': _('cure_rate_override_laser_power_amount DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0, 1],
                },
# ----------- BEGIN Dripper --------------------
                {
                    'type': 'options',
                    'key': 'dripper_type',
                    'section': _('Dripper'),
                    'title': _('dripper_type TITLE'),
                    'desc': _('dripper_type DESCRIPTION'),
                    'options': [_('Emulated'), _('Photo'), _('Circut')],
                    'options_id': ['emulated', 'photo', 'microcontroller']
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_drips_per_mm',
                    'section': _('Dripper'),
                    'title': _('dripper_drips_per_mm TITLE'),
                    'desc': _('dripper_drips_per_mm DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [1, None],
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_emulated_drips_per_second',
                    'section': _('Dripper'),
                    'title': _('dripper_emulated_drips_per_second TITLE'),
                    'desc': _('dripper_emulated_drips_per_second DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0, None],
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_photo_zaxis_delay',
                    'section': _('Dripper'),
                    'title': _('dripper_photo_zaxis_delay TITLE'),
                    'desc': _('dripper_photo_zaxis_delay DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0, 1],
                },
                ]

    def refresh_settings(self, settings, config):
        self.load_config(config)
        settings.register_type('string', SettingString)
        settings.register_type('bool', SettingBoolean)
        settings.register_type('numeric', SettingNumeric)

        sections = set([item['section'] for item in self.config_info])
        for section in sections:
            Logger.info("SECTION ADDED: %s" % section)
            data = [cfg for cfg in self.config_info if cfg['section'] == section]
            settings.add_json_panel(section, config, data=json.dumps(data))

    def set_defaults(self, config):
        Logger.info("Setting Defaults")

    def _convert(self, item, value):
        entry_type = item['type']
        if entry_type == 'string':
            return str(value)
        if entry_type == 'numeric':
            if '.' in str(value):
                return float(value)
            else:
                return int(value)
        if entry_type == 'bool':
            if value == 'True':
                return True
            else:
                return False
        if entry_type == 'options':
            return item['options_id'][item['options'].index(value)]

    def update_setting(self, section, key, value):
        Logger.info(u"Setting changed  %s, %s -> %s" % (section, key, value))
        item = [item for item in self.config_info if item['key'] == key][0]
        if hasattr(self.configuration_api, 'set_' + key):
            getattr(self.configuration_api, 'set_' + key)(self._convert(item, value))
        self.configuration_api.save()

    def load_config(self, config):
        Logger.info("Loading Configs")
        printers = self.configuration_api.get_available_printers()
        if not printers:
            self.configuration_api.add_printer("Peachy Printer")
        self.configuration_api.load_printer(self.configuration_api.get_available_printers()[0])

        for item in self.config_info:
            key = item['key']
            section = item['section']
            getter = 'get_' + key
            value = getattr(self.configuration_api, getter)()
            if item['type'] == 'options':
                value = item['options'][item['options_id'].index(value)]
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, key, value)

    def get_settings(self):
        setting_values = collections.OrderedDict()
        for setting in sorted(self.config_info, key=lambda t: t['key']):
            setting_values[setting['title']] = str(getattr(self.configuration_api, 'get_' + setting['key'])())
        return setting_values
