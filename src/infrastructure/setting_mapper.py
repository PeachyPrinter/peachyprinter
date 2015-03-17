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

    def refresh_settings(self, settings, config):
        settings.add_json_panel("Info", config, data=json.dumps(self.config_info))

    def set_defaults(self, config):
        info_items = dict([(item['key'], "Not Specified") for item in self.config_info])
        config.setdefaults("Info", info_items)
