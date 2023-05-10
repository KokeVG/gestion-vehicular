import requests
import json
import cv2

class Camara:

    def __init__(self, camara):
        self.camara = camara
    
    def ingreso(patente):
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        form_data = json.dumps({'patente': patente, 'tipo':'ingreso'})
        resp = requests.post('http://localhost:8000/api/ingresossalidas/', data=form_data, headers=newHeaders)
        print(resp.status_code)
        if resp.status_code == 200:
            x = resp.json()
            print(x["message"])

    def salida(patente):
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        form_data = json.dumps({'patente': patente, 'tipo':'salida'})
        resp = requests.post('http://localhost:8000/api/ingresossalidas/', data=form_data, headers=newHeaders)
        print(resp.status_code)
        if resp.status_code == 200:
            x = resp.json()
            print(x["message"])


cam1 = cv2.VideoCapture('rtsp://sc-2019w:2108@192.168.1.153:8554/profile1')
cam2 = cv2.VideoCapture('rtsp://sc-2019w:2108@192.168.1.153:8554/profile1')
cam3 = cv2.VideoCapture('rtsp://sc-2019w:2108@192.168.1.153:8554/profile1')

ingreso = Camara(cam1)
salida = Camara(cam2)
estacionamiento1 = Camara(cam3)


cv2.namedWindow("Camara")
while True:
    ret, frame = ingreso.camara.read()
    cv2.imshow("Camara", frame)
    if cv2.waitKey(50) >= 0:
        break