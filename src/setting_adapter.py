import json


class SettingsAdapter(object):
    def __init__(self):
        self.def_dict = {
            "Main": {
               'name': "Peachy Printer",
            },
            "Audio": {
               'output.bit_depth': "16 bit",
               'output.sample_rate': 48000,
               'output.modulation_on_frequency': 8000,
               'output.modulation_off_frequency': 2000,
               'input.bit_depth': "16 bit",
               'input.sample_rate': 44100,
            },
            "Options": {
               'sublayer_height_mm': 0.01,
               'laser_thickness_mm': 0.5,
               'laser_offset': 7,
               'scaling_factor': 1.0,
               'overlap_amount': 1.0,
               'use_shufflelayers': True,
               'use_sublayers': False,
               'use_overlap': True,
               'print_queue_delay': 0.0,
               'pre_layer_delay': 0.0,
            },
            "Dripper": {
               'drips_per_mm': 100.0,
               'max_lead_distance_mm': 1.0,
               'dripper_type': 'audio',
               'emulated_drips_per_second': 1.0,
               'photo_zaxis_delay': 3.0,
            },
            "Calibration": {
               'max_deflection': 0.95,
               'height': 40.0,
               'lower_points': 7,
               'upper_points': 7,
            },
            "Serial": {
               'on': False,
               'port': "COM2",
               'on_command': "7",
               'off_command': "8",
               'layer_started': "S",
               'layer_ended': "E",
               'print_ended': "Z",
            },
            "Email": {
               'on': False,
               'port': 25,
               'host': "some.smtp.server",
               'sender': "senderemail@email.com",
               'recipient': "recipientemail@email.com",
            },
            "Cure Rate": {
               'base_height': 3.0,
               'total_height': 23.0,
               'start_speed': 50.0,
               'finish_speed': 200.0,
               'draw_speed': 100.0,
               'use_draw_speed': True,
            },
            "Micro Controller": {
               'port': '/dev/ttyACM0',
               'rate': 8000,
               'header': '@',
               'footer': 'A',
               'escape': 'B',
            },
            "Circut": {
               'circut_type': 'Analog',
               'version': 'r1.99-r3',
            },
            }
    def getSettings(self):
        return self.jsonSettings()

    def saveSettings(self, settings):
        pass

    def defaults(self):
        return self.def_dict

    def jsonSettings(self):
        return [
    {
        'type': 'string',
        'section': 'Main',
        'desc': 'BETTER DESCRIPTION HERE: string',
        'title': 'Name',
        'key': 'name',
    },
    {
        'type': 'options',
        'options': [
           '16 Bit',
           '24 Bit'
      ],
        'title': 'Bit Depth',
        'desc': 'BETTER DESCRIPTION HERE: Bit Depth',
        'section': 'Audio',
        'key': 'output.bit_depth',
    },
    {
        'type': 'options',
        'options': [
           '48,000Khz',
           '44,100Khz'
      ],
        'title': 'Output Sample Rate',
        'desc': 'BETTER DESCRIPTION HERE: Output Sample Rate',
        'section': 'Audio',
        'key': 'output.sample_rate',
    },
    {
        'type': 'numeric',
        'title': 'Modulation On Frequency',
        'desc': 'BETTER DESCRIPTION HERE: Modulation On Frequency',
        'section': 'Audio',
        'key': 'output.modulation_on_frequency',
    },
    {
        'type': 'numeric',
        'title': 'Modulation Off Frequency',
        'desc': 'BETTER DESCRIPTION HERE: Modulation Off Frequency',
        'section': 'Audio',
        'key': 'output.modulation_off_frequency',
    },
    {
        'type': 'options',
        'options': [
           '16 Bit',
           '24 Bit'
      ],
        'title': 'Input Bit Depth',
        'desc': 'BETTER DESCRIPTION HERE: Input Bit Depth',
        'section': 'Audio',
        'key': 'input.bit_depth',
    },
    {
        'type': 'options',
        'options': [
           '48,000Khz',
           '44,100Khz'
      ],
        'title': 'Input Sample Rate',
        'desc': 'BETTER DESCRIPTION HERE: Input Sample Rate',
        'section': 'Audio',
        'key': 'input.sample_rate',
    },
    {
        'type': 'numeric',
        'title': 'Sublayer Height',
        'desc': 'BETTER DESCRIPTION HERE: Sublayer Height',
        'section': 'Options',
        'key': 'sublayer_height_mm',
    },
    {
        'type': 'numeric',
        'title': 'Laser_thickness_mm',
        'desc': 'BETTER DESCRIPTION HERE: Laser_thickness_mm',
        'section': 'Options',
        'key': 'laser_thickness_mm',
    },
    {
        'type': 'numeric',
        'title': 'Laser_offset',
        'desc': 'BETTER DESCRIPTION HERE: Laser_offset',
        'section': 'Options',
        'key': 'laser_offset',
    },
    {
        'type': 'numeric',
        'title': 'Scaling_factor',
        'desc': 'BETTER DESCRIPTION HERE: Scaling_factor',
        'section': 'Options',
        'key': 'scaling_factor',
    },
    {
        'type': 'numeric',
        'title': 'Overlap_amount',
        'desc': 'BETTER DESCRIPTION HERE: Overlap_amount',
        'section': 'Options',
        'key': 'overlap_amount',
    },
    {
        'type': 'bool',
        'title': 'Use_shufflelayers',
        'desc': 'BETTER DESCRIPTION HERE: Use_shufflelayers',
        'section': 'Options',
        'key': 'use_shufflelayers',
    },
    {
        'type': 'bool',
        'title': 'Use_sublayers',
        'desc': 'BETTER DESCRIPTION HERE: Use_sublayers',
        'section': 'Options',
        'key': 'use_sublayers',
    },
    {
        'type': 'bool',
        'title': 'Use_overlap',
        'desc': 'BETTER DESCRIPTION HERE: Use_overlap',
        'section': 'Options',
        'key': 'use_overlap',
    },
    {
        'type': 'numeric',
        'title': 'Print_queue_delay',
        'desc': 'BETTER DESCRIPTION HERE: Print_queue_delay',
        'section': 'Options',
        'key': 'print_queue_delay',
    },
    {
        'type': 'numeric',
        'title': 'Pre_layer_delay',
        'desc': 'BETTER DESCRIPTION HERE: Pre_layer_delay',
        'section': 'Options',
        'key': 'pre_layer_delay',
    },
    {
        'type': 'numeric',
        'title': 'Drips_per_mm',
        'desc': 'BETTER DESCRIPTION HERE: Drips_per_mm',
        'section': 'Dripper',
        'key': 'drips_per_mm',
    },
    {
        'type': 'numeric',
        'title': 'Max_lead_distance_mm',
        'desc': 'BETTER DESCRIPTION HERE: Max_lead_distance_mm',
        'section': 'Dripper',
        'key': 'max_lead_distance_mm',
    },
    {
        'type': 'options',
        'options': [
           'Audio',
           'Emulated',
           'Photo'
      ],
        'title': 'Dripper_type',
        'desc': 'BETTER DESCRIPTION HERE: Dripper_type',
        'section': 'Dripper',
        'key': 'dripper_type',
    },
    {
        'type': 'numeric',
        'title': 'Emulated_drips_per_second',
        'desc': 'BETTER DESCRIPTION HERE: Emulated_drips_per_second',
        'section': 'Dripper',
        'key': 'emulated_drips_per_second',
    },
    {
        'type': 'numeric',
        'title': 'Photo_zaxis_delay',
        'desc': 'BETTER DESCRIPTION HERE: Photo_zaxis_delay',
        'section': 'Dripper',
        'key': 'photo_zaxis_delay',
    },
    {
        'type': 'numeric',
        'title': 'Max_deflection',
        'desc': 'BETTER DESCRIPTION HERE: Max_deflection',
        'section': 'Calibration',
        'key': 'max_deflection',
    },
    {
        'type': 'numeric',
        'title': 'Height',
        'desc': 'BETTER DESCRIPTION HERE: Height',
        'section': 'Calibration',
        'key': 'height',
    },
    {
        'type': 'numeric',
        'title': 'Lower_points',
        'desc': 'BETTER DESCRIPTION HERE: Lower_points',
        'section': 'Calibration',
        'key': 'lower_points',
    },
    {
        'type': 'numeric',
        'title': 'Upper_points',
        'desc': 'BETTER DESCRIPTION HERE: Upper_points',
        'section': 'Calibration',
        'key': 'upper_points',
    },
    {
        'type': 'bool',
        'title': 'On',
        'desc': 'BETTER DESCRIPTION HERE: On',
        'section': 'Serial',
        'key': 'on',
    },
    {
        'type': 'string',
        'title': 'Port',
        'desc': 'BETTER DESCRIPTION HERE: Port',
        'section': 'Serial',
        'key': 'port',
    },
    {
        'type': 'string',
        'title': 'On_command',
        'desc': 'BETTER DESCRIPTION HERE: On_command',
        'section': 'Serial',
        'key': 'on_command',
    },
    {
        'type': 'string',
        'title': 'Off_command',
        'desc': 'BETTER DESCRIPTION HERE: Off_command',
        'section': 'Serial',
        'key': 'off_command',
    },
    {
        'type': 'string',
        'title': 'Layer_started',
        'desc': 'BETTER DESCRIPTION HERE: Layer_started',
        'section': 'Serial',
        'key': 'layer_started',
    },
    {
        'type': 'string',
        'title': 'Layer_ended',
        'desc': 'BETTER DESCRIPTION HERE: Layer_ended',
        'section': 'Serial',
        'key': 'layer_ended',
    },
    {
        'type': 'string',
        'title': 'Print_ended',
        'desc': 'BETTER DESCRIPTION HERE: Print_ended',
        'section': 'Serial',
        'key': 'print_ended',
    },
    {
        'type': 'bool',
        'title': 'On',
        'desc': 'BETTER DESCRIPTION HERE: On',
        'section': 'Email',
        'key': 'on',
    },
    {
        'type': 'numeric',
        'title': 'Port',
        'desc': 'BETTER DESCRIPTION HERE: Port',
        'section': 'Email',
        'key': 'port',
    },
    {
        'type': 'string',
        'title': 'Host',
        'desc': 'BETTER DESCRIPTION HERE: Host',
        'section': 'Email',
        'key': 'host',
    },
    {
        'type': 'string',
        'title': 'Sender',
        'desc': 'BETTER DESCRIPTION HERE: Sender',
        'section': 'Email',
        'key': 'sender',
    },
    {
        'type': 'string',
        'title': 'Recipient',
        'desc': 'BETTER DESCRIPTION HERE: Recipient',
        'section': 'Email',
        'key': 'recipient',
    },
    {
        'type': 'numeric',
        'title': 'Base_height',
        'desc': 'BETTER DESCRIPTION HERE: Base_height',
        'section': 'Cure Rate',
        'key': 'base_height',
    },
    {
        'type': 'numeric',
        'title': 'Total_height',
        'desc': 'BETTER DESCRIPTION HERE: Total_height',
        'section': 'Cure Rate',
        'key': 'total_height',
    },
    {
        'type': 'numeric',
        'title': 'Start_speed',
        'desc': 'BETTER DESCRIPTION HERE: Start_speed',
        'section': 'Cure Rate',
        'key': 'start_speed',
    },
    {
        'type': 'numeric',
        'title': 'Finish_speed',
        'desc': 'BETTER DESCRIPTION HERE: Finish_speed',
        'section': 'Cure Rate',
        'key': 'finish_speed',
    },
    {
        'type': 'numeric',
        'title': 'Draw_speed',
        'desc': 'BETTER DESCRIPTION HERE: Draw_speed',
        'section': 'Cure Rate',
        'key': 'draw_speed',
    },
    {
        'type': 'bool',
        'title': 'Use_draw_speed',
        'desc': 'BETTER DESCRIPTION HERE: Use_draw_speed',
        'section': 'Cure Rate',
        'key': 'use_draw_speed',
    },
    {
        'type': 'string',
        'title': 'Port',
        'desc': 'BETTER DESCRIPTION HERE: Port',
        'section': 'Micro Controller',
        'key': 'port',
    },
    {
        'type': 'numeric',
        'title': 'Rate',
        'desc': 'BETTER DESCRIPTION HERE: Rate',
        'section': 'Micro Controller',
        'key': 'rate',
    },
    {
        'type': 'string',
        'title': 'Header',
        'desc': 'BETTER DESCRIPTION HERE: Header',
        'section': 'Micro Controller',
        'key': 'header',
    },
    {
        'type': 'string',
        'title': 'Footer',
        'desc': 'BETTER DESCRIPTION HERE: Footer',
        'section': 'Micro Controller',
        'key': 'footer',
    },
    {
        'type': 'string',
        'title': 'Escape',
        'desc': 'BETTER DESCRIPTION HERE: Escape',
        'section': 'Micro Controller',
        'key': 'escape',
    },
    {
        'type': 'options',
        'options': [
           'Analog',
           'Microcontroller'
      ],
        'title': 'Circut_type',
        'desc': 'BETTER DESCRIPTION HERE: Circut_type',
        'section': 'Circut',
        'key': 'circut_type',
    },
    {
        'type': 'options',
        'options': [
           'pe1.99b',
           'pb3.23r',
           'pp122yui'
      ],
        'title': 'Version',
        'desc': 'BETTER DESCRIPTION HERE: Version',
        'section': 'Circut',
        'key': 'version',
   },

]