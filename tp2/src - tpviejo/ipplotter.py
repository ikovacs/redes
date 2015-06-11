#! /usr/bin/python

from iplocator import *
import numpy as np
import matplotlib.pyplot as plt

file_base = 'traceroutes/'

def trace_teorico(pais):

	rtt_empirico = {
		'rusia' : 134.8101,
		'canada': 113.0214,
		'china' : 185.1104
	}

	hora = []
	times = []
	cota = [rtt_empirico[pais] for i in range(0,19)]

	for i in range(0,19):

		f = file_base + str(i) + "_" + pais + ".txt"
		l = IPLocator( f )

		hora.append(i+1)

		last_hop = int(l.hops.keys()[-1])
		times.append(float(l.hops[last_hop]['time']))

	plt.plot(hora, times, hora, cota)

	plt.xlabel('hs')
	plt.ylabel('rtt')
	plt.legend(['traceroute','rtt'])
	plt.show()

def rtt_promedio_dia(pais, salto):
	hs = range(0,20)

	experimentos = [IPLocator(file_base+str(i)+'_'+pais+'.txt') for i in hs ]
	
	i = 0
	intervalos = []
	while i < len(hs):
		intervalos.append( (i,i+int(salto)) )
		i += int(salto)

	legends = []
	for i in intervalos:
		first = i[0]
		last = i[1]

		legends.append( str(first+1) + ' hs a ' + str(last+1) + ' hs' )
		experimentos_f_l = experimentos[first:last]
		cant_exp = len(experimentos_f_l)

		#print str(first) + '->' + str(last) + '(' + str(cant_exp) + ' experimentos)'

		#print experimentos_f_l

		hops_f_l = []
		media_time_f_l = []

		#print hops_f_l
		#print media_time_f_l

		for iplocator in experimentos_f_l:
			#print iplocator
			for hop in iplocator.hops:
				#print iplocator.hops[hop]
				if hop > len(media_time_f_l):
					hops_f_l.append( hop )
					media_time_f_l.append( iplocator.hops[hop]['time'] / cant_exp )
				else:
					media_time_f_l[hop-1]+=iplocator.hops[hop]['time'] / cant_exp
		
		#print hops_f_l
		#print media_time_f_l

		plt.plot(hops_f_l, media_time_f_l)

	plt.xlabel('hops')
	plt.ylabel('media rtt')
	plt.legend(legends,loc=2)
	plt.show()

def show_help():
	print "Se pueden llamar a dos funciones (escribiendolas como primer parametro): \n"
	print "\ta) rtt_promedio_dia: grafica los rtt promedios en cada intervalo de tiempo de x horas, usando los archivos de la carpeta ./traceroute"
	print "\t\t necesita dos parametros: pais (china, rusia, canada) y el intervalo de horas (entero > 0)"
	print "\t\t ejemplo de uso: ./ipploter.py rtt_promedio_dia china 5\n"
	print "\tb) trace_teorico: grafica el rtt empirico tomado de los archivos ./traceroute y lo compara con el rtt teorico."
	print "\t\t necesita un solo pais (china, rusia, canada)"
	print "\t\t ejemplo de uso: ./ipploter.py trace_teorico rusia"

def main(params):

	if( params[0] == 'rtt_promedio_dia' and len(params) == 3):
		rtt_promedio_dia(params[1], params[2])
	else if( params[0] == 'trace_teorico' and len(params) == 2 ):
		trace_teorico(params[1])
	else:
		show_help()

if __name__ == "__main__":
	if( len(sys.argv) == 1 ):
		show_help()
	else:
		main(sys.argv[1:])