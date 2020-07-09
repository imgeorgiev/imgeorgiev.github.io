---
layout: post
title: Weather Widget
subtitle: I've developed a small embedded Nest-like device which shows weather and control smart-home appliances 
tags: [projects, embedded]
---

![Weather Widget](https://user-content.gitlab-static.net/dfc053c3347de799b85cd99fa59cf4b4476246d4/687474703a2f2f692e696d6775722e636f6d2f426766715051302e6a7067)

As a side project, I developed a cheap Nest
alternative which
can display time, weather forecast, ambient information and can be
controlled via a touchscreen.

## Hardware

I designed this as an easy single-board computer based around
a [2.8" LCD Screen](https://www.winstar.com.tw/products/tft-lcd/module/ili9341-tft.html)
I had lying around. To turn this into an IoT device, I used the
popular ESP8266 chip featuring a 32-bit RISC processor
and an onboard Wi-Fi module. Then to enable smarter
features, I equipped it with BMP180 temperature and
humidity sensor and an MCP23008 chip for additional IO
to control things around the house.

I designed a 2-layer PCB for this from the ground up using
Altium Designer. The board is wholly powered via Micro USB
and features no battery. Overall all the components on the
board are accessible for under $30, although getting them
might be more tricky.

The full files and libraries of components
can be found on the [repository of the project](https://gitlab.com/imgeorgiev/WeatherWidget).

## Software

The backend of the software is based on C++ with Arduino
to stick everything together. It reads sensory information
locally, downloads weather forecasts from
[Weather Underground](https://www.wunderground.com/)
and can communicate to an external server with
the MQTT IoT protocol.

The frontend comes in two parts. First, we have everything
that is displayed on the screen, as in the picture. It features
two screens: one to display weather and sensor data and one
to control things around the house. The display can be
interfaced via the touchscreen. Additionally, the small
Nest clone has another trick up its sleeve - a small
HTML web server, which can be used to reconfigure its settings!

The full code can be found in its
[repository](https://gitlab.com/imgeorgiev/WeatherWidget)
