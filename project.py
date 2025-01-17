#asource my_env/bin/activate
 

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from pyzbar.pyzbar import decode
import cv2
import requests
from kivy.core.window import Window

class MacronutrientTrackerApp(App):
    def build(self):
        # Set window title and background color
        Window.title = "Macronutrient Tracker"
        Window.clearcolor = (1, 1, 1, 1)  # White background

        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Add a logo or image at the top
        logo = Image(source='ricekrispies.png', size_hint_y=None, height=100)
        main_layout.add_widget(logo)

        # Create a title label
        title_label = Label(text="Macronutrient Tracker", font_size='24', bold=True)
        main_layout.add_widget(title_label)

        #sub-layout for barcode input and scan button
        input_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.barcode_input = TextInput(hint_text="Enter barcode or scan", multiline=False)
        self.scan_button = Button(text="Scan Barcode", on_press=self.start_scanning,
                                  background_color=(0, 0.5, 0, 1),  # Dark green
                                  color=(1, 1, 1, 1),  # White text
                                  size_hint_x=0.3)
        input_layout.add_widget(self.barcode_input)
        input_layout.add_widget(self.scan_button)
        main_layout.add_widget(input_layout)

        #label for displaying food info
        self.food_info_label = Label(text="", font_size='18')
        main_layout.add_widget(self.food_info_label)

        return main_layout

    def start_scanning(self, instance):
        print("Starting barcode scan...")
        self.food_info_label.text = "Scanning... Press 'q' to exit."
        self._capture_and_scan()

    def _capture_and_scan(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to access the camera.")
            self.food_info_label.text = "Error: Unable to access the camera."
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Decode barcodes in the frame
            decoded_objects = decode(frame)

            for obj in decoded_objects:
                barcode_data = obj.data.decode('utf-8')
                barcode_type = obj.type  # Identify the type of barcode
                print(f"Decoded Barcode: {barcode_data}, Type: {barcode_type}")

                # Displaying the detected barcode and type on the UI
                Clock.schedule_once(lambda dt: self.update_food_info(f"Scanned: {barcode_data}\nType: {barcode_type}"))

                # Use the barcode for further processing (fetch macronutrient data)
                self.get_macronutrients(barcode_data)

                # Stopping scanning once a barcode is detected
                cap.release()
                cv2.destroyAllWindows()
                return

            # Display the frame for debugging
            cv2.imshow('Barcode Scanner', frame)

            # Exit if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def update_food_info(self, text):
        self.food_info_label.text = text

    def get_macronutrients(self, barcode):
        if not barcode:
            print("Invalid barcode, skipping API request.")
            self.food_info_label.text = "Invalid barcode."
            return

        # API request to get food info using the scanned barcode
        API_KEY = '27420f6a219b93aada8ff0d82588b295' 
        APP_ID = 'd22234145'  
        API_URL = f'https://api.nutritionix.com/v1_1/item?upc={barcode}&appId={APP_ID}&appKey={API_KEY}'

        try:
            response = requests.get(API_URL, timeout=5)  # Added a timeout for the request
            response.raise_for_status()  # Raisedd an exception for bad status codes

            data = response.json()

            if 'item_name' in data:
                # Extracting macronutrient data from the response
                food_name = data['item_name']
                food_macros = (
                    data.get('nf_total_carbohydrate', 0),
                    data.get('nf_protein', 0),
                    data.get('nf_total_fat', 0),
                )

                # Preparing the info to display
                food_info = (f"Food: {food_name}\n"
                             f"Carbs: {food_macros[0]}g\n"
                             f"Protein: {food_macros[1]}g\n"
                             f"Fat: {food_macros[2]}g")
                # Updating the label with food info
                Clock.schedule_once(lambda dt: self.update_food_info(food_info))
            else:
                print("Food data not found.")
                self.food_info_label.text = "Food data not found. Try again."

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectTimeout):
                print(f"Request timed out: {e}")
                self.food_info_label.text = "Request timed out. Please try again."
            elif isinstance(e, requests.exceptions.ConnectionError):
                print(f"Connection error: {e}")
                self.food_info_label.text = "Connection error. Please try again."
            else:
                print(f"Request error: {e}")
                self.food_info_label.text = "Error retrieving data. Please try again."

if __name__ == '__main__':
    MacronutrientTrackerApp().run()
    