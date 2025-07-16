from PIL import Image


def merge_tiff_files(image_paths, output_path, direction="vertical"):
    """
    Concatenate multiple images into a single image, either vertically or horizontally.

    Args:
        image_paths (list): List of paths to the input images
        output_path (str): Path where the concatenated image will be saved
        direction (str): 'vertical' or 'horizontal'

    Returns:
        str: Path to the output image
    """
    # Open all images
    images = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            # Convert to RGB if needed (to ensure compatibility)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            images.append(img)
            print(f"Loaded image: {img_path}, size: {img.size}")
        except Exception as e:
            print(f"Error loading {img_path}: {e}")

    if not images:
        raise ValueError("No images could be loaded")

    # Determine total size
    if direction == "vertical":
        # All images will have the width of the widest image
        width = max(img.width for img in images)
        height = sum(img.height for img in images)
    else:  # horizontal
        # All images will have the height of the tallest image
        width = sum(img.width for img in images)
        height = max(img.height for img in images)

    # Create a new blank image
    combined_image = Image.new("RGB", (width, height))

    # Paste images into the combined image
    y_offset = 0
    x_offset = 0

    for img in images:
        if direction == "vertical":
            # Center horizontally if narrower than the widest image
            x_pos = (width - img.width) // 2
            combined_image.paste(img, (x_pos, y_offset))
            y_offset += img.height
        else:  # horizontal
            # Center vertically if shorter than the tallest image
            y_pos = (height - img.height) // 2
            combined_image.paste(img, (x_offset, y_pos))
            x_offset += img.width

    # Save the combined image
    combined_image.save(output_path)
    print(f"Successfully created combined image: {output_path}")
    return output_path


# Example usage
if __name__ == "__main__":
    input_files = ["A0000001.tiff", "A0000002.tiff"]
    output_file = "merged_output.tiff"
    merge_tiff_files(input_files, "merged_output.tiff", direction="vertical")