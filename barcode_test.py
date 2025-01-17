def input_barcode():
    # Ask the user to manually input a barcode number
    barcode = input("Please enter the barcode: ")

    # Display the entered barcode
    print(f"Barcode entered: {barcode}")

    # Process the barcode (checking length for 12-digit barcode)
    if len(barcode) == 12 and barcode.isdigit():
        print(f"Valid barcode: {barcode}")
        # Add code here to fetch and display the macronutrient info using the barcode
    else:
        print("Invalid barcode. Please enter a 12-digit barcode.")

if __name__ == "__main__":
    input_barcode()
