import unreal
import json
import os
import numpy as np


def load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    root_path = r""
    curve_data_file = ""
    animation_path = r""
    animation = unreal.load_asset(animation_path, unreal.AnimationAsset)
   
    unreal.AnimationLibrary.remove_all_curve_data(animation)
    
    curve_data = load_json(os.path.join(root_path, curve_data_file))

    text_label = "insert key "
    with unreal.ScopedSlowTask(len(curve_data), text_label) as slow_task:
        slow_task.make_dialog(True) 
        for key in list(curve_data.keys()):  # 按照channle 读入
            if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                break
            unreal.AnimationLibrary.add_curve(animation, key, curve_type=unreal.RawCurveTrackTypes.RCT_FLOAT, meta_data_curve=False)
            floatkeys = unreal.Array(float)
            for data in curve_data[key]:
                floatkeys.append(data['value'])
                print("insert value: {}".format(data['value']))
            time = unreal.Array(float)
            times = [unreal.AnimationLibrary.get_time_at_frame(animation, data['frameNum']) for data in curve_data[key]]
            for t in times:
                if unreal.AnimationLibrary.is_valid_time(animation, t):
                    time.append(t)
            unreal.AnimationLibrary.add_float_curve_keys(animation, key, time, floatkeys)
            slow_task.enter_progress_frame(1)
    print("insert animaiton successful") 