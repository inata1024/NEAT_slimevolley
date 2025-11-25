"""
Visualize Neural Network Evolution as GIF
Generate an animated GIF showing the evolution of network structures over generations
"""
import os
import glob
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environments
from matplotlib import pyplot as plt
import vis as nv

def visualize_network_evolution(
    networks_dir='log/success3_best',
    output_gif='network_evolution.gif',
    task_name='slimevolley',
    fps=2,
    sample_every=1,
    figsize=(10, 10),
    dpi=100
):
    """
    Create a GIF showing the evolution of neural network structures

    Args:
        networks_dir: Directory containing .out files with network structures
        output_gif: Output GIF filename
        task_name: Task name for the network (e.g., 'slimevolley')
        fps: Frames per second for the GIF
        sample_every: Sample every N networks (1 = all networks, 2 = every other, etc.)
        figsize: Figure size (width, height) in inches
        dpi: Figure resolution
    """

    # Find all .out files in the directory
    network_files = sorted(glob.glob(os.path.join(networks_dir, '*.out')))

    if len(network_files) == 0:
        print(f"No .out files found in {networks_dir}")
        return

    # Sample networks if needed
    network_files = network_files[::sample_every]

    print(f"Found {len(network_files)} network files")
    print(f"Creating GIF with {len(network_files)} frames...")

    # Generate frames
    frames = []
    for i, network_file in enumerate(network_files):
        generation = os.path.basename(network_file).replace('.out', '')
        print(f"Processing {i+1}/{len(network_files)}: Generation {generation}")

        try:
            # Create the figure using viewInd
            fig, ax = nv.viewInd(network_file, task_name)

            # Add generation number as title
            ax.set_title(f'Generation {generation}', fontsize=20, fontweight='bold', pad=20)

            # Convert matplotlib figure to PIL Image
            fig.canvas.draw()

            # Get the RGBA buffer from the figure
            w, h = fig.canvas.get_width_height()
            buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            buf = buf.reshape((h, w, 3))

            # Convert to PIL Image
            img = Image.fromarray(buf)
            frames.append(img)

            # Close the figure to free memory
            plt.close(fig)

        except Exception as e:
            print(f"Error processing {network_file}: {e}")
            continue

    if len(frames) == 0:
        print("No frames were successfully generated")
        return

    # Save as GIF
    duration = int(1000 / fps)  # Duration in milliseconds

    print(f"\nSaving GIF to {output_gif}...")
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0  # 0 means infinite loop
    )

    print(f"Successfully saved {len(frames)} frames to {output_gif}")
    print(f"GIF settings: {fps} fps, {duration}ms per frame")


def create_comparison_gif(
    networks_dir='log/success3_best',
    output_gif='network_evolution_comparison.gif',
    task_name='slimevolley',
    fps=2,
    num_snapshots=10,
    figsize=(12, 10),
    dpi=100
):
    """
    Create a GIF showing evolution with statistics comparison
    Shows network structure alongside generation information

    Args:
        networks_dir: Directory containing .out files
        output_gif: Output GIF filename
        task_name: Task name for the network
        fps: Frames per second
        num_snapshots: Number of evenly-spaced snapshots to include
        figsize: Figure size
        dpi: Resolution
    """

    # Find all .out files
    network_files = sorted(glob.glob(os.path.join(networks_dir, '*.out')))

    if len(network_files) == 0:
        print(f"No .out files found in {networks_dir}")
        return

    # Select evenly-spaced snapshots
    if len(network_files) > num_snapshots:
        indices = np.linspace(0, len(network_files)-1, num_snapshots, dtype=int)
        network_files = [network_files[i] for i in indices]

    print(f"Creating comparison GIF with {len(network_files)} snapshots...")

    frames = []
    for i, network_file in enumerate(network_files):
        generation = os.path.basename(network_file).replace('.out', '')
        print(f"Processing snapshot {i+1}/{len(network_files)}: Generation {generation}")

        try:
            # Load network data
            ind = np.loadtxt(network_file, delimiter=',')
            wMat = ind[:, :-1]
            num_connections = np.sum(wMat != 0)
            num_nodes = wMat.shape[0]

            # Create figure
            fig, ax = nv.viewInd(network_file, task_name)

            # Add detailed title with statistics
            title_text = (f'Generation {generation}\n'
                         f'Nodes: {num_nodes} | Connections: {num_connections}')
            ax.set_title(title_text, fontsize=18, fontweight='bold', pad=20)

            # Convert to PIL Image
            fig.canvas.draw()
            w, h = fig.canvas.get_width_height()
            buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            buf = buf.reshape((h, w, 3))
            img = Image.fromarray(buf)
            frames.append(img)

            plt.close(fig)

        except Exception as e:
            print(f"Error processing {network_file}: {e}")
            continue

    if len(frames) == 0:
        print("No frames were successfully generated")
        return

    # Save as GIF
    duration = int(1000 / fps)

    print(f"\nSaving GIF to {output_gif}...")
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )

    print(f"Successfully saved {len(frames)} frames to {output_gif}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Visualize neural network evolution as GIF')
    parser.add_argument('-d', '--dir', type=str, default='log/success4_best',
                      help='Directory containing network .out files')
    parser.add_argument('-o', '--output', type=str, default='network_evolution.gif',
                      help='Output GIF filename')
    parser.add_argument('-t', '--task', type=str, default='slimevolley',
                      help='Task name (e.g., slimevolley, swingup)')
    parser.add_argument('--fps', type=int, default=2,
                      help='Frames per second for the GIF')
    parser.add_argument('--sample', type=int, default=1,
                      help='Sample every N networks (1=all, 2=every other, etc.)')
    parser.add_argument('--comparison', action='store_true',
                      help='Create comparison GIF with statistics')
    parser.add_argument('--snapshots', type=int, default=10,
                      help='Number of snapshots for comparison mode')

    args = parser.parse_args()

    if args.comparison:
        create_comparison_gif(
            networks_dir=args.dir,
            output_gif=args.output,
            task_name=args.task,
            fps=args.fps,
            num_snapshots=args.snapshots
        )
    else:
        visualize_network_evolution(
            networks_dir=args.dir,
            output_gif=args.output,
            task_name=args.task,
            fps=args.fps,
            sample_every=args.sample
        )
