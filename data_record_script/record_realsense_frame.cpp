#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include "example.hpp" // Include a short list of convenience functions for rendering

// Create a simple OpenGL window for rendering:
window app(1280, 720, "RealSense Capture Example");
// Declare two textures on the GPU, one for depth and one for color
texture depth_image, color_image;

//Declare depth colorizer for enhanced color visualization of depth data
rs2::colorizer color_map;

// Declare the RealSense pipeline, encapsulating the actual device and sensors
rs2::pipeline pipe;
// Start streaming with the default recommended configuration
pipe.start();

rs2::frameset data = pipe.wait_for_frames(); // Wait for next set of frames from the camera

rs2::frame depth = color_map(data.get_depth_frame()); // Find and colorize the depth data
rs2::frame color = data.get_color_frame();            // Find the color data

// Render depth on to the first half of the screen and color on to the second
depth_image.render(depth, { 0,               0, app.width() / 2, app.height() });
color_image.render(color, { app.width() / 2, 0, app.width() / 2, app.height() });
