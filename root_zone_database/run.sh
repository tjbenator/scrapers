#!/bin/bash
scrapy runspider ./root_zone_database/spiders/iana.py -o file.csv -t csv
