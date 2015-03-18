from langtools import _
import json

class SettingsMapper(object):
    def __init__(self,):
        
        self.config_info = [
            {
                'type': 'string',
                'section': 'Info',
                'desc': _('Peachy Printers Software Version'),
                'title': _('Version'),
                'key': 'version_number',
                'disabled': True
            },
            {
                'type': 'string',
                'section': 'Info',
                'desc': _('Your Peachy Printers Hardware Serial Number'),
                'title': _('Serial Number'),
                'key': 'serial_number',
                'disabled': True
            },
            {
                'type': 'string',
                'section': 'Info',
                'desc': _('Your Peachy Printers Hardware Version'),
                'title': _('Hardware Number'),
                'key': 'hardware_version_number',
                'disabled': True
            },
            {
                'type': 'string',
                'section': 'Info',
                'desc': _('Your Peachy Printers Firmware Version'),
                'title': _('Firmware Number'),
                'key': 'firmwware_version_number',
                'disabled': True
            },
            ]
        self.options = [
            {
                'type': 'bool',
                'section': 'Options',
                'key': 'options.use_sublayers',
                'title': _('Use Sublayers'),
                'desc': _('Augment the gcode model with sublayers for use with large layers [Off]'),
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.sublayer_height_mm',
                'title': _('Sublayer Height (mm)'),
                'desc': _('Height of a sublayer in mm [0.1]'),
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.laser_thickness_mm',
                'title': _('Laser Thickness (mm)'),
                'desc': _('The thickness of the laser where it intersects the resin [0.5]'),
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.scaling_factor',
                'title': '',
                'desc': '',
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.overlap_amount',
                'title': '',
                'desc': '',
            },
            {
                'type': 'bool',
                'section': 'Options',
                'key': 'options.use_shufflelayers',
                'title': '',
                'desc': '',
            },
            {
                'type': 'bool',
                'section': 'Options',
                'key': 'options.use_overlap',
                'title': '',
                'desc': '',
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.print_queue_delay',
                'title': '',
                'desc': '',
            },
            {
                'type': 'numeric',
                'section': 'Options',
                'key': 'options.pre_layer_delay',
                'title': '',
                'desc': '',
            },
        ]

    def refresh_settings(self, settings, config):
        settings.add_json_panel("Info", config, data=json.dumps(self.config_info))

    def set_defaults(self, config):
        info_items = dict([(item['key'], "Not Specified") for item in self.config_info])
        config.setdefaults("Info", info_items)
