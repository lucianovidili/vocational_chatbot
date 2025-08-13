# Header Image Instructions

## Adding the Header Image

To add the header image to your vocational orientation chatbot:

1. **Replace the placeholder file**: Delete the `header-image.jpg` placeholder file and replace it with your actual image file.

2. **Image specifications**:
   - **File name**: `header-image.jpg` (or update the template to match your filename)
   - **Format**: JPG, PNG, or WebP recommended
   - **Recommended dimensions**: 1200x300 pixels or similar aspect ratio
   - **File size**: Keep under 500KB for optimal loading

3. **Image content**: The image should be the one described with:
   - Four young people using smartphones outdoors
   - "Orientación Vocacional" text overlay
   - Insight logo (yellow circle with white text)
   - Bright, vibrant outdoor setting

4. **Template integration**: The image is already integrated into the template and will:
   - Scale to fill the full width of the screen
   - Maintain aspect ratio
   - Be responsive on mobile devices
   - Have a maximum height of 300px on desktop, 200px on mobile

## File Structure
```
chatbot/static/chatbot/images/
├── header-image.jpg  <- Replace this with your actual image
└── README.md         <- This file
```

## Testing
After adding the image, restart your Django development server and visit the chatbot page to see the header image in action.

