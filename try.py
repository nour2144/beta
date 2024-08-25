# import socket
# from kivy.lang import Builder
# from kivymd.app import MDApp
#
# KV = '''
# Screen:
#     MDRaisedButton:
#         text: "Send Data"
#         pos_hint: {"center_x": 0.5, "center_y": 0.5}
#         on_release: app.send_data_to_esp8266()
# '''
#
#
# class MainApp(MDApp):
#     def build(self):
#         # try:
#         #     host = "192.168.4.1"  # ESP8266 AP IP address
#         #     port = 80  # ESP8266 Port
#         #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         #     # Connect to the server
#         #     client_socket.connect((host, port))
#         #     response = client_socket.recv(1024)
#         #     print(f"Received from ESP8266: {response.decode()}")
#         # except:
#         #     pass
#         return Builder.load_string(KV)
#
#     def send_data_to_esp8266(self):
#         host = "192.168.4.1"  # ESP8266 AP IP address
#         port = 80  # ESP8266 Port
#         try:
#             # Create a socket object
#             client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             # Connect to the server
#             client_socket.connect((host, port))
#             # Send data
#             client_socket.sendall(b"a1\n")
#
#             # Wait for a response
#             response = client_socket.recv(1024)
#             print(f"Received from ESP8266: {response.decode()}")
#
#             # Close the connection
#             client_socket.close()
#             print("Data sent successfully")
#         except Exception as e:
#             print(f"Failed to send data: {e}")
#
#
# if __name__ == "__main__":
#     MainApp().run()
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivymd.uix.screen import Screen
# from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.dialog import MDDialog
# import requests
#
# KV = '''
# Screen:
#     BoxLayout:
#         orientation: 'vertical'
#         padding: dp(10)
#         spacing: dp(10)
#
#         MDTextField:
#             id: ip_address
#             hint_text: "Enter ESP8266 IP Address"
#             size_hint_x: None
#             width: dp(300)
#             pos_hint: {'center_x': 0.5}
#
#         MDRaisedButton:
#             text: "Turn Relay ON"
#             pos_hint: {'center_x': 0.5}
#             on_release: app.send_command("Relay1ON")
#
#         MDRaisedButton:
#             text: "Turn Relay OFF"
#             pos_hint: {'center_x': 0.5}
#             on_release: app.send_command("Relay1OFF")
# '''
#
# class ESP8266App(MDApp):
#     def build(self):
#         self.screen = Builder.load_string(KV)
#         return self.screen
#
#     def send_command(self, command):
#         ip_address = self.screen.ids.ip_address.text
#         url = f"http://{ip_address}/{command}"
#
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 self.show_dialog(f"Success: {response.text}")
#             else:
#                 self.show_dialog(f"Failed: {response.status_code}")
#         except requests.exceptions.RequestException as e:
#             self.show_dialog(f"Error: {str(e)}")
#
#     def show_dialog(self, message):
#         dialog = MDDialog(title="Response", text=message, size_hint=(0.8, 1))
#         dialog.open()
#
# if __name__ == "__main__":
#     ESP8266App().run()
#
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import easyocr
import cv2
import numpy as np
import streamlit as st
from PIL import Image


def numbers(text):
    try:
        price = text.replace(" ", '').replace(',', '.').replace('$', "")
        count = price.count('.')
        for i in range(count - 1):
            price = price.replace('.', '', 1)
        price = float(price)
        number.append(price)
    except:
        pass


number = []
points = []

image = st.file_uploader('Upload an image', type=['png', 'jpg'])
if image:
    image = Image.open(image)  # Open the image using PIL
    image = np.array(image)  # Convert the image to a NumPy array

    reader = easyocr.Reader(['en'])
    results = reader.readtext(image, width_ths=0.5)

    # Print the extracted text
    for result in results:
        bounding_box, text, confidence = result
        numbers(text)
        pts = [tuple(pt) for pt in bounding_box]
        pts = np.array(pts, dtype=np.int32)
        points.append(pts)

    st.write(f"Maximum number found: {max(number)}")

    image_with_boxes = cv2.polylines(image.copy(), points, isClosed=True, color=(0, 255, 0), thickness=2)
    st.image(image_with_boxes, caption="Image with detected text")
# from google.cloud import vision
# import io
#
# def detect_text(image_path):
#     """Detects text in the file."""
#     client = vision.ImageAnnotatorClient()
#
#     with io.open(image_path, 'rb') as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#
#     if response.error.message:
#         raise Exception(
#             f'{response.error.message}'
#         )
#
#     return texts[0].description if texts else ""
#
# # Example usage
# text = detect_text('image.png')
# print("Extracted Text:\n", text)
