import unreal
import json
import os
import math

def export_selected_animation_curves_to_json(output_dir):
    """
    导出当前选中的动画序列中的所有曲线数据到JSON文件
    :param output_dir: 输出JSON文件的目录路径
    """
    # 获取选中的资产
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    
    # 确保只选中了一个动画序列
    if len(selected_assets) == 0:
        unreal.log_error("没有选中任何资产！")
        return
    
    if len(selected_assets) > 1:
        unreal.log_error("请只选择一个动画序列！")
        return
    
    anim_sequence = selected_assets[0]
    
    # 检查选中的资产是否是动画序列
    if not isinstance(anim_sequence, unreal.AnimSequence):
        unreal.log_error(f"选中的资产不是动画序列！类型: {anim_sequence.__class__}")
        return
    
    # 获取动画序列信息
    sequence_name = anim_sequence.get_name()
    asset_path = anim_sequence.get_path_name()
    
    # 获取动画序列的帧数
    num_frames = unreal.AnimationLibrary.get_num_frames(anim_sequence)
    duration = anim_sequence.get_editor_property("sequence_length")
    frame_rate_value = (num_frames - 1) / duration if duration > 0 else 30.0
    
    unreal.log(f"正在处理动画序列: {sequence_name}")
    unreal.log(f"路径: {asset_path}")
    unreal.log(f"帧数: {num_frames}, 帧率: {frame_rate_value:.2f}, 时长: {duration:.2f}秒")

    # 获取所有曲线名称
    try:
        curve_names = unreal.AnimationLibrary.get_animation_curve_names(anim_sequence, unreal.RawCurveTrackTypes.RCT_FLOAT)
        unreal.log(f"找到 {len(curve_names)} 条曲线")
        
        if len(curve_names) == 0:
            unreal.log_warning("未找到任何曲线数据！")
            return
            
    except Exception as e:
        unreal.log_error(f"无法获取曲线名称：{str(e)}")
        return

    # 准备数据结构
    animation_data = []
    
    # 创建进度对话框
    with unreal.ScopedSlowTask(len(curve_names), "正在导出动画曲线数据...") as slow_task:
        slow_task.make_dialog(True)
        
        # 遍历所有帧
        for frame in range(num_frames):
            frame_data = {
                "frameIndex": frame,
                "time": frame / frame_rate_value,
                "keyValues": {}
            }
            
            # 遍历所有曲线
            for curve_name in curve_names:
                if slow_task.should_cancel():
                    unreal.log_warning("用户取消了导出操作")
                    return
                    
                try:
                    # 获取曲线的关键帧时间和值
                    times, values = unreal.AnimationLibrary.get_float_keys(anim_sequence, curve_name)
                    
                    # 确保我们有足够的数据点
                    if frame < len(values):
                        # 获取当前帧的值
                        value = values[frame]
                        # 只保留曲线名称的最后一部分（去掉前缀）
                        simple_name = str(curve_name).split('_')[-1]
                        frame_data["keyValues"][simple_name] = round(value, 5)
                        
                except Exception as e:
                    unreal.log_warning(f"无法获取曲线 {curve_name} 在帧 {frame} 的值: {str(e)}")
                    frame_data["keyValues"][str(curve_name)] = 0.0
                
            animation_data.append(frame_data)
            slow_task.enter_progress_frame(1)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出路径
    json_filename = f"{sequence_name}_CurveData.json"
    output_path = os.path.join(output_dir, json_filename)
    
    # 导出JSON文件
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(animation_data, json_file, indent=2, ensure_ascii=False)
    
    unreal.log(f"成功导出曲线数据到: {output_path}")
    unreal.EditorDialog.show_message("导出成功", f"曲线数据已导出到:\n{output_path}", unreal.AppMsgType.OK)
    return output_path

# 使用示例
if __name__ == "__main__":
    # ===== 配置参数 =====
    # 输出目录（可以是项目外部的绝对路径）
    OUTPUT_DIR = r"D:\unreal_projects\UE554Project\python"  # 修改为您想要的输出路径
    # ===================
    
    export_path = export_selected_animation_curves_to_json(OUTPUT_DIR)