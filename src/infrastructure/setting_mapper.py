from langtools import _

import json
import collections
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.settings import SettingBoolean 
from ui.peachy_settings import SettingString, SettingNumeric

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
                # {
                #     'type': 'string',
                #     'section': _('Info'),
                #     'desc_source': _('info_version_number DESCRIPTION'),
                #     'title_source': _('info_version_number TITLE'),
                #     'key': 'info_version_number',
                #     'disabled': True
                # },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc_source': _('info_serial_number DESCRIPTION'),
                    'title_source': _('info_serial_number TITLE'),
                    'key': 'info_serial_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc_source': _('info_hardware_version_number DESCRIPTION'),
                    'title_source': _('info_hardware_version_number TITLE'),
                    'key': 'info_hardware_version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': _('Info'),
                    'desc_source': _('info_firmware_version_number DESCRIPTION'),
                    'title_source': _('info_firmware_version_number TITLE'),
                    'key': 'info_firmware_version_number',
                    'disabled': True
                },
                {
                    'type': 'numeric',
                    'section': _('Info'),
                    'desc_source': _('info_firmware_data_rate DESCRIPTION'),
                    'title_source': _('info_firmware_data_rate TITLE'),
                    'key': 'info_firmware_data_rate',
                    'disabled': True
                },
# ----------- BEGIN Options --------------------
                {
                    'type': 'bool',
                    'section': _('Options'),
                    'key': 'options_use_sublayers',
                    'title_source': _('options_use_sublayers TITLE'),
                    'desc_source': _('options_use_sublayers DESCRIPTION'),                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_sublayer_height_mm',
                    'title_source': _('options_sublayer_height_mm TITLE'),
                    'desc_source': _('options_sublayer_height_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'bool',
                    'section': _('Options'),
                    'key': 'options_use_shufflelayers',
                    'title_source': _('options_use_shufflelayers TITLE'),
                    'desc_source': _('options_use_shufflelayers DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_shuffle_layers_amount',
                    'title_source': _('options_shuffle_layers_amount TITLE'),
                    'desc_source': _('options_shuffle_layers_amount DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'bool',
                    'section': _('Options'),
                    'key': 'options_use_overlap',
                    'title_source': _('options_use_overlap TITLE'),
                    'desc_source': _('options_use_overlap DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_overlap_amount_mm',
                    'title_source': _('options_overlap_amount_mm TITLE'),
                    'desc_source': _('options_overlap_amount_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_laser_thickness_mm',
                    'title_source': _('options_laser_thickness_mm TITLE'),
                    'desc_source': _('options_laser_thickness_mm DESCRIPTION'),
                    'value_range': [0, None]
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_scaling_factor',
                    'title_source': _('options_scaling_factor TITLE'),
                    'desc_source': _('options_scaling_factor DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },

                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_max_lead_distance_mm',
                    'title_source': _('options_max_lead_distance_mm TITLE'),
                    'desc_source': _('options_max_lead_distance_mm DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_pre_layer_delay',
                    'title_source': _('options_pre_layer_delay TITLE'),
                    'desc_source': _('options_pre_layer_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_post_fire_delay',
                    'title_source': _('options_post_fire_delay TITLE'),
                    'desc_source': _('options_post_fire_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_slew_delay',
                    'title_source': _('options_slew_delay TITLE'),
                    'desc_source': _('options_slew_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_wait_after_move_milliseconds',
                    'title_source': _('options_wait_after_move_milliseconds TITLE'),
                    'desc_source': _('options_wait_after_move_milliseconds DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'numeric',
                    'section': _('Options'),
                    'key': 'options_print_queue_delay',
                    'title_source': _('options_print_queue_delay TITLE'),
                    'desc_source': _('options_print_queue_delay DESCRIPTION'),
                    'value_range': [0, None],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
# ----------- BEGIN EMAIL --------------------
                {
                    'type': 'bool',
                    'section': _('Email'),
                    'key': 'email_on',
                    'title_source': _('email.on TITLE'),
                    'desc_source': _('email.on DESCRIPTION'),
                    'true': 'auto' 
                },
                {
                    'type': 'numeric',
                    'section': _('Email'),
                    'key': 'email_port',
                    'title_source': _('email.port TITLE'),
                    'desc_source': _('email.port DESCRIPTION'),
                    'value_range': [0, 49152],
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_host',
                    'title_source': _('email.host TITLE'),
                    'desc_source': _('email.host DESCRIPTION'),
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_sender',
                    'title_source': _('email.sender TITLE'),
                    'desc_source': _('email.sender DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': self.email_regex
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_recipient',
                    'title_source': _('email.recipient TITLE'),
                    'desc_source': _('email.recipient DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': self.email_regex
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_username',
                    'title_source': _('email.username TITLE'),
                    'desc_source': _('email.username DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Email'),
                    'key': 'email_password',
                    'title_source': _('email.password TITLE'),
                    'desc_source': _('email.password DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
# ----------- BEGIN Serial --------------------
                {
                    'type': 'bool',
                    'section': _('Serial'),
                    'key': 'serial_enabled',
                    'title_source': _('serial_enabled TITLE'),
                    'desc_source': _('serial_enabled DESCRIPTION'),                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_port',
                    'title_source': _('serial_port TITLE'),
                    'desc_source': _('serial_port DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel")
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_on_command',
                    'title_source': _('serial_on_command TITLE'),
                    'desc_source': _('serial_on_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_off_command',
                    'title_source': _('serial_off_command TITLE'),
                    'desc_source': _('serial_off_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_layer_started_command',
                    'title_source': _('serial_layer_started_command TITLE'),
                    'desc_source': _('serial_layer_started_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_layer_ended_command',
                    'title_source': _('serial_layer_ended_command TITLE'),
                    'desc_source': _('serial_layer_ended_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
                {
                    'type': 'string',
                    'section': _('Serial'),
                    'key': 'serial_print_ended_command',
                    'title_source': _('serial_print_ended_command TITLE'),
                    'desc_source': _('serial_print_ended_command DESCRIPTION'),
                    'ok_button_text': _("Ok"),
                    'cancel_button_text': _("Cancel"),
                    'validation_regex': ".$"
                },
# ----------- BEGIN Cure Rate --------------------
                {
                    'type': 'bool',
                    'key': 'cure_rate_use_draw_speed',
                    'section': _('Cure Rate'),
                    'title_source': _('cure_rate_use_draw_speed TITLE'),
                    'desc_source': _('cure_rate_use_draw_speed DESCRIPTION'),                },
                {
                    'type': 'numeric',
                    'key': 'cure_rate_draw_speed',
                    'section': _('Cure Rate'),
                    'title_source': _('cure_rate_draw_speed TITLE'),
                    'desc_source': _('cure_rate_draw_speed DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [1, None],
                },
                {
                    'type': 'numeric',
                    'key': 'cure_rate_move_speed',
                    'section': _('Cure Rate'),
                    'title_source': _('cure_rate_move_speed TITLE'),
                    'desc_source': _('cure_rate_move_speed DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [1, None],
                },
                {
                    'type': 'bool',
                    'key': 'cure_rate_override_laser_power',
                    'section': _('Cure Rate'),
                    'title_source': _('cure_rate_override_laser_power TITLE'),
                    'desc_source': _('cure_rate_override_laser_power DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                },
                {
                    'type': 'numeric',
                    'key': 'cure_rate_override_laser_power_amount',
                    'section': _('Cure Rate'),
                    'title_source': _('cure_rate_override_laser_power_amount TITLE'),
                    'desc_source': _('cure_rate_override_laser_power_amount DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0, 1.0],
                },
# ----------- BEGIN Dripper --------------------
                {
                    'type': 'options',
                    'key': 'dripper_type',
                    'section': _('Dripper'),
                    'title_source': _('dripper_type TITLE'),
                    'desc_source': _('dripper_type DESCRIPTION'),
                    'options': [_('Emulated'), _('Photo'), _('Circut')],
                    'options_id': ['emulated', 'photo', 'microcontroller']
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_drips_per_mm',
                    'section': _('Dripper'),
                    'title_source': _('dripper_drips_per_mm TITLE'),
                    'desc_source': _('dripper_drips_per_mm DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [1, None],
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_emulated_drips_per_second',
                    'section': _('Dripper'),
                    'title_source': _('dripper_emulated_drips_per_second TITLE'),
                    'desc_source': _('dripper_emulated_drips_per_second DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0.0, 20.0],
                },
                {
                    'type': 'numeric',
                    'key': 'dripper_photo_zaxis_delay',
                    'section': _('Dripper'),
                    'title_source': _('dripper_photo_zaxis_delay TITLE'),
                    'desc_source': _('dripper_photo_zaxis_delay DESCRIPTION'),
                    'ok_button_text': _('Ok'),
                    'cancel_button_text': _('Cancel'),
                    'value_range': [0, None],
                },
                ]

    def refresh_settings(self, settings, config):
        self.load_config(config)
        settings.register_type('string', SettingString)
        # settings.register_type('bool', SettingBoolean)
        settings.register_type('numeric', SettingNumeric)

        sections = set([item['section'] for item in self.config_info])
        for section in sections:
            Logger.info("SECTION ADDED: %s" % section)
            section_data = [cfg for cfg in self.config_info if cfg['section'] == section]
            translated_section_name = App.get_running_app().translation(section)
            for cfg in section_data:
                cfg['section'] = App.get_running_app().translation(section)
                cfg['title'] = App.get_running_app().translation(cfg['title_source'])
                cfg['desc'] = App.get_running_app().translation(cfg['desc_source'])
            settings.add_json_panel(translated_section_name, config, data=json.dumps(section_data))

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
            if value == '1' or value == True:
                return True
            else:
                return False
        if entry_type == 'options':
            return item['options_id'][item['options'].index(value)]

    def update_setting(self, section, key, value):
        Logger.info(u"Setting changed  %s, %s -> %s" % (section, key, value))
        item = [item for item in self.config_info if item['key'] == key][0]
        try:
            if hasattr(self.configuration_api, 'set_' + key):
                getattr(self.configuration_api, 'set_' + key)(self._convert(item, value))
            self.configuration_api.save()
        except Exception as ex:
            Logger.info("Save to %s,%s of %s resulted in an error %s, changes not saved" % (section, key, value, ex))

    def load_config(self, config):
        Logger.info("Loading Configs")
        self.configuration_api.load_printer()

        for item in self.config_info:
            key = item['key']
            section = item['section']
            translated_section_name = App.get_running_app().translation(section)
            getter = 'get_' + key
            value = getattr(self.configuration_api, getter)()
            if item['type'] == 'options':
                value = item['options'][item['options_id'].index(value)]
            if item['type'] == 'bool':
                value = '1' if value else '0'
            if not config.has_section(translated_section_name):
                config.add_section(translated_section_name)
            config.set(translated_section_name, key, value)

    def get_settings(self):
        Logger.info("getting Settings")
        setting_values = collections.OrderedDict()
        for setting in sorted(self.config_info, key=lambda t: t['key']):
            setting_values[setting['title_source']] = str(getattr(self.configuration_api, 'get_' + setting['key'])())
        return setting_values
