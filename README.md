## In summary
This software automatically turns on a SONOFF S31 Lite power plug's relay when it is first plugged in, and also back on 30 seconds anytime after the relay is turned off assuming the S31 remains plugged in and powered.

**It has been written to run via Home Assistant - ESPHOME and testing on a SONOFF S31 Lite power plug.**

# License
MIT

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Important note 
There are always risks associated with turning off power to a device without an ordered shutdown having first being completed. These risks are present when using this software.  

# Use case
My own use case for this is to help reboot my internet router.  

With this software flashed to my SONOFF S31 Lite power plug, I can (from my office) use Home Assistant to switch off the power to my internet router (which is in my basement) and know that it will automatically be turned back on in 30 seconds. 

Having that said, the software is also designed so that the power will be turned back on automatically in 30 seconds should it be turned off via the button on the S31 itself as well.

# Recommendation for first time use
Ensure the device running this software has access to Home Assistant at the location it will be used.

To do this is to plug the device running this software into to the power outlet that you intended to use with it, but do not yet plug anything into the device running this software.

Next, use ESPHOME's log feature to view the logs of the device running this software to confirm that this device is connecting though to Home Assistant.

Next, turn the device off either manually by pushing its button or add it to your Home Assistant dashboard and turn it off via the dashboard.  Once done wait 30 seconds and the relay should switch back on.

# A helpful video 
on how to install ESPHome softwar on a SONOFF S31 Lite can be found here:
[https://www.youtube.com/watch?v=S4-HVYPCA2c](https://www.youtube.com/watch?v=S4-HVYPCA2c&t=617s)

## Support

[<img alt="buy me  a coffee" width="200px" src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" />](https://www.buymeacoffee.com/roblatour)
 
