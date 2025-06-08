# HomeTempIOT

It's getting hot outside and I can't just open my windows to let the cool air in.
I wanted a way to know when I should open my windows, so I created a python script.
Using an ESP board with a temp sensor I get the temperature in my living room, and
I fetch the outside temperature using OpenWeather's API.
If the temp outside is lower I get a desktop notification to open the windows.

Also as a bonus I added a notification in case the forecast shows rain in the next hours, that way I can get my laundry from outside.

In the future I could add another board on my balcony so I get more precise measurements and upgrade it to a more standalone weatherstation. Also, phone notifications should be added at some point

## TODO

Until I get the ESP8266 working, I will simulate the temperature input.
Server will also be running on ESP8266, so now it is running on my PC (server.py)