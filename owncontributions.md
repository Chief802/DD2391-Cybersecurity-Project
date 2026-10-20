# Own Contributions
This page gives an overview of individual contributions by the different members of the project. 
There was collaboration and discussions on many different parts between all members however, either in person or online.

## Aron

In preparation for investigating BLE devices, the best tool for fulfilling our project statement needed to be identified. 
On the preparation stage, we all investigated different tools, and I looked at how well Wireshark would function as a method of scanning and enumerating Bluetooth devices.
This did show promise, giving information such as the source and destination of each device, the protocol, length, and other information. 
The information we needed could be found with the help of the Bleak tool however, which also gave more flexibility as we could more easily work with a script of our own.

In the stage of code-writing, in addition to working on bluetoothscanner.py for reasons such as fixing inconsistencies or bugs that affected the program, I worked on testing to find where issues could lie.
This also involved doing some manual tests to investigate the accuracy of bluetoothscanner.py, which told us that there could be inaccuracies in the exact distance of a device,
even though it generally would be correct about how far away it was. 


## Leo

As stated we all investigated how best to fulfill the requirements of the project, as in finding the best tool. I investigated Python and using bleak in order to extract BLE data. This showed promise and could easily extract a lot of information from a lot of devices in close proximity. I also drafted and coded the ground work of the bluetoothscaner.py to get at rough idea of how it worked, what it could do and what the limitations where of the tool. It proved useful and was therefore selected as the basis of the project. I have then helped in completing the program and assisted in the creation of the deviceTracker.py extension program that is to continuously follow a selected device. I have also along with my peers tested these programs in order to find bugs and to see the extent of its usefulness.


## Ludwig
I primarily worked on the device_tracker.py script to continuosly check the distance to a singular device based on either the broadcast device name
or MAC/UUID. I integrated the old BLE scanner script to make it a complete command line tool where you first can scan for names and MACs and then target a specific
one to analyze the estimated distance over a mean signal strength which can be adjusted to either become more response or more stable depending on the needs by 
setting a flag.
I also improved on the original scan script in device_tracker.py by adding support for more manufacturer hex code by adding an external library.

I also dabbled with the task of connecting multiple scanners together, through communication to a central http server, to trilaterate the position of the
examined device relative to the positions of the scanners. I was only ever able to connect two scanners together so I couldn't get true trilateration but by examining
which of two scanners had the strongest connection to the device to determine which of the two points we were aiming towards.
This however, needed more testing to be fully integrated in the project.
