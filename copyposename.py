import unreal
import json
import os

selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

if not selected_assets:
    print("plese select a PoseAsset first！")
else:
    pose_asset = selected_assets[0]
    if not isinstance(pose_asset, unreal.PoseAsset):
        print("the select assets is not a PoseAsset！")
    else:
        pose_names = pose_asset.get_pose_names()
        names_list = [str(name) for name in pose_names]
        
        # 创建输出目录（如果不存在）
        output_dir = os.path.dirname(os.path.realpath(__file__))
        output_file = os.path.join(output_dir, "pose_names.json")
        
        # 将姿势名称保存到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"pose_names": names_list}, f, indent=4, ensure_ascii=False)
        
        # 打印到控制台并通知用户
        names_str = "\n".join(names_list)
        unreal.log(names_str)
        print(f"姿势名称已保存到文件：{output_file}")