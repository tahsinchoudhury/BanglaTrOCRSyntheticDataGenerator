import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import string
import numpy as np
import click
import os
from augmentation import data_transformer

from bidi.algorithm import get_display

# all_characters = string.ascii_letters + string.digits + string.punctuation + " " + ''.join([chr(i) for i in range(192, 256)])  # Latin-1 Supplement (includes accents)

# Adding Bangla characters
bangla_characters = ''.join([chr(i) for i in range(0x0980, 0x09FF + 1)])

# Combine with other character sets as needed
all_characters = string.punctuation + " " + bangla_characters


@click.command()
@click.option('--text', help='Text to be generated in the image')
@click.option('--font_size', default=48, help='Font size for the text')
@click.option('--font_path', default="", help='Path to the font file (empty for random font)')
@click.option('--bars', default=True, type=click.BOOL, help='List of bars to be added to the image')
@click.option('--add_random_text', default=True, type=click.BOOL, help='Add random text to the image')
@click.option('--add_boxes', default=True, type=click.BOOL, help='Add boxes to the image')
@click.option('--apply_data_augmentation', default=True, type=click.BOOL, help='Apply data augmentation to the image')
@click.option('--output_path', default="generated_image.png", help='Output path of the generated image')
def generate_text_image(text, font_size, font_path, bars, add_random_text, add_boxes, apply_data_augmentation, output_path):
    image = Image.new("RGB", (1000, 1000), "white")  
    draw = ImageDraw.Draw(image)

    print(f"Provided text: {text}")
    text = get_display(text)
    
    if font_path == "":
        base_fonts_dir = 'bangla_fonts'
        font_type = np.random.choice(["hw", "printed"])
        font_name = np.random.choice(os.listdir(f"{base_fonts_dir}/{font_type}/"))
        font_path = os.path.join(base_fonts_dir, font_type, font_name)
        
    font = ImageFont.truetype(font_path, size=font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    if add_boxes:
        tol = random.randint(10, 15) / 10
        character_width, character_height = np.mean([draw.textsize(c, font) for c in text], axis=0).astype(int)
        image = Image.new("RGB", (int(tol * character_width * len(text)), character_height), "white")
    else:
        image = Image.new("RGB", (text_width, text_height), "white")
    
    padding = tuple(random.randint(5, 20) for _ in range(4))
    image = ImageOps.expand(image, padding, fill="white")
    draw = ImageDraw.Draw(image)
    
    if bars:
        for _ in range(random.randint(3, 6)):
            bar_x = random.randint(0, image.size[0] - 1)
            draw.line([(bar_x, 0), (bar_x, image.size[1])], fill=tuple([np.random.randint(0, 100)] * 3), width=random.randint(1, 3))
     
        for _ in range(random.randint(1, 3)):
            bar_y = random.randint(0, image.size[1] - 1)
            draw.line([(0, bar_y), (image.size[0], bar_y)], fill=tuple([np.random.randint(0, 100)] * 3), width=random.randint(1, 3))

    if add_random_text:
        random_text = ''.join(random.choice(all_characters) for _ in range(len(text)))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (random.randint(-50, 50), image.size[1] - random.randint(5, 15) if padding[1] <= padding[3] else -text_height + random.randint(5, 15) ), 
            random_text, 
            font=font, 
            fill= tuple([np.random.randint(0, 100)] * 3),
        )
        
    if add_boxes:
        color = tuple([np.random.randint(0, 100)] * 3)
        text_color = tuple([np.random.randint(0, 100)] * 3)
        width = random.randint(1,3)
        for i in range(len(text)):
            draw.line([(padding[0] + i*tol * character_width, padding[1]), (padding[0] + i*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.line([(padding[0] + i*tol * character_width, padding[1] + tol * character_width), (padding[0] + (i+1)*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.line([(padding[0] + (i+1)*tol * character_width, padding[1]), (padding[0] + (i+1)*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.text(
                (padding[0] + i*tol * character_width + ((tol-1) * character_width) // 2 + random.randint(-2,2), padding[1] + tol * character_width -  character_height  + random.randint(-2,2)), 
                text[i], 
                font=font, 
                fill= text_color,
            )  
    else:
        draw.text(
            (padding[0],padding[1]), 
            text, 
            font=font, 
            fill= tuple([np.random.randint(0, 100)] * 3),
        )

    # draw.text(
    #     (padding[0],padding[1]), 
    #     text, 
    #     font=font, 
    #     fill= tuple([np.random.randint(0, 100)] * 3),
    # )
    
    if apply_data_augmentation:
        image = data_transformer(image)
    image.save(output_path)
    return

def generate_text_image_logic(text, font_size, font_path, bars, add_random_text, add_boxes, apply_data_augmentation, output_path):
    image = Image.new("RGB", (1000, 1000), "white")  
    draw = ImageDraw.Draw(image)

    print(f"Provided text: {text}")
    text = get_display(text)
    
    if font_path == "":
        base_fonts_dir = 'bangla_fonts'
        font_type = np.random.choice(["hw", "printed"])
        font_name = np.random.choice(os.listdir(f"{base_fonts_dir}/{font_type}/"))
        font_path = os.path.join(base_fonts_dir, font_type, font_name)
        
    font = ImageFont.truetype(font_path, size=font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    if add_boxes:
        tol = random.randint(10, 15) / 10
        character_width, character_height = np.mean([draw.textsize(c, font) for c in text], axis=0).astype(int)
        image = Image.new("RGB", (int(tol * character_width * len(text)), character_height), "white")
    else:
        image = Image.new("RGB", (text_width, text_height), "white")
    
    padding = tuple(random.randint(5, 20) for _ in range(4))
    image = ImageOps.expand(image, padding, fill="white")
    draw = ImageDraw.Draw(image)
    
    if bars:
        for _ in range(random.randint(3, 6)):
            bar_x = random.randint(0, image.size[0] - 1)
            draw.line([(bar_x, 0), (bar_x, image.size[1])], fill=tuple([np.random.randint(0, 100)] * 3), width=random.randint(1, 3))
     
        for _ in range(random.randint(1, 3)):
            bar_y = random.randint(0, image.size[1] - 1)
            draw.line([(0, bar_y), (image.size[0], bar_y)], fill=tuple([np.random.randint(0, 100)] * 3), width=random.randint(1, 3))

    if add_random_text:
        random_text = ''.join(random.choice(all_characters) for _ in range(len(text)))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (random.randint(-50, 50), image.size[1] - random.randint(5, 15) if padding[1] <= padding[3] else -text_height + random.randint(5, 15) ), 
            random_text, 
            font=font, 
            fill= tuple([np.random.randint(0, 100)] * 3),
        )
        
    if add_boxes:
        color = tuple([np.random.randint(0, 100)] * 3)
        text_color = tuple([np.random.randint(0, 100)] * 3)
        width = random.randint(1,3)
        for i in range(len(text)):
            draw.line([(padding[0] + i*tol * character_width, padding[1]), (padding[0] + i*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.line([(padding[0] + i*tol * character_width, padding[1] + tol * character_width), (padding[0] + (i+1)*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.line([(padding[0] + (i+1)*tol * character_width, padding[1]), (padding[0] + (i+1)*tol * character_width, padding[1] + tol * character_width)], fill=color, width=width)
            draw.text(
                (padding[0] + i*tol * character_width + ((tol-1) * character_width) // 2 + random.randint(-2,2), padding[1] + tol * character_width -  character_height  + random.randint(-2,2)), 
                text[i], 
                font=font, 
                fill= text_color,
            )  
    else:
        draw.text(
            (padding[0],padding[1]), 
            text, 
            font=font, 
            fill= tuple([np.random.randint(0, 100)] * 3),
        )

    # draw.text(
    #     (padding[0],padding[1]), 
    #     text, 
    #     font=font, 
    #     fill= tuple([np.random.randint(0, 100)] * 3),
    # )
    
    if apply_data_augmentation:
        image = data_transformer(image)
    image.save(output_path)
    return


if __name__ == '__main__':
    generate_text_image()