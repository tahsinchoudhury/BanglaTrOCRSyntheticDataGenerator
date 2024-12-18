from extract_from_wikipedia import extract_from_wikipedia
from generate_image import generate_text_image_logic
from bangla_validator import is_bangla
from csv_handler import CSVHandler

def generate_text_image_from_wikipedia():
    with open("wikipedia_dataset.txt", "r") as file:
        line = file.readline()
        generate_text_image_logic(
            text=line,
            font_size=16,
            font_path='bangla_fonts/printed/Nilima.ttf',
            bars=False,
            add_random_text=False,
            add_boxes=False,
            apply_data_augmentation=False,
            output_path="out/images/1.png"
        )

def generate_data():
    # line = ""
    # image_id = 1
    # generate_text_image_logic(
    #     text=line,
    #     font_size=16,
    #     font_path='bangla_fonts/printed/Nilima.ttf',
    #     bars=False,
    #     add_random_text=False,
    #     add_boxes=False,
    #     apply_data_augmentation=False,
    #     output_path=f"out/images/{image_id}.png"
    # )
    with open("wikipedia_dataset.txt", "r") as file:
        image_id = 7437
        for line in file.readlines():
            line = line.strip()
            if is_bangla(line) == False:
                continue
            generate_text_image_logic(
                text=line,
                font_size=16,
                font_path='bangla_fonts/printed/Nilima.ttf',
                bars=False,
                add_random_text=False,
                add_boxes=False,
                apply_data_augmentation=False,
                output_path=f"out/images/{image_id}.png"
            )
            csvHandler = CSVHandler("out/labels/labels.csv")
            csvHandler.insert_data(image_id=image_id, text=line)
            image_id += 1

def test_csv():
    import pandas as pd

    df = pd.read_csv('out/labels/labels.csv')
    print(df.tail())

def test_bangla_validator():
    with open('wikipedia_dataset.txt', 'r') as file:
    # Iterate over each line in the file
        validated_line_count = 0
        processed_lines = 0
        for line in file:
            processed_lines += 1

            if is_bangla(line) == True:
                validated_line_count += 1
                # print("Processed: ", processed_lines, " Validated: ", validated_line_count)
            # else:
                # print("Line ", processed_lines, " Rejected: ", line)
            # Process each line (strip the newline character if needed)
            # print(line.strip())  # Or do any other processing here

if __name__ == '__main__':
    # generate_text_image_from_wikipedia()
    test_csv()

    # generate_data()

    pass