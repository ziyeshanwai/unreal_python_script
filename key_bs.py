"""
author:liyouwang
the code is key animation curve and export the animaiton curve animation to fbx
import the fbx to dcc like blender and then you can do anything you can do in blender
"""
import unreal
import json
import os

def write_json(file_name, file):
    with open(file_name, 'w') as fw:
        json.dump(file, fw)
        print("save {}".format(file_name))


if __name__ == "__main__":

    animation_path = r"/Game/animation_sequence/bs_ani.bs_ani"
    animation = unreal.load_asset(animation_path, unreal.AnimationAsset)
    animation_track_names= unreal.AnimationLibrary.get_animation_curve_names(animation, unreal.RawCurveTrackTypes.RCT_FLOAT)
    output_path = r"E:/UE4_project/Content/ouput_json"
    unreal.AnimationLibrary.remove_all_curve_data(animation)
    
    for name in animation_track_names:
        unreal.AnimationLibrary.add_curve(animation, name, curve_type=unreal.RawCurveTrackTypes.RCT_FLOAT, meta_data_curve=False)
    time = unreal.Array(float)
    times = [unreal.AnimationLibrary.get_time_at_frame(animation, i) for i in range(0, len(animation_track_names))]
    for t in times:
        if unreal.AnimationLibrary.is_valid_time(animation, t):
            time.append(t)
    text_label = "insert key "
    with unreal.ScopedSlowTask(len(animation_track_names), text_label) as slow_task:
        slow_task.make_dialog(True) 
        for i, animation_track_name in enumerate(animation_track_names):  # 按照channle 读入
            if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                break
            floatkeys = unreal.Array(float)
            for f in range(0, len(animation_track_names)):
                if i==f:
                    floatkeys.append(1)
                else:
                    floatkeys.append(0)
            unreal.AnimationLibrary.add_float_curve_keys(animation, animation_track_name, time, floatkeys)
            slow_task.enter_progress_frame(1)
    # write_json(os.path.join(output_path, "names.json"), {"names": [str(name) for name in animation_track_names]})
       