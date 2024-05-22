# Motorised sliding door

A sliding door was made from balsa wood and actuated using a small stepper motor. The door opens using a push button switch (green) and closes with a different switch (red). When the door reaches its limits of motion, it presses a microswitch, which is detected and the Arduino stops the motor from trying to move the door any further.

The circuit diagram excluding the Arduino (a Seeed Xiao ESP32C3) is shown below. The pin number (e.g. `D0`) is shown in blue.

![](circuit-diagram.drawio.png)

To run the tests, uncomment the `test()` function and comment the main code.
