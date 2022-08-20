#!/bin/bash
#!/user/bin/env pythonnoetic

echo "Local Package Started..."

local1

echo "====Ublox Package Started===="

python3 ahrs_parser.py

echo "====AHRS Data is Publishing===="

python3 encoder_parser.py

echo "====Encoder Data is Publishing===="

python3 serial_io.py

echo "====serial_io Started===="

echo "Where is base?? : KCity, Siheung..."
read base

python3 local.py --base ${base}