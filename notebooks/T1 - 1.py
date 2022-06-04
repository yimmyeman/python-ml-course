# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:17:04 2022

@author: yimmy
"""

def downloadFromURL(url, filename, sep = ",", delim = "\n", encoding="utf-8", 
                   mainpath = "/Users/yimmy/Desktop/python-ml-course/datasets"):
    #primero importamos la librería y hacemos la conexión con la web de los datos
    import pandas as pd
    import os
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print("El estado de la respuesta es %d" %(r.status))
    response = r.data ## CORREGIDO: eliminado un doble decode que daba error
    
    #El objeto reponse contiene un string binario, así que lo convertimos a un string descodificándolo en UTF-8
    str_data = response.decode(encoding)

    #Dividimos el string en un array de filas, separándolo por intros
    lines = str_data.split(delim)

    #La primera línea contiene la cabecera, así que la extraemos
    col_names = lines[0].split(sep)
    n_cols = len(col_names)

    #Generamos un diccionario vacío donde irá la información procesada desde la URL externa
    counter = 0
    main_dict = {}
    for col in col_names:
        main_dict[col] = []

    #Procesamos fila a fila la información para ir rellenando el diccionario con los datos como hicimos antes
    for line in lines:
        #Nos saltamos la primera línea que es la que contiene la cabecera y ya tenemos procesada
        if(counter > 0):
            #Dividimos cada string por las comas como elemento separador
            values = line.strip().split(sep)
            #Añadimos cada valor a su respectiva columna del diccionario
            for i in range(len(col_names)):
                main_dict[col_names[i]].append(values[i])
        counter += 1

    print("El data set tiene %d filas y %d columnas"%(counter-1, n_cols))

    #Convertimos el diccionario procesado a Data Frame y comprobamos que los datos son correctos
    df = pd.DataFrame(main_dict)
    print(df.head())

    #Elegimos donde guardarlo (en la carpeta athletes es donde tiene más sentido por el contexto del análisis)
    fullpath = os.path.join(mainpath, filename)

    #Lo guardamos en CSV, en JSON o en Excel según queramos
    df.to_csv(fullpath+".csv")
    df.to_json(fullpath+".json")
    df.to_excel(fullpath+".xls")
    print("Los ficheros se han guardado correctamente en: "+fullpath)
    
    return df

df = downloadFromURL("http://winterolympicsmedals.com/medals.csv", "athletes/downloaded_medals")
