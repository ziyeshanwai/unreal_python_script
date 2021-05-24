import unreal
import json
import os
import numpy as np


def write_json(file_name, file):
    with open(file_name, 'w') as fw:
        json.dump(file, fw)
        print("save {}".format(file_name))


if __name__ == "__main__":

    animation_path = r"/Game/animation_sequence/firest_animaiton_sequence.firest_animaiton_sequence"
    animation = unreal.load_asset(animation_path, unreal.AnimationAsset)
    animation_track_names= unreal.AnimationLibrary.get_animation_curve_names(animation, unreal.RawCurveTrackTypes.RCT_FLOAT)
    output_path = r"E:/UE4_project/ouput_json"
    # print(animation_track_names)
    num_frames = unreal.AnimationLibrary.get_num_frames(animation)
    for animation_track_name in animation_track_names:
        times, values = unreal.AnimationLibrary.get_float_keys(animation, animation_track_name)
        assert len(times) == num_frames, "animation length is not right!"
    # frame = unreal.AnimationLibrary.get_frame_at_time(animation, time)
    animaiton_dict = {}
    text_label = "Working!"
    
    with unreal.ScopedSlowTask(len(animation_track_names), text_label) as slow_task:
        slow_task.make_dialog(True) 
        for animation_track_name in animation_track_names:  # 按照channle 读入
            if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                break
            times, values = unreal.AnimationLibrary.get_float_keys(animation, animation_track_name)
            animaiton_dict[str(animation_track_name)] = []
            for i in range(0, len(times)): 
                tmp = {} 
                frame = unreal.AnimationLibrary.get_frame_at_time(animation, times[i])
                tmp["frame_number"] = frame
                tmp["time"] = times[i]
                tmp['value'] = values[i]
                animaiton_dict[str(animation_track_name)].append(tmp)
                # gc.collect()
            # print(animaiton_dict[animation_track_name])
            slow_task.enter_progress_frame(1)
        write_json(os.path.join(output_path, "output_ani.json"), animaiton_dict)
    
    """
    插入关键帧[]
    """
    # weights = np.array(load_pickle_file(weights_path)).T
    # print(weights.shape)
    # time = unreal.Array(float)
    # times = [unreal.AnimationLibrary.get_time_at_frame(animation, i) for i in range(0, weights.shape[1])]
    # print(len(times))
    # for t in times:
    #     if unreal.AnimationLibrary.is_valid_time(animation, t):
    #         time.append(t)
    # for i, name in enumerate(expression_names):
    #     #unreal.AnimationLibrary.add_float_curve_key
    #     floatkeys = unreal.Array(float)
    #     for f in range(0, weights.shape[1]):
    #         floatkeys.append(weights[i][f])
    #     unreal.AnimationLibrary.add_float_curve_keys(animation, name, time, floatkeys)
    # print("insert animaiton successful") 