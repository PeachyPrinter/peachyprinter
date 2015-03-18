from langtools import _

import json
from kivy.logger import Logger

class SettingsMapper(object):
    def __init__(self, api):
        self.api = api

    @property
    def config_info(self):
        return [
                {
                    'type': 'string',
                    'section': 'Info',
                    'desc': _('info.version_number DESCRIPTION'),
                    'title': _('info.version_number TITLE'),
                    'key': 'info.version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': 'Info',
                    'desc': _('info.serial_number DESCRIPTION'),
                    'title': _('info.serial_number TITLE'),
                    'key': 'info.serial_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': 'Info',
                    'desc': _('info.hardware_version_number DESCRIPTION'),
                    'title': _('info.hardware_version_number TITLE'),
                    'key': 'info.hardware_version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': 'Info',
                    'desc': _('info.firmwware_version_number DESCRIPTION'),
                    'title': _('info.firmwware_version_number TITLE'),
                    'key': 'info.firmwware_version_number',
                    'disabled': True
                },
               ]

    @property
    def config_options(self):
        return [
                {
                    'type': 'bool',
                    'section': 'Options',
                    'key': 'options.use_sublayers',
                    'title': _('options.use_sublayers TITLE'),
                    'desc': _('options.use_sublayers DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.sublayer_height_mm',
                    'title': _('options.sublayer_height_mm TITLE'),
                    'desc': _('options.sublayer_height_mm DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.laser_thickness_mm',
                    'title': _('options.laser_thickness_mm TITLE'),
                    'desc': _('options.laser_thickness_mm DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.scaling_factor',
                    'title': _('options.scaling_factor TITLE'),
                    'desc': _('options.scaling_factor DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.overlap_amount',
                    'title': _('options.overlap_amount TITLE'),
                    'desc': _('options.overlap_amount DESCRIPTION'),
                },
                {
                    'type': 'bool',
                    'section': 'Options',
                    'key': 'options.use_shufflelayers',
                    'title': _('options.use_shufflelayers TITLE'),
                    'desc': _('options.use_shufflelayers DESCRIPTION'),
                },
                {
                    'type': 'bool',
                    'section': 'Options',
                    'key': 'options.use_overlap',
                    'title': _('options.use_overlap TITLE'),
                    'desc': _('options.use_overlap DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.print_queue_delay',
                    'title': _('options.print_queue_delay TITLE'),
                    'desc': _('options.print_queue_delay DESCRIPTION'),
                },
                {
                    'type': 'numeric',
                    'section': 'Options',
                    'key': 'options.pre_layer_delay',
                    'title': _('options.pre_layer_delay TITLE'),
                    'desc': _('options.pre_layer_delay DESCRIPTION'),
                },]

    def refresh_settings(self, settings, config):
        settings.add_json_panel(_('Info'), config, data=json.dumps(self.config_info))
        settings.add_json_panel(_('Options'), config, data=json.dumps(self.config_options))

    def set_defaults(self, config):
        self.load_config(config)

    def update_setting(self, section, key, value):
        Logger.info(u"Setting changed  %s, %s -> %s" % (section, key, value))

    def load_config(self, config):
        configuration_api = self.api.get_configuration_api()
        configuration_api.load_printer(configuration_api.get_available_printers()[0])
        info_items = {
            'info.version_number': 'Not Yet Determined',
            'info.serial_number': 'Not Yet Determined',
            'info.hardware_version_number': 'Not Yet Determined',
            'info.firmwware_version_number': 'Not Yet Determined',
            }

        config_items = {
            'options.use_sublayers': configuration_api.get_use_sublayers(),
            'options.sublayer_height_mm': configuration_api.get_sublayer_height_mm(),
            'options.laser_thickness_mm': configuration_api.get_laser_thickness_mm(),
            'options.scaling_factor': configuration_api.get_scaling_factor(),
            'options.overlap_amount': configuration_api.get_overlap_amount_mm(),
            'options.use_shufflelayers': configuration_api.get_use_shufflelayers(),
            'options.use_overlap': configuration_api.get_use_overlap(),
            'options.print_queue_delay': configuration_api.get_print_queue_delay(),
            'options.pre_layer_delay': configuration_api.get_pre_layer_delay(),
        }

        config.setdefaults('Info', info_items)
        config.setdefaults('Options', config_items)
