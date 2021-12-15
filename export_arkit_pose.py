import unreal
import json
import os
import numpy as np


def write_json(file_name, file):
    with open(file_name, 'w') as fw:
        json.dump(file, fw)
        print("save {}".format(file_name))


if __name__ == "__main__":

    animation_path = r"/Game/MetaHumans/Common/Common/Mocap/mh_arkit_mapping_anim.mh_arkit_mapping_anim"
    animation = unreal.load_asset(animation_path, unreal.AnimationAsset)
    animation_track_names= unreal.AnimationLibrary.get_animation_curve_names(animation, unreal.RawCurveTrackTypes.RCT_FLOAT)
    output_path = r"E:\UE4_project\custom_metahuman\Content\liyouwang\python"
    # print(animation_track_names)
    global_frame_index_set = set()
    num_frames = unreal.AnimationLibrary.get_num_frames(animation)
    for animation_track_name in animation_track_names:
        times, values = unreal.AnimationLibrary.get_float_keys(animation, animation_track_name)
        assert len(times) == num_frames, "animation length is not right!"
    # frame = unreal.AnimationLibrary.get_frame_at_time(animation, time)
    animaiton_dict = {}
    text_label = "Working!"
    dcc_easy_list = []
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
                if frame in global_frame_index_set:
                    if dcc_easy_list[i]["frameIndex"] == frame:
                        dcc_easy_list[i]["keyValues"][str(animation_track_name).split('_')[-1]] = values[i]
                    else:
                        for data in dcc_easy_list:
                            if data["frameIndex"] == frameIndex:
                                data["keyValues"][str(animation_track_name).split('_')[-1]] = values[i]
                                break
                else:
                    tmp["frameIndex"] = frame
                    tmp["time"] = times[i]
                    global_frame_index_set.add(frame)
                    tmp['keyValues'] = {}
                    tmp['keyValues'][str(animation_track_name).split('_')[-1]] = values[i]
                    # animaiton_dict[str(animation_track_name)].append(tmp)
                    dcc_easy_list.append(tmp)
            slow_task.enter_progress_frame(1)
        write_json(os.path.join(output_path, "output_ani.json"), dcc_easy_list)