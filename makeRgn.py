# Convert CSV to region file

infile = '/home/mknapp/VLSS_11deg.csv'
outfile = '/home/mknapp/VLSSrgn_all.rgn'

inf=open(infile, 'r')
of = open(outfile, 'w+')

# Write header
of.write('#CRTFv0\n')
of.write('global coord=J2000, color=yellow\n')

for line in inf.readlines():
	if line.startswith('#'):
		continue
	tmp = line.split(',')
	of.write('circle[['+tmp[1]+'deg, '+tmp[2]+'deg], 15pix]\n')
inf.close()
of.close()