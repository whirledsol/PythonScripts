#!/usr/bin/env python3
"""
dialogue-histogram.py
Created: 20190118
@author: Will Rhodes

"""
import os,pysrt,seaborn,numpy,math
import matplotlib.pyplot as plt



def start():
	directory = 'assets/atla_s03/'
	title = 'Avatar Season 3 Dialogue'
	color='red'
	binsize = 1
	tickspacing = 5

	files = os.listdir(directory)
	files.sort()

	rows = 3 if len(files) % 3 == 0 else 2
	cols = int(math.ceil(len(files)/rows))
	
	print(f"About to graph subplots ({rows},{cols})")
	fig, axs = plt.subplots(rows, cols)
	axs = flatten(axs)
	for i,ax in enumerate(axs):
		if(i<len(files)):
			filename = files[i]
			filename = os.path.join(directory,filename)
			subtitle = os.path.basename(filename)

			#custom
			subtitle = subtitle.split('-')[-1].split('.')[0].strip()

			bins = parse(filename,binsize)
			graph_subplot(ax,bins,tickspacing,color,subtitle)
		else:
			ax.axis('off')
	fig.suptitle(title)
	plt.subplots_adjust(left=.02, top=.85, right=.98, bottom=.04)
	plt.show()

def parse(filename,binsize,duration=None):
	'''
	parse the srt
	'''
	subs = pysrt.open(filename, encoding='iso-8859-1')
	sample = [x.text for x in subs[:-50]]
	#print('SAMPLE')
	#print(sample)

	timestamps = [x.start.ordinal/1000/60 for x in subs]
	mx = int(math.ceil(max(timestamps))) if duration is None else duration
	binsize = int(mx/binsize)
	return numpy.histogram(timestamps,binsize,range=(0,mx))

def graph_subplot(ax, bins,tickspacing, color='red', subtitle=None):
	'''
	graphs the data for the current plot
	'''
	x = bins[1][:-1]
	y = bins[0]
	ticks = numpy.arange(max(x),step=tickspacing)
	palette = seaborn.dark_palette(color)
	seaborn.barplot(x,y,ax=ax,palette=palette)
	ax.set_xticks(ticks)
	
	#custom: no values
	ax.set_yticklabels([])
	ax.set_xticklabels([])
	#ax.set_xticklabels([int(x) for x in ticks])

	if subtitle is not None:
		ax.set_title(subtitle, fontsize=6)

def flatten(l): return [item for sublist in l for item in sublist]

if  __name__ =='__main__': start()
