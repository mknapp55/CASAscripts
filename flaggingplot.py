# Plot flagging data

# Percentages:
plt.plot(np.array(ipct)*100, 'g.:')
plt.plot(np.array(fpct)*100, 'r.:')
plt.xlabel('Subband')
plt.ylabel('Percent data flagged')
plt.legend(['Original data', 'After running rflag autoflagger'])

# Percent change:
plt.figure()
plt.plot(change*-100, 'b.:')
plt.xlabel('Subband')
plt.ylabel('Percent change in flagged data')

# Initial maxes, post flagging maxes
plt.figure()
plt.plot(imaxs, 'g.:')
plt.plot(fmaxs, 'r.:')
plt.xlabel('Subband')
plt.ylabel('Maximum visibility amp')
plt.legend(['Original data', 'After running rflag'])

# Initial means, post flagging means
plt.figure()
plt.plot(imeans, 'g.:')
plt.plot(fmeans, 'r.:')
plt.xlabel('Subband')
plt.ylabel('Mean visibility amp')
plt.legend(['Original data', 'After running rflag'])


# Initial stdevs, post flagging stdevs
plt.figure()
plt.plot(istdevs, 'g.:')
plt.plot(fstdevs, 'r.:')
plt.xlabel('Subband')
plt.ylabel('Visibility standard dev (sigma)')
plt.legend(['Original data', 'After running rflag'])
