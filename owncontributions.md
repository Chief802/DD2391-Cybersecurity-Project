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

