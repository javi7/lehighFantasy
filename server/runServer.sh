#!/bin/bash

sudo nohup python server.py 80 > logs/webLog.out 2> logs/error.out &
