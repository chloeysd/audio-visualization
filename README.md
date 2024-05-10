# audio-visualization

# Project Overview
"InkFlow" is a dynamic audio visualization tool inspired by Chinese ink-wash painting techniques. It uses Fast Fourier Transform (FFT) values and user mouse events to generate visual patterns that mimic brush strokes on a canvas. The visuals change in real-time based on the audio input and user interactions, providing a unique experience with each use.

## Features
- **Audio Analysis**: Utilizes a `MusicAnalyser` object to analyze audio files and extract FFT values.
- **Visual Dynamics**: Scales the radius of visual elements dynamically based on FFT values to create effects similar to ink splashes.
- **Interactive Controls**: User mouse clicks change the colors and quantity of visual elements, enhancing the interactivity and creative output of the program.
- **Adaptable Visuals**: The program adjusts the visualization style (dots, lines, or blocks) based on the musical genre being analyzed, reflecting the intensity and rhythm of the music.

## Setup and Initialization
- **Initial Setup**: Calls `setup()` and `start_loop()` functions within the initialization to prepare for loops and mouse events.
- **Visual Elements**: Initializes a list containing 10 balls, each defined by initial positions, speed, direction, and color.

## Technology
- **OpenCV**: Used for drawing each visual element in the window and for continuously updating the display.
- **Optional Backgrounds**: The background of the visualization can be toggled, enhancing the aesthetic appeal.

## Usage
To use "InkFlow", simply load an audio file into the program. The visualization will adjust based on the FFT analysis of the audio:
- **Low-variance Jazz**: Generates dense and continuous lines.
- **Piano Music**: Produces thicker, smooth, and continuous lines, reflecting the flow and harmony typical of piano music.
- **Hip-Hop**: Alternates visualization between dots and lines due to larger rhythm variations.
- **Heavy Metal or EDM**: Transforms visualization into block-like shapes, mirroring the intense rhythm.

## Installation Requirements
Ensure you have the following installed:
- Python 3.x
- OpenCV library
- Any additional libraries required for audio processing and FFT analysis.

## Acknowledgments
This project was developed as part of an academic assignment and draws inspiration from traditional Chinese art forms and modern music analysis techniques.

