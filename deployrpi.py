import robotpy_installer.sshcontroller
import websockets
import json
import asyncio


ip_address = "10.55.28.6"

class SshController(robotpy_installer.sshcontroller.SshController):
    def put(self, src, dest):
        sftp = self.client.open_sftp()
        try:
            sftp.put(src, dest, confirm=False)
        finally:
            sftp.close()


async def async_send_message(msg):
    async with websockets.connect(f"ws://{ip_address}/", subprotocols=["frcvision"]) as websocket:
        while True:
            try:
                print(f"Sending {msg}...")
                await websocket.send(json.dumps({"type": msg}))
                print("Message sent.")
                break
            except Exception as e:
                print(e)
                await asyncio.sleep(1)


def send_message(msg):
    asyncio.get_event_loop().run_until_complete(async_send_message(msg))


send_message("systemWritable")

with SshController(ip_address, "pi", "raspberry") as controller:
    # controller.exec_cmd("cat runCamera", print_output=True)
    controller.put("visioncargo.py", "/home/pi/visioncargo.py")
    controller.put("visionhub.py", "/home/pi/visionhub.py")
    controller.put("visionmaster.py", "/home/pi/visionmaster.py")
    controller.put("runCamera", "/home/pi/runCamera")
    controller.exec_cmd("chmod 777 runCamera")
    controller.exec_cmd("rm -rf /home/pi/vision")
    controller.sftp("./vision", "/home/pi/")
    # controller.exec_cmd("pkill -f python3")

send_message("systemReadOnly")
send_message("visionKill")
