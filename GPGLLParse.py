withdata = "$GPGLL,4916.45,N,12311.12,W,225444,A,*1D\r\n"
emptydata = "$GPGLL,,,,,,A,*1D\r\n"


def gpgll_parse(sentence):
	words = sentence.split(',')
	if words[1] != '':
		nmealat = words[1].split('.')
		lat = int(nmealat[0][:-2]) + int(nmealat[0][-2:]) / 60 + int(nmealat[1]) / 6000
		lat = lat * 2 * ((words[2] == 'N') - 0.5)

		nmealon = words[3].split('.')
		lon = int(nmealon[0][:-2]) + int(nmealon[0][-2:]) / 60 + int(nmealon[1]) / 6000
		lon = lon * 2 * ((words[4] == 'E') - 0.5)
		return lat, lon
	return 0, 0


print(gpgll_parse(withdata))
print(gpgll_parse(emptydata))
