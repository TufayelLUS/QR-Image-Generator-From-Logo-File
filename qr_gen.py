import qrcode
from PIL import Image, ImageDraw

def generate_colorful_circular_qr_full_bg(data, bg_path, output_path, box_size=20, border=4):
    """
    data       : URL or text
    bg_path    : Background image path
    output_path: Where to save final QR
    box_size   : Size of each QR dot
    border     : Number of QR modules as border
    """
    # Load background image
    bg_img = Image.open(bg_path).convert("RGBA")
    
    # Generate QR matrix without extra border
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,  # we handle scaling manually
        border=0     # no extra border
    )
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    qr_matrix_size = len(matrix)  # size without border

    # Total QR size including custom border
    total_size = (qr_matrix_size + 2 * border) * box_size

    # Resize background to match total QR size
    bg_resized = bg_img.resize((total_size, total_size), Image.LANCZOS)
    bg_pixels = bg_resized.load()

    # Create QR layer with white background
    qr_img = Image.new("RGBA", (total_size, total_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(qr_img)

    # Draw circular dots with border offset
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                px = (x + border) * box_size + box_size // 2
                py = (y + border) * box_size + box_size // 2
                color = bg_pixels[px, py][:3]  # sample background color
                top_left = ((x + border) * box_size, (y + border) * box_size)
                bottom_right = ((x + border + 1) * box_size, (y + border + 1) * box_size)
                draw.ellipse([top_left, bottom_right], fill=color)

    # Composite QR over background
    final_img = Image.alpha_composite(bg_resized, qr_img)
    final_img.save(output_path)
    print("QR Code Image generated")

if __name__ == "__main__":
    # Example usage
    generate_colorful_circular_qr_full_bg(
        data="https://example.com",
        bg_path="f.png",
        output_path="ff.png",
        box_size=20,
        border=2)
