PRPA_Practica2
Synchronized crossing of a bridge by pedestrians and cars heading both directions using a monitor.

El pueblo de Ambite (https://es.wikipedia.org/wiki/Ambite) tiene un puente que
atraviesa el río Tajuña. Es un puente compartido por peatones y vehículos. La anchura del
puente no permite el paso de vehículos en ambos sentidos (Observa la figura 1.). Por motivos
de seguridad los peatones y los vehículos no pueden compartir el puente. En el caso de los
peatones, sí que que pueden pasar peatones en sentido contrario.
Desarrolla en papel el cliente y los el monitor (o monitores) necesarios. Parte de una
solución sencilla que cumpla la seguridad y a partir de ella intenta buscar soluciones a
los problema de inanición.
• Escribe el invariante del monitor.
• Demuestra que el puente es seguro (no hay coches y peatones a la vez en el puente,
no hay coches en sentidos opuestos)
• Demuestra la ausencia de deadlocks
• Demuestra la ausencia de inanición.
Implementa una solución en python con la biblioteca multiprocessing.

La primera solución a este ejericicio la hice sin usar la plantilla, solo teniendo como referencia los scripts vistos en clase sobre filosofos, lectores, etc... (Esta solución se encunetra en FernandezdelAmoP_PRPAPractica2.pdf y en FernandezdelAmoP_Practica2Ianicion.pdf.

Los scripts restantes son la solución a esta práctica utilizando la plantilla dada (skel.py)
