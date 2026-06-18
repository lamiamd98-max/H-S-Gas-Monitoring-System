import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
import time
import random

async def run():
   drone = System()
   print("Connecting to PX4...")
   await drone.connect(system_address="udp://:14540")
   print("drone connected")

   print("Arming...")
   await drone.action.arm()
   print("Drone armed!")

   # Takeoff
   print("Taking off...")
   await drone.action.takeoff()
   await asyncio.sleep(10)



def get_h2s_reading() -> float:
   return random.uniform(1.0, 20.0)   #الارقام تمثل قراءه الغاز بوحدهPPM #


async def wait_for_connection(drone: System):
   async for state in drone.core.connection_state():
       if state.is_connected:
           print("✅ تم الاتصال بـ jMAVSim!")
           return


async def upload_mission(drone: System):
   print("📍 جاري تحميل نقاط الفحص...")

   mission_items = [
       MissionItem(
           latitude_deg=47.3985,   # خط العرض #
           longitude_deg=8.5460,   # خط الطول #
           relative_altitude_m=15,  # الارتفاع #
           speed_m_s=5,             # السرعه# 
           is_fly_through=False,    #يتوقف عند نقطه معينه#
           gimbal_pitch_deg=float('nan'), 
           gimbal_yaw_deg=float('nan'),
           camera_action=MissionItem.CameraAction.NONE,
           loiter_time_s=15,        # يبقى 15 ثانيه #
           camera_photo_interval_s=float('nan'),
           acceptance_radius_m=2,   #يعتبر وصل لو المسافه اقصر من 2 متر #
           yaw_deg=float('nan'),
           camera_photo_distance_m=float('nan'),
           vehicle_action=MissionItem.VehicleAction.NONE
       ),
       
   ]

   mission_plan = MissionPlan(mission_items)
   await drone.mission.upload_mission(mission_plan)
   print("✅ تم تحميل المسار (نقطتان للفحص)")


async def monitor_h2s(drone: System):
   last_update = 0.0  # وقت اخر قراءه #
   max_reading = 0.0  #اعلى قراءه مسجله #
   readings = []      # سجل القراءات السابقه اتوقع #
   start_time = time.monotonic() # وقت البدايه #
   duration = 10.0               # مده الفحص #



   async for position in drone.telemetry.position():

       now = time.monotonic()
       if now - last_update < 1.0:   # اتحكم في وقت القراءه وهي كل ثانيه #
           continue
       last_update = now

       if now - start_time >= duration:   
           print("⏱️  انتهت مدة الفحص — جاري العودة للقاعدة")
           await drone.action.return_to_launch()
           return "DONE"
       


       h2s_level = await asyncio.to_thread(get_h2s_reading)
       readings.append(h2s_level)

       if h2s_level > max_reading:
           max_reading = h2s_level

       lat = position.latitude_deg
       lon = position.longitude_deg
       alt = position.relative_altitude_m

       print("-" * 55)
       print(f"🕐 {time.strftime('%H:%M:%S')}")
       print(f"📍 الموقع: ({lat:.6f}, {lon:.6f})")
       print(f"🔼 الارتفاع: {alt:.2f} م")  
       print(f"☁️  H2S الحالي: {h2s_level:.2f} PPM")
       print(f"📊 أعلى قراءة: {max_reading:.2f} PPM")

       danger  = h2s_level >= 50.0
       warning = (not danger) and h2s_level >= 10.0
       safe    = (not danger) and (not warning)

       if danger:
           print("🚨🚨 خطر شديد! H2S > 50 PPM — RTL فوري!")
           await drone.action.return_to_launch()
           return "DANGER"

       if warning:
           print("⚠️  تحذير! H2S تجاوز الحد الآمن (10 PPM)")

       if safe:
           print("✅ المستوى آمن")

   return "DONE"


async def run():
   drone = System()

   print("🔌 جاري الاتصال بـ jMAVSim...")
   await drone.connect(system_address="udp://:14540")

   await asyncio.wait_for(wait_for_connection(drone), timeout=20.0)

   await upload_mission(drone)

   print("⚙️  جاري التسليح...")
   await drone.action.arm()
   print("✅ Drone Armed!")

   print("🚁 جاري الإقلاع...")
   await drone.action.takeoff()
   await asyncio.sleep(8)

   print("🗺️  بدء مسار الفحص...")
   await drone.mission.start_mission()

   print("\n🔍 بدء قياس كبريتيد الهيدروجين H2S...\n")
   result = await monitor_h2s(drone)

   if result == "DONE":
       print("\n✅ اكتملت المهمة بنجاح — جاري العودة للقاعدة")

   print("\n🏁 انتهت مهمة فحص H2S")


if __name__ == "__main__":
   asyncio.run(run())


