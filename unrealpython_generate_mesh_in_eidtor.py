import unreal
obj = unreal.load_asset('/Game/asset/suzan')
for i in range(0, 10):
    actor_location = unreal.Vector(0.0,0.0,i*150)
    actor_rotation = unreal.Rotator(0.0,0.0,0.0)
    unreal.EditorLevelLibrary.spawn_actor_from_object(obj, actor_location, actor_rotation)