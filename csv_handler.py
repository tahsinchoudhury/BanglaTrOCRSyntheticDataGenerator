import csv
import os

class CSVHandler:
    def __init__(self, filename):
        self.filename = filename
        # Create the CSV file with headers if it does not exist
        self.create_csv()

    # Method to create a new CSV file with headers if not already created
    def create_csv(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Add headers: Image ID and Text
                writer.writerow(['image_id', 'text'])
            print(f"File '{self.filename}' created with headers.")
        else:
            print(f"File '{self.filename}' already exists.")

    # Method to insert data (image ID and text) into the CSV file
    def insert_data(self, image_id, text):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([image_id, text])
        print(f"Data inserted: image_id={image_id}, text={text}")

    # Method to view all data in the CSV file
    def view_data(self):
        if not os.path.exists(self.filename):
            print(f"File '{self.filename}' does not exist.")
            return
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

# Example usage
if __name__ == "__main__":
    # Instantiate the MLDataCSV class with the filename
    ml_csv = CSVHandler("out/labels/labels.csv")

    # Insert some sample data
    ml_csv.insert_data("img_001", "This is the first image description.")
    ml_csv.insert_data("img_002", "This is the second image description.")
    ml_csv.insert_data("img_003", "A description for the third image.")

    # View the data in the CSV file
    print("\nViewing Data in the CSV File:")
    ml_csv.view_data()
