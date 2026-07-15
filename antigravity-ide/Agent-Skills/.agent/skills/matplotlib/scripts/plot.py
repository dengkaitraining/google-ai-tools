#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt

def plot_sine_cosine(output_path: str, title: str, xlabel: str, ylabel: str) -> None:
    # Set premium style aesthetics
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    # Generate data
    x = np.linspace(0, 2 * np.pi, 1000)
    y_sin = np.sin(x)
    y_cos = np.cos(x)
    
    # Plot lines with premium colors and styles
    ax.plot(x, y_sin, label='Sine', color='#1a73e8', linewidth=2.5, linestyle='-')
    ax.plot(x, y_cos, label='Cosine', color='#e8710a', linewidth=2.5, linestyle='--')
    
    # Customizations
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color='#202124')
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10, color='#202124')
    ax.set_ylabel(ylabel, fontsize=12, labelpad=10, color='#202124')
    
    # Grid customization
    ax.grid(True, linestyle=':', alpha=0.6, color='#dadce0')
    
    # Border removal (top and right)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
        
    # Legend custom styling
    ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#dadce0', fontsize=11, loc='upper right')
    
    # Layout adjustments
    plt.tight_layout()
    
    # Save the file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated Sine vs Cosine plot and saved to '{output_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Matplotlib Plotting CLI for Antigravity Skill")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # sine-cosine plot command
    parser_sc = subparsers.add_parser("sine-cosine", help="Generate Sine and Cosine comparison plot")
    parser_sc.add_argument("--output", "-o", default="plot.png", help="Path to save the generated PNG plot")
    parser_sc.add_argument("--title", default="Sine vs Cosine Wave Comparison", help="Plot Title")
    parser_sc.add_argument("--xlabel", default="Angle (radians)", help="X-axis label")
    parser_sc.add_argument("--ylabel", default="Amplitude", help="Y-axis label")
    
    args = parser.parse_args()
    
    if args.command == "sine-cosine":
        plot_sine_cosine(args.output, args.title, args.xlabel, args.ylabel)

if __name__ == "__main__":
    main()
