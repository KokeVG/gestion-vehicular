import PySimpleGUI as sg
import cv2
from sys import exit as exit
from datetime import datetime
# Librería para contar elementos de una lista
from collections import Counter

# Librería que transforma imagen en texto
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

CAM = 'rtsp://sc-2019w:2108@192.168.1.153:8554/profile1'
#CAM = 0


# Funciones

def leerPlaca(foto):
    patente = None
    contornos, imagen, gray = buscarContornos(foto)
    contorno = filtarContornos(contornos, imagen, gray)
    patente = identificarTexto(contorno)

    return patente

def buscarContornos(foto):
    imagen = cv2.imread(foto) #640x360
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))
    canny = cv2.Canny(imagen,150,200)
    canny = cv2.dilate(canny,None,iterations=1)
    #_,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contornos,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imagen,contornos,-1,(0,255,0),2)
    #cv2.imwrite('Grises.png',canny)
    #print(len(cnts))
    return contornos, imagen, gray

def filtarContornos(contornos, imagen, gray):
    placa= None
    resultado = None
    for c in contornos:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        # Para que el area de la placa sea la misma o aproximada, los vehículo debe estar a la misma distancia de la toma, se considerara 1 metro.
        if area>1000:
            #print('area=',area)
            cv2.drawContours(imagen,[approx],0,(0,255,0),3)
            aspect_ratio = float(w)/h # 360/130 que son las dimensiones de la placa en mm.
            #print('aspect ratio: ', aspect_ratio)
            if aspect_ratio>2.5:#2.5
                placa = gray[y:y+h,x:x+w]
                texto = pytesseract.image_to_string(placa,config='--psm 11')
                texto = ''.join(char for char in texto if char.isalnum())
                # Obtener el contorno que de un texto que tenga 5 o 6 caracteres de largo (Motos o autos)
                if len(texto) == 5 or len(texto) == 6:
                    if texto.isupper(): # Verifica si esta en mayuscula lo detectado
                        resultado = texto
    return resultado

def identificarTexto(resultado):
    if resultado is None:
        return "No hay patente detectada"
    elif len(resultado) == 0:
        resultado = "No hay patente detectada"
    return resultado

def filtrarResultados(resultados):
    aux = Counter(resultados)
    return max(aux, key=aux.get)

def obtenerFechaHora():
    aux = datetime.now()
    fecha = str(formato(aux.day)) + "/" + str(formato(aux.month)) + "/" + str(formato(aux.year))
    hora = str(formato(aux.hour)) + ":" + str(formato(aux.minute)) + ":" + str(formato(aux.second))
    return fecha + " a las " + hora

def formato(num):
    if num < 10:
        num = '0' + str(num)
    return num

def crearVentana():
    sg.ChangeLookAndFeel('SystemDefault') # Color de la ventana
    # Vista de la ventana
    layout = [[sg.Text('Detector de patentes vehiculares', size=(40, 1), justification='center', font='Helvetica 20')],
            [sg.Image(filename='', key='image')], # Cámara
            [sg.Button('Leer patente', size=(10, 1), font='Helvetica 14'), # Botón Leer patente
            sg.Button('Salir', size=(10, 1), font='Helvetica 14')]] # Botón Salir
    # Crear ventana
    window = sg.Window('Detector de patentes vehiculares', layout,
                    location=(400,200), resizable = True)
    return window

if __name__ == '__main__':
    ventana = crearVentana()
    
    cap = cv2.VideoCapture(CAM) # Asignar que cámara usar

    if cap.isOpened():
        # Bucle infinito en busca de patentes vehiculares
        while True:
            # Obtiene el evento, en este caso el botón Salir
            event, values = ventana.Read(timeout=20)
            if event == 'Salir' or event is None:
                break
            elif event == 'Leer patente':
                # Se tomarán capturas, en cada captura se detectara si hay patente o no
                resultados = []
                for i in range(1):
                    ret, frame = cap.read()            
                    imgbytes=cv2.imencode('.png', frame)[1].tobytes()
                    ventana['image'].Update(data=imgbytes)

                    foto="temp.jpg"
                    cv2.imwrite(foto,frame)
                    resultado=leerPlaca(foto)
                    resultados.append(resultado)
                
                placa = filtrarResultados(resultados)
                #print(resultados)
                print(placa)
                print(obtenerFechaHora())

            # Usa la cámara en la ventana
            ret, frame = cap.read()            
            imgbytes=cv2.imencode('.png', frame)[1].tobytes()
            ventana['image'].Update(data=imgbytes)
        
        ventana.close() #cerrar todo
        exit()
    else:
        print("Cámara desconectada")



