import os
import sys
import io
import click
from PIL import Image

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the ImageProcessor
from library.image_processor import ImageProcessor

# Create the processor instance
processor = ImageProcessor()


@click.group()
def cli():
    """Background Removal CLI tool.

    This tool allows you to remove backgrounds from images using the rembg library.
    """


@cli.command("remove")
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), required=False)
@click.option(
    "--format",
    "-f",
    "output_format",
    default="PNG",
    type=click.Choice(["PNG", "JPEG", "png", "jpeg"]),
    help="Output image format (PNG or JPEG)",
)
@click.option(
    "--bg-color",
    "-c",
    type=(int, int, int),
    default=None,
    help="Replace transparent background with color as RGB values (e.g., 255 0 0 for red)",
)
def remove_background(input_path, output_path, output_format, bg_color):
    """Remove background from an image and save the result.

    INPUT_PATH: Path to the input image

    OUTPUT_PATH: Path where the processed image will be saved (optional)
                 If not provided, output will be saved as "[original]_output.[format]"
    """
    output_format = output_format.upper()

    # Generate output path if not provided
    if not output_path:
        input_dir = os.path.dirname(input_path)
        input_filename = os.path.basename(input_path)
        name, _ = os.path.splitext(input_filename)
        suffix = "_replaced" if bg_color else "_output"
        output_path = os.path.join(input_dir, f"{name}{suffix}.{output_format.lower()}")

    click.echo(f"Processing image: {input_path}")
    click.echo(f"Output format: {output_format}")
    if bg_color:
        click.echo(f"Background color: RGB{bg_color}")
    click.echo(f"Output will be saved to: {output_path}")

    try:
        # Read the image file
        with open(input_path, "rb") as f:
            image_bytes = f.read()

        with click.progressbar(length=2, label="Removing background") as bar:
            # Process image
            if bg_color:
                result, _ = processor.replace_background(
                    image_bytes, background_color=bg_color
                )
                if output_format != "PNG":
                    img = Image.open(io.BytesIO(result))
                    output_bytes = io.BytesIO()
                    img.save(output_bytes, format=output_format)
                    output_bytes.seek(0)
                    result = output_bytes.getvalue()
            else:
                result, _ = processor.process_and_convert(
                    image_bytes, output_format=output_format
                )
            bar.update(1)

            # Save the result
            output = Image.open(io.BytesIO(result))
            output.save(output_path)
            bar.update(1)

        click.secho("✓ Successfully processed image!", fg="green")
        click.echo(f"Output saved to: {os.path.abspath(output_path)}")

    except (IOError, OSError) as e:
        click.secho(f"✗ Error processing image: {str(e)}", fg="red")
        sys.exit(1)


@cli.command("info")
def show_info():
    """Display information about the background removal tool."""
    click.echo("Background Removal Tool")
    click.echo("----------------------")
    click.echo("This tool uses the rembg library to remove backgrounds from images.")
    click.echo("Supported output formats: PNG, JPEG")
    click.echo("\nExample usage:")
    click.echo("  python cli.py remove input.jpg output.png --format PNG")


# Add batch processing command
@cli.command("batch")
@click.argument(
    "input_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument(
    "output_dir", type=click.Path(file_okay=False, dir_okay=True), required=False
)
@click.option(
    "--format",
    "-f",
    "output_format",
    default="PNG",
    type=click.Choice(["PNG", "JPEG", "png", "jpeg"]),
    help="Output image format (PNG or JPEG)",
)
@click.option(
    "--recursive/--no-recursive",
    default=False,
    help="Process subdirectories recursively",
)
@click.option(
    "--bg-color",
    "-c",
    type=(int, int, int),
    default=None,
    help="Replace transparent background with color as RGB values (e.g., 255 0 0 for red)",
)
def batch_process(input_dir, output_dir, output_format, recursive, bg_color):
    """Process all images in a directory.

    INPUT_DIR: Directory containing images to process

    OUTPUT_DIR: Directory where processed images will be saved (optional)
                If not provided, output will be saved to "[input_dir]_output"
    """
    output_format = output_format.upper()

    # Generate output directory if not provided
    if not output_dir:
        # Get input directory name
        input_dir_path = os.path.abspath(input_dir)
        input_dir_name = os.path.basename(input_dir_path.rstrip(os.path.sep))
        parent_dir = os.path.dirname(input_dir_path)

        # Create output directory name by appending "_output"
        suffix = "_replaced" if bg_color else "_output"
        output_dir = os.path.join(parent_dir, f"{input_dir_name}{suffix}")

    click.echo(f"Processing images from: {input_dir}")
    click.echo(f"Output format: {output_format}")
    if bg_color:
        click.echo(f"Background color: RGB{bg_color}")
    click.echo(f"Output will be saved to: {output_dir}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        click.echo(f"Created output directory: {output_dir}")

    # Get all image files
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    image_files = []

    if recursive:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(input_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(input_dir, file))

    if not image_files:
        click.secho("No image files found!", fg="yellow")
        return

    click.echo(f"Found {len(image_files)} images to process")

    # Process each image
    success_count = 0
    error_count = 0

    with click.progressbar(image_files, label="Processing images") as bar:
        for image_path in bar:
            try:
                # Determine output path
                rel_path = os.path.relpath(image_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)

                # Change extension based on format
                output_path = (
                    os.path.splitext(output_path)[0] + f".{output_format.lower()}"
                )

                # Create subdirectories if needed
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Read the image file
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                # Process image based on whether bg_color is provided
                if bg_color:
                    result, _ = processor.replace_background(
                        image_bytes, background_color=bg_color
                    )
                    if output_format != "PNG":
                        img = Image.open(io.BytesIO(result))
                        output_bytes = io.BytesIO()
                        img.save(output_bytes, format=output_format)
                        output_bytes.seek(0)
                        result = output_bytes.getvalue()
                else:
                    result, _ = processor.process_and_convert(
                        image_bytes, output_format=output_format
                    )

                # Save the result
                output = Image.open(io.BytesIO(result))
                output.save(output_path)

                success_count += 1

            except (IOError, OSError, ValueError) as _:
                error_count += 1
                # Optionally log the error for debugging
                # print(f"Error processing {image_path}: {str(error)}")

    # Show summary
    click.echo("\nBatch processing complete:")
    click.secho(f"✓ Successfully processed: {success_count} images", fg="green")
    if error_count > 0:
        click.secho(f"✗ Failed to process: {error_count} images", fg="red")
    click.echo(f"Output saved to: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    cli()
