import unreal
import json
import os


if __name__ == "__main__":
    map_asset_path = r"/Game/Levels/my_map"
    sequencer_asset_path = r"/Game/N_pv_test/level2/level2.level2"
    sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
    all_tracks = []
    all_float_keys = []
    channel_name = "CTRL_C_jaw.Y"
    for object_binding in sequence.get_bindings():
        tracks = object_binding.get_tracks()
        for track in tracks:
            for section in track.get_sections():
                section_name = section.get_name()
                if "ControlRig" in section_name:
                    export_dict = {}
                    for channel in section.get_channels():
                        if channel:
                            value_list = []
                            name = channel.get_name()
                            if channel_name in  name:
                                keys = channel.get_keys()
                                buchang = keys[0].get_value()
                                # print(type(keys[0]))
                                # value = [[key.get_value(), key.get_time().frame_number.value] for key in keys]
                                
                                # value = [{"Time": "{0: 6d}:{1:4.3f}".format(key.get_time().frame_number.value, key.get_time().sub_frame), "value":key.get_value()} for key in keys]
                                # value_list = [{"Time": "{}".format(key.get_time(time_unit=unreal.SequenceTimeUnit.TICK_RESOLUTION).frame_number.value), "value":key.get_value()} for key in keys]
                                for key in keys:
                                    qua_time= unreal.QualifiedTime(frame=key.get_time().frame_number, frame_rate=sequence.get_display_rate(), sub_frame=key.get_time().sub_frame)
                                    channel.add_key(key.get_time().frame_number, key.get_value()-buchang,
                                    sub_frame=key.get_time().sub_frame, time_unit=unreal.SequenceTimeUnit.DISPLAY_RATE, interpolation=unreal.MovieSceneKeyInterpolation.LINEAR)