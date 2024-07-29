# Generative Adversarial Network (GAN)

## Terms
- **Gen**: Generator
- **Disc**: Discriminator
- **Z**: Latent Space Representation

## Methodology
- 3k images are generally used.
- The 'Gen' is run once and the 'Disc' is run twice. Literature suggests that running the 'Disc' more times than the 'Gen' yields state-of-the-art performance.
- The 'Disc' tries to maximize its loss, whereas the 'Gen' tries to minimize its loss.
- The generator uses an Encoder-Decoder architecture:
  - The generator takes a grayscale image and generates a latent representation 'Z'.
  - The decoder's job is to produce a colorful image by enlarging the "Z".

## U-Net Architecture
- Used to segment objects from images.
- The images contain objects such as temples, people, birds, flags, etc.
- Designed for semantic segmentation.
- Two kinds of segmentation:
  - Instance
  - Semantic

## DeOldify Model

[Understanding GANs with DeOldify](https://medium.com/@rohanricky/understanding-gans-with-deoldify-ddaccd684daf)

### Variants
- **Artistic**: Focused on colorful colorizations rather than spatial stability.
- **Video**: Focused on spatial and temporal stability.
- **Stable**: Focused only on spatial stability, yielding more colorful colorizations than the 'video' version but less than the 'artistic' version.

### Network Architecture
![Network_Architecture_image](./images/architecture.png)
- It uses a U-net Architecture
- U-Net architecture is used for the colorizer network.
- The U-Net architecture encoding part is made from pre-trained ResNet because:
  - It provides strong feature extraction and compact abstract representation.
  - The Artistic Color Variant model specially use resNet34 while others use resNet101 , due to computational capacity
- The U-Net architecture decoding part uses the abstract representation from encoder resNet34 
    - to reconstruct the final output image. It applies up-sampling and convolution operations to gradually rebuild the image, adding color information and refining details to produce a colorized version
- As we can see the:
    - Red part in architecture is : ResNet34
    - Blue part is Convolution layer
    - Green part is Upsampling layer
    - Orange part is self-attention layer
    - at Last pink is sigmoid layer
    - the black lines are skip connectuin which are commin in U-Net architecture.
