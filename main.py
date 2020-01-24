import os

import requests
import time
from miio.airpurifier import AirPurifier, AirPurifierException


def main():
	ip = os.getenv('AQM_IP')
	if not ip:
		raise RuntimeError('not configured')
	token = os.getenv('AQM_TOKEN')
	if not token:
		raise RuntimeError('not configured')
	prom_url = os.getenv('PROM_URL')
	if not prom_url:
		raise RuntimeError('not configured')

	while True:
		time.sleep(30)
		try:
			device = AirPurifier(ip=ip, token=token)
			print(f"AQI: {device.status().aqi}")
			data = f"""
				# TYPE iot_cn_aqi gauge
				iot_cn_aqi {device.status().aqi}
			"""

			r = requests.post(prom_url, data=data)
		except AirPurifierException as e:
			print("Cannot connect to device")
			print(e)
		except Exception as e:
			print(e)


if __name__ == '__main__':
	main()
