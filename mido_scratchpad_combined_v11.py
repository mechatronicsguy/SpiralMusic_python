import sys, os, pygame
from pygame import midi
import pygame.gfxdraw
import mido
import rtmidi
# from mido import MidiFile
import numpy as np
import time
import tkinter
import tkinter.filedialog



instrument_dict = {1: 'AcousticGrandPiano', 2: 'BrightAcousticPiano', 3: 'ElectricGrandPiano',
                   4: 'Honky-tonkPiano', 5: 'ElectricPiano1', 6: 'ElectricPiano2', 7: 'Harpsichord',
                   8: 'Clavinet', 9: 'Celesta', 10: 'Glockenspiel', 11: 'MusicBox', 12: 'Vibraphone',
                   13: 'Marimba', 14: 'Xylophone', 15: 'TubularBells', 16: 'Dulcimer', 17: 'DrawbarOrgan',
                   18: 'PercussiveOrgan', 19: 'RockOrgan', 20: 'ChurchOrgan', 21: 'ReedOrgan', 22: 'Accordion',
                   23: 'Harmonica', 24: 'TangoAccordion', 25: 'AcousticGuitar(nylon)', 26: 'AcousticGuitar(steel)',
                   27: 'ElectricGuitar(jazz)', 28: 'ElectricGuitar(clean)', 29: 'ElectricGuitar(muted)',
                   30: 'ElectricGuitar(overdriven)', 31: 'ElectricGuitar(distortion)', 32: 'ElectricGuitar(harmonics)',
                   33: 'AcousticBass', 34: 'ElectricBass(finger)', 35: 'ElectricBass(picked)', 36: 'FretlessBass',
                   37: 'SlapBass1', 38: 'SlapBass2', 39: 'SynthBass1', 40: 'SynthBass2', 41: 'Violin', 42: 'Viola',
                   43: 'Cello', 44: 'Contrabass', 45: 'TremoloStrings', 46: 'PizzicatoStrings', 47: 'OrchestralHarp',
                   48: 'Timpani', 49: 'StringEnsemble1', 50: 'StringEnsemble2', 51: 'SynthStrings1',
                   52: 'SynthStrings2', 53: 'ChoirAahs', 54: 'VoiceOohs', 55: 'SynthVoiceorSoloVox',
                   56: 'OrchestraHit', 57: 'Trumpet', 58: 'Trombone', 59: 'Tuba', 60: 'MutedTrumpet',
                   61: 'FrenchHorn', 62: 'BrassSection', 63: 'SynthBrass1', 64: 'SynthBrass2', 65: 'SopranoSax',
                   66: 'AltoSax', 67: 'TenorSax', 68: 'BaritoneSax', 69: 'Oboe', 70: 'EnglishHorn', 71: 'Bassoon',
                   72: 'Clarinet', 73: 'Piccolo', 74: 'Flute', 75: 'Recorder', 76: 'PanFlute', 77: 'Blownbottle',
                   78: 'Shakuhachi', 79: 'Whistle', 80: 'Ocarina', 81: 'Lead1(square)', 82: 'Lead2(sawtooth)',
                   83: 'Lead3(calliope)', 84: 'Lead4(chiff)', 85: 'Lead5(charang)', 86: 'Lead6(spacevoice)',
                   87: 'Lead7(fifths)', 88: 'Lead8(bassandlead)', 89: 'Pad1(newageorfantasia)', 90: 'Pad2(warm)',
                   91: 'Pad3(polysynthorpoly)', 92: 'Pad4(choir)', 93: 'Pad5(bowedglassorbowed)',
                   94: 'Pad6(metallic)', 95: 'Pad7(halo)', 96: 'Pad8(sweep)', 97: 'FX1(rain)',
                   98: 'FX2(soundtrack)', 99: 'FX3(crystal)', 100: 'FX4(atmosphere)', 101: 'FX5(brightness)',
                   102: 'FX6(goblins)', 103: 'FX7(echoesorechodrops)', 104: 'FX8(sci-fiorstartheme)',
                   105: 'Sitar', 106: 'Banjo', 107: 'Shamisen', 108: 'Koto', 109: 'Kalimba', 110: 'Bagpipe',
                   111: 'Fiddle', 112: 'Shanai', 113: 'TinkleBell', 114: 'AgogÃ´', 115: 'SteelDrums',
                   116: 'Woodblock', 117: 'TaikoDrum', 118: 'MelodicTomor808Toms', 119: 'SynthDrum',
                   120: 'ReverseCymbal', 121: 'GuitarFretNoise', 122: 'BreathNoise', 123: 'Seashore',
                   124: 'BirdTweet', 125: 'TelephoneRing', 126: 'Helicopter', 127: 'Applause', 128: 'Gunshot'}


def add_absolute_times_to_midi(midifile_in):
    output_list = []
    msg_count = 0
    current_time = 0
    for msg in midifile_in:
        # if msg.is_meta:
        #     continue

        current_time += msg.time
        output_list.append( [ current_time,msg])

        msg_count += 1
        # print(msg)
        # if msg_count > 10:
        #     print(type(msg),dir(msg))
        #     break
    return output_list


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    # From here: https://stackoverflow.com/questions/63801960/how-to-prompt-user-to-open-a-file-with-python3-pygame
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def channel_num_to_hue(channel_num):
    return np.mod(channel_num*20.0, 360)


def draw_circle_alpha(surface, color, center, radius):
    # From: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def draw_single_note(x_pos, y_pos, symbol_width, note_status, note_last_on_time):
    if len(note_status) is 0:
        # Note is off and possibly fading:
        note_duration = (pygame.time.get_ticks() - note_last_on_time)/1000.0
        fade_duration = 10.0 # seconds
        note_brightness_percentage = np.clip( (fade_duration-note_duration)/fade_duration, 0, 1.0)
        my_color = pygame.Color(10, 10, 10)
        my_color.hsva = (0.0,
                         0.0,  # Saturation
                         note_brightness_percentage*20.0+0.0,   # Value
                         1)
        pygame.draw.circle(screen, my_color, [x_pos, y_pos], symbol_width)
    else:
        # Note is on (and has colour based on channel number
        alpha_fraction = 100.0 / len(note_status)
        for note in note_status:
            # if len(note_status)>1:
            #     print("Double note: ", note_status)
            my_color = pygame.Color(50, 50, 50)
            my_color.hsva = (channel_num_to_hue(note.channel),  # Hue
                             100,  # Saturation
                             np.clip(note.velocity/128.0*80.0*2+20.0, 0, 100),  # Value
                             alpha_fraction)
            # my_color.a = 10
            # pygame.draw.circle(screen, my_color,[x_pos, y_pos] , symbol_width)
            draw_circle_alpha(screen, my_color, [x_pos, y_pos], symbol_width)

            # # Write MIDI note num (0-127) on notes, for checking:
            # write_text(str(note.note),
            #            x_pos- myfont.get_height() / 2.0,
            #            y_pos- myfont.get_height() / 2.0,
            #                pygame.Color(255, 255, 255))


def update_display_rectangular(skip_unchanged_notes=True):
    symbols_per_row = 12
    symbol_spacing = width*0.8 / symbols_per_row
    symbol_width = 14.0

    for n in range(0, 127):
        if note_update[n] or skip_unchanged_notes is False:
            note_update[n] = False
            x_num = np.mod(n, symbols_per_row)
            y_num = np.floor_divide(n, symbols_per_row)
            x_pos = x_num * symbol_spacing + symbol_width + width * 0.15
            y_pos = height-y_num * symbol_spacing - symbol_width

            draw_single_note(x_pos, y_pos, symbol_width, note_status[n], note_last_on_time[n])

            if n < 12:
                note_name = ['C', 'C#', 'D', 'D#',
                             'E', 'F', 'F#', 'G',
                             'G#', 'A', 'A#', 'B'][n]
                # x_pos_text = (r+symbol_spacing*1.3) * np.cos(theta) + width / 2.0
                # y_pos_text = (r+symbol_spacing*1.3) * np.sin(theta) + height / 2.0
                write_text(note_name, x_pos-myfont.get_height()/2.0, y_pos-myfont.get_height()/2.0,
                           pygame.Color(100, 100, 100))


def update_display_spiral(skip_unchanged_notes=True):
    symbol_width = 8.0
    symbol_spacing = 18.0
    centre_location = [width * 0.6, height * 0.5]

    spiral_locations = []
    for n in range(0, 127*4):
        r = ((127*4 - n) / 12.0)/4 * symbol_spacing + 10.0
        theta = -(127*4 - n) /4/12.0 * np.pi * 2.0 + np.pi / 2.0 + 2 * np.pi / 12
        x_pos = r * np.cos(theta) + centre_location[0]
        y_pos = r * np.sin(theta) + centre_location[1]
        spiral_locations.append([x_pos,y_pos])
    pygame.draw.lines(screen, pygame.color.Color(50, 50, 50),
                      False, spiral_locations, width=1)

    for n in range(0, 127):
        if note_update[n] or skip_unchanged_notes is False:
            note_update[n] = False
            r = ((127-n)/12.0) * symbol_spacing+10.0
            theta = -(127-n)/12.0 * np.pi * 2.0 + np.pi/2.0 +2*np.pi/12
            x_pos = r * np.cos(theta) + centre_location[0]
            y_pos = r * np.sin(theta) + centre_location[1]

            if n < 12:
                note_name = ['C', 'C#', 'D', 'D#',
                             'E', 'F', 'F#', 'G',
                             'G#', 'A', 'A#', 'B'][n]
                x_pos_text = (r+symbol_spacing*1.3) * np.cos(theta) + centre_location[0]
                y_pos_text = (r+symbol_spacing*1.3) * np.sin(theta) + centre_location[1]
                write_text(note_name, x_pos_text-myfont.get_height()/2.0, y_pos_text-myfont.get_height()/2.0,
                           pygame.Color(100, 100, 100))
            pygame.draw.circle(screen,
                               pygame.Color(100, 100, 100),
                               [x_pos, y_pos], symbol_width * 1.2, width=1)


            draw_single_note(x_pos, y_pos, symbol_width,note_status[n],note_last_on_time[n])


def write_text(text_str, x_loc, y_loc, my_color):
    textsurface = myfont.render(text_str, False, my_color)
    screen.blit(textsurface, (x_loc, y_loc))


def do_housekeeping_gui():
    write_text(midi_filename, width/3, 0, pygame.Color(127, 127, 127))
    for channel_num in range(1, 30):
        instrument_num = channel_instrument[channel_num]
        instrument_name = instrument_dict.get( instrument_num, "-")
        my_color = pygame.Color(50, 50, 50)
        my_color.hsva = (channel_num_to_hue(channel_num),  # Hue
                         100,  # Saturation
                         np.clip(100 / 128.0 * 80.0 * 2 + 20.0, 0, 100),  # Value
                         0)
        # if channel_num == 9:
        #     instrument_name = "  " + instrument_name
        instrument_name = str(channel_num) +" "+ instrument_name
        write_text(instrument_name,0, (channel_num-1 )* 16,my_color)

# midi_filename = 'midi/toccata_and_fugue_in_d_minor.mid'
# midi_filename = 'midi/toccataandfugue.mid' # This one is good:
# midi_filename = 'midi/toccataefuga_inversion.mid'
# midi_filename = 'midi/Song-stories-for-the-kindergarten_1896_twinkle-twinkle-little-star_sheet-music.mid'
# midi_filename = 'midi/beethoven_symphony_5_1_(c)galimberti.mid'
# midi_filename = 'midi/strawberry_fields_forever.mid'
midi_filename = 'midi/radioGAGA.mid'
# midi_filename = 'midi/youcancallmeal.mid'
# midi_filename = 'midi/magiccarpet.mid'
# midi_filename = 'midi/beethoven_op92_1_mod.mid'
# midi_filename = 'midi/suddenly-seymour.mid'
# midi_filename = 'midi/ShakeItOff.mid'
# midi_filename = 'midi/ridevalk.mid'
# midi_filename = 'midi/greatgig.mid'
# midi_filename = 'midi/AbbaTakeachanceonme.mid'
# midi_filename = 'midi/birdhouse_in_your_soul.mid'
# midi_filename = 'midi/symphony_9_4_(c)cvikl.mid'
# midi_filename = 'midi/Hungarian_Rhapsody.mid'
# midi_filename = 'midi/1812ovt.mid'
# midi_filename = 'midi/barbersevilcl.mid'
# midi_filename = 'midi/tom-sawyer-3.mid'
# midi_filename = 'midi/good-bad.mid'
# midi_filename = 'midi/THUNDERS.MID'
# midi_filename = 'midi/sympathy2.mid'
# midi_filename = 'midi/Eine-Kleine-Nachtmusik1-Flute.mid'
# midi_filename = 'midi/einekleine.mid' # Sucpect?
# midi_filename = 'midi/musical_opfer_bwv-1079-2_(unknown-grossman).mid'
# midi_filename = 'midi/bach_brandeburg_concert_1047_1_(nc)anonym.mid'
# midi_filename = 'midi/bach_brandeburg_concert_1049_1_(nc)anonym.mid' #Skips
# midi_filename = 'midi/bach_brandeburg_concert_1051_1_(c)siu.mid'
# midi_filename = 'midi/rimsky-kosakov_70301a_flight_of_the_bumble_bee_(nc)smythe.mid' # good
# midi_filename = 'midi/rossini_6232d_william_tell_overture_(nc)smythe.mid'
# midi_filename = 'midi/rossini_60103a_william_tell_overture_(part_1)_(nc)smythe.mid'
# midi_filename = 'midi/vivaldi_4_stagioni_primavera_1_(c)pollen.mid' # something funny here.
# midi_filename = 'midi/4tcqogmi.mid'
# midi_filename = 'midi/4tcqogmi_mod.mid'
# midi_filename = 'midi/4tcqogmi_mod3.mid'
# midi_filename = 'midi/4tcqogmi_mod3split.mid'

midifile = mido.MidiFile(midi_filename) #os.path.join('midi', midi_filename))
print("file has length: ", midifile.length)
absolute_midi_notes_list = add_absolute_times_to_midi(midifile)

pygame.font.init()
pygame.init()
size = width, height = 800, 800*9/16

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont('Comic Sans MS', 16)

# pygame.midi.init()
# print("Default input device is: ",pygame.midi.get_default_input_id())
# print("Default output device is: ",pygame.midi.get_default_output_id())
# for device_id in range(pygame.midi.get_count()):
#     print("Device: ", device_id, midi.get_device_info(device_id ))

MIDO_output_names = mido.get_output_names()
print("MIDO library, MIDI output names are: ",MIDO_output_names)
output_port = mido.open_output(MIDO_output_names[0])
print("\toutput port: ", output_port)

note_status = [[]]*128
note_update = [True]*128
note_last_on_time = [-10000.0]*128
channel_instrument = [None]*128
f = "<No File Selected>"

# for x in absolute_midi_notes_list:
#     print(x)

offset_time = pygame.time.get_ticks()

while True:# pygame.time.get_ticks()<30000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                f = prompt_file()

    if len(absolute_midi_notes_list) == 0:
        # File finished.
        break

    while absolute_midi_notes_list[0][0]*1000.0 <= (pygame.time.get_ticks() - offset_time):
        # Process any notes that are overdue before moving to screen drawing stuff:
        msg = absolute_midi_notes_list[0][1]

        absolute_midi_notes_list.pop(0)
        if len(absolute_midi_notes_list)==0:
            # File finished.
            break

        if not (len(msg.bytes())>3 and (msg.bytes()[0] != 0xF0)): #msg.type not in ['set_tempo','time_signature']:
            # Send to output (MIDI synth, to make noise).
            output_port.send(msg)

        if msg.type == 'program_change':
            # Track the assignemnt of instruments to MIDI channels.
            channel_instrument[msg.channel+1] = msg.program

        if msg.type == 'note_on':
            note_num = msg.note
            if (msg.channel+1) == 10 and channel_instrument[10] == None:
                # Probably percussion, skip.
                continue
            note_update[note_num] = True
            if msg.velocity == 0:
                # velocity 0 is an unconventional way to turn off a note.
                note_status[note_num] = [x for x in note_status[note_num] if x.channel != msg.channel]
            else:
                note_status[note_num] = note_status[note_num] + [msg]
                note_last_on_time[note_num] = pygame.time.get_ticks()
        elif msg.type == 'note_off':
            if (msg.channel+1) == 10 and channel_instrument[10] == None:
                # Percussion, skip.
                continue
            note_update[msg.note] = True
            note_status[msg.note] = [x for x in note_status[msg.note] if x.channel != msg.channel]

    ## update display:
    screen.fill(pygame.Color(0, 0, 0))

    if False:
        update_display_rectangular(skip_unchanged_notes=False)
    else:
        update_display_spiral(skip_unchanged_notes=False)
    do_housekeeping_gui()

    pygame.display.update()
