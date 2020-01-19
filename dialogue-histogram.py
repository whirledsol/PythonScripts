#!/usr/bin/env python3
"""
dialogue-histogram.py
Created: 20190118
@author: Will Rhodes

"""
import pysrt
import seaborn 
import numpy
import math
import matplotlib.pyplot as pyplot

def start():
	filename = 'assets/2001.srt'
	title = '"2001: A Space Odyssey" Dialogue'
	binsize = 1
	tickspacing = 5
	duration = 142
	bins = parse(filename,binsize,duration)
	graph(bins,title,tickspacing)
	

def parse(filename,binsize,duration):
	subs = pysrt.open(filename)
	sample = [x.text for x in subs[:-50]]
	print('SAMPLE')
	print(sample)

	timestamps = [x.start.ordinal/1000/60 for x in subs]
	mx = int(math.ceil(max(timestamps))) if duration is None else duration
	binsize = int(mx/binsize)
	return numpy.histogram(timestamps,binsize,range=(0,mx))


def graph(bins,title,tickspacing):
	x = bins[1][:-1]
	y = bins[0]
	ticks = numpy.arange(max(x),step=tickspacing)
	palette = seaborn.dark_palette("red")
	ax = seaborn.barplot(x,y,palette=palette)
	ax.set_xticks(ticks)
	ax.set_xticklabels([int(x) for x in ticks])
	ax.set_xlabel('Time (minutes)')
	ax.set_ylabel('Lines')
	ax.set_title(title)
	pyplot.show()
if  __name__ =='__main__': start()
