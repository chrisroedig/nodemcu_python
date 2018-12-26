# Dev environment for using MicroPython on NodeMCU boards

This repo should provide the basics for using nodeMCU boards with python. The goal is to make everything easy to do and to shorten the feedback loop when developing code for this hardware.
This work is mainly for my own convenience. If it you find it useful, that's cool too. Feel free to collaborate by opening PRs issues.

If you're a hardcore embedded C programmer, just stop reading. This will make you cringe....

The idea is to make programming ESP8266 SoCs simple, much like Ruby on Rails makes web development simple.

* Why not Arduino IDE? I like Bikeshedding
* Why not PlatformIO? ....Bikesheds are more fun
* Why python? I like python

## Features

### Automation Scripts

Basically just shell scripts to quick work through repetitive tasks with the hardware. Later one this could be some kind of file watch and auto build/deplpoy thing.

* checking the environment for required configs, ports and software
* flashing mircopython firmware
* uploading application and supporting code
* entering REPL session

### Project Support

Some code that will likely be reused between projects.

* connecting to a wifi network

### This repo

The goal is to turn this into a package that can be included in a project, inspired by certain web development frameworks. For now it's just some starter code.

* `/app` your code, the method `run` within `app.py` is the entry point
* `/bin` shell scripts to handle automating environment tasks
* `/platform` reusable code support your application
* `/tmp` temporary directory for build artifacts
* `.env` local configuration

## Requirements

* only really tested on macOSX
* hardware requirements
  * anything compatible with micropython
  * example: https://www.amazon.com/HiLetgo-Internet-Development-Wireless-Micropython/dp/B010N1SPRK/ref=sr_1_1_sspa?s=pc&ie=UTF8&qid=1545859869&sr=1-1-spons&keywords=esp8266&psc=1
* required software
  * appropriate USB/UART driver for your board
    * for nodemcu it's likely this one: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
  * python (usually comes with OS)
  * esptool for flashing the firmware (python package): https://github.com/espressif/esptool
  * ampy for uploading files (python package): https://github.com/adafruit/ampy
  * picocom for console/REPl (viahomebrew): https://github.com/npat-efault/picocom

## Getting Started

### Setup

* install all the required software
* plug in your board
* copy `.env.example` to `.env`
* check the configs in `.env`
  * `NODEMCU_PORT` should exist file (using `ls /dev/cu.*`)
  * `MICROPYTHON_URL` should point to the desired (newest) version
  * wifi info (optional) should be for desired newtork
* flash the micropython firmware `bin/install`

### Running Code

* upload and run the application code `bin/run`
  * LED on board should start flashing once per second
* connect to the board's REPL `bin/repl`
  * you should see something like `application runnning`
  * push the reset button to hard reset the board, watch it boot
  * ctrl-C to stop the running code and enter python REPL
