#!/usr/bin/env bash

allure_logdir=reports

pytest --alluredir=$allure_logdir -s -v pytest_selenium_allure.py
allure serve $allure_logdir