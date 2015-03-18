from langtools import _
import json

class SettingsMapper(object):
    def __init__(self,):
        pass

    @property
    def config_info(self):
        return [
                {
                    'type': 'string',
                    'section': u'Info',
                    'desc': _('info.version_number DESCRIPTION'),
                    'title': _('info.version_number TITLE'),
                    'key': 'info.version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': u'Info',
                    'desc': _('info.serial_number DESCRIPTION'),
                    'title': _('info.serial_number TITLE'),
                    'key': 'info.serial_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': u'Info',
                    'desc': _('info.hardware_version_number DESCRIPTION'),
                    'title': _('info.hardware_version_number TITLE'),
                    'key': 'info.hardware_version_number',
                    'disabled': True
                },
                {
                    'type': 'string',
                    'section': u'Info',
                    'desc': _('info.firmwware_version_number DESCRIPTION'),
                    'title': _('info.firmwware_version_number TITLE'),
                    'key': 'info.firmwware_version_number',
                    'disabled': True
                },
               ]

    @property
    def options(self):
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

    def set_defaults(self, config):
        info_items = dict([(item['key'], "Not Specified") for item in self.config_info])
        config.setdefaults(u'Info', info_items)
