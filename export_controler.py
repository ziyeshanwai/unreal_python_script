import unreal
import json
import os


def export_fbx(map_asset_path, sequencer_asset_path, output_file):
    # Load the map, get the world
    world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
    # Load the sequence asset
    sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
    # Set Options
    export_options = unreal.FbxExportOption()
    export_options.ascii = False
    export_options.level_of_detail = False
    # Get Bindings
    bindings = sequence.get_bindings()
    # Export
    unreal.SequencerTools.export_fbx(world, sequence, bindings, export_options, output_file)
    unreal.log("export finish")
    return


def write_json(file_name, file):
    with open(file_name, 'w') as fw:
        json.dump(file, fw)
        print("save {}".format(file_name))




if __name__ == "__main__":
    unreal.log("start call")
    map_asset_path = r"/Game/Levels/my_map"
    sequencer_asset_path = r"/Game/mypractice/sequence/mag/mag.mag"
    output_file = r"E:/UE4_project/AIFA_metahuman/Content/export_fbx"
    sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
    all_tracks = []
    all_float_keys = []
    for object_binding in sequence.get_bindings():
        if object_binding.get_name() == "DynamicSkeletalMeshComponent0_0":
            all_tracks.extend(object_binding.get_tracks())
    unreal.log("load all tracks")
    print("the length of track is {}".format(len(all_tracks)))
    sections = []
    
    for track in all_tracks:
        for section in track.get_sections():
            print(section.get_name())
            if section.get_name() == "MovieSceneControlRigParameterSection_0":
                sections.append(section)
    i = 0
    export_dict = {}
    for channel in sections[0].find_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
        if channel:
            keys = channel.get_keys()
            name = channel.get_name()
            # frame_index = key.get_time().frame_number.value
            # time = key.get_time().sub_frame 
            value = [[key.get_value(), key.get_time().frame_number.value] for key in keys]
            export_dict[name] = value
    write_json(os.path.join(output_file, "controller.json"), export_dict)
            # if i==0:
            #     print(channel.get_name())
            #     print(len(keys))
            #     for key in keys:
            #         print('Frame:{0:5d} time:{1:4.3f} Value: {2: 6.5f}'.format(key.get_time().frame_number.value, key.get_time().frame_number.value/60, key.get_value()))
            # i += 1
            # print('Added {0} keys from channel: {1} on section: {2}'.format(len(keys), channel.get_name(), section.get_name()))
            # all_float_keys.extend(keys)
    # for key in all_float_keys:
    #     # print('Time: {0: 6d}:{1:4.3f} Value: {2: 6.2f} InterpMode: {3} TangentMode: {4} TangentWeightMode: {5} ArriveTangent: {6:+11.8f} ArriveTangentWeight: {7:+9.4f}  LeaveTangent: {8:+11.8f} LeaveTangentWeight: {9:+9.4f}'.format(key.get_time().frame_number.value, key.get_time().sub_frame, key.get_value(), key.get_interpolation_mode(), key.get_tangent_mode(), key.get_tangent_weight_mode(), key.get_arrive_tangent(), key.get_arrive_tangent_weight(), key.get_leave_tangent(), key.get_leave_tangent_weight()))
