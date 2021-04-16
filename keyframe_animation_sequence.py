import unreal
import json
import os
import random
import pickle
import numpy as np

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


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))

if __name__ == "__main__":
    root_path = r"E:\project_N\xiaobai\project_test\1"
    curve_names_path = os.path.join(root_path, "pose_name_aifa.pkl")
    weights_path = os.path.join(root_path, "arkit_weights.pkl")
    animation_path = r"/Game/N_pv_test/lqc_smooth_1/lqc_smooth_1_modify_curve_drive.lqc_smooth_1_modify_curve_drive"
    animation = unreal.load_asset(animation_path, unreal.AnimationAsset)
   
    # animation_track_names = animation.get_editor_property("animation_track_names")  # 注意用法
    # animation_track_names = editor_properties.animation_track_names()
    # print("animation_track_names is {}".format(animation_track_names))
    """添加曲线"""
    unreal.AnimationLibrary.remove_all_curve_data(animation)
    curve_names = load_pickle_file(curve_names_path)
    curve_names.remove("head_geo.obj")
    expression_names = ["CTRL_expressions_{}".format(name[:-4]) for name in curve_names]
    for name in expression_names:
        unreal.AnimationLibrary.add_curve(animation, name, curve_type=unreal.RawCurveTrackTypes.RCT_FLOAT, meta_data_curve=False)

    
    # animation_track_names= unreal.AnimationLibrary.get_animation_curve_names(animation, unreal.RawCurveTrackTypes.RCT_FLOAT)
    # print(animation_track_names)
    # time, value = unreal.AnimationLibrary.get_float_keys(animation, animation_track_names[0])
    # print("time is {}".format(time))
    # print("value is {}".format(value))
    """
    插入关键帧
    """
    weights = np.array(load_pickle_file(weights_path)).T
    print(weights.shape)
    time = unreal.Array(float)
    times = [unreal.AnimationLibrary.get_time_at_frame(animation, i) for i in range(0, weights.shape[1])]
    print(len(times))
    for t in times:
        if unreal.AnimationLibrary.is_valid_time(animation, t):
            time.append(t)
    for i, name in enumerate(expression_names):
        #unreal.AnimationLibrary.add_float_curve_key
        floatkeys = unreal.Array(float)
        for f in range(0, weights.shape[1]):
            floatkeys.append(weights[i][f])
        unreal.AnimationLibrary.add_float_curve_keys(animation, name, time, floatkeys)
    print("insert animaiton successful") 
   