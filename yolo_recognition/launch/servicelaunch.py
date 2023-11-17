# from launch import LaunchService
# from yolo import generate_launch_description

# import time

# launch_service = LaunchService()
# launch_service.include_launch_description(generate_launch_description())
# # launch_service.run_async()

# def main():
#     condition = input("input: ")


#     # if condition:
#     #     # launch_service.run()
#     #     print(condition)_

#     try:
#         condition = bool(int(condition))
#     except ValueError:
#         print("Invalid input. Please enter either 0 or 1.")
#         condition = False


#     if condition:
#         launch_service.run()
#     elif not condition:
#         launch_service.shutdown()

#         # time.sleep(5)
#         # launch_service.shutdown()
#         # print(condition)

# if __name__ == "__main__":
#     main()

import time
import asyncio
import multiprocessing

from launch import LaunchService
from yolo import generate_launch_description

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Ros2LaunchParent:
    def start(self, launch_description):
        self._stop_event = multiprocessing.Event()
        self._process = multiprocessing.Process(target=self._run_process, args=(self._stop_event, launch_description), daemon=True)
        self._process.start()

    def shutdown(self):
        self._stop_event.set()
        self._process.join()

    def _run_process(self, stop_event, launch_description):
        loop = asyncio.get_event_loop()
        launch_service = LaunchService()
        launch_service.include_launch_description(launch_description)
        launch_task = loop.create_task(launch_service.run_async())
        loop.run_until_complete(loop.run_in_executor(None, stop_event.wait))
        if not launch_task.done():
            asyncio.ensure_future(launch_service.shutdown(), loop=loop)
            loop.run_until_complete(launch_task)

# class MyRos2Launcher(Ros2LaunchParent):
#     def __init__(self):
#         super().__init__()

class LaunchServiceAsync(Node):

    def __init__(self):
        super().__init__('LegConnection_service'):
        self.srv() = self.create_service(Trigger, 'leg_trigger', self.callback_trigger)

    def callback_trigger(self):


def launc_main(args=None):
    launcher = Ros2LaunchParent()
    launch_description = generate_launch_description()
    
    try:
        launcher.start(launch_description)
        # Your main application code can run here
        time.sleep(10)
        launcher.shutdown()

    except KeyboardInterrupt:
        pass
    finally:
        launcher.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = LaunchServiceAsync()

    client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
