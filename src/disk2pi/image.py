from PIL import Image
import os



def decoupage ():
    return



def conversion () :
    return


def compression(input_path,output_path,quality=1,format=None) :

    img=Image.open(input_path)

    save_format=format or os.path.splitext(output_path)[1][1:].upper()
    if save_format == "JPG":
        save_format = "JPEG"
    save_kwargs = {"optimize": True}
    
    if save_format == "JPEG":
        save_kwargs["quality"] = quality
    elif save_format == "WEBP":
        save_kwargs["quality"] = quality
    elif save_format == "PNG":
        save_kwargs["compress_level"] = 9

    img.save(output_path, format=save_format, **save_kwargs)

    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    ratio = (1 - compressed_size / original_size) * 100

    print(f"Original  : {original_size / 1024:.1f} KB")
    print(f"Compressé : {compressed_size / 1024:.1f} KB")
    print(f"Réduction : {ratio:.1f}%")

    return compressed_size




# Compression simple
compression("image_test.jpg", "photo_compressed.jpg")
