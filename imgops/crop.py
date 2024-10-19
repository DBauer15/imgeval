def crop_img(image, pos, size):
    return image[pos[1]:pos[1]+size[1], pos[0]:pos[0]+size[0], :]


def compute_imageop(imageop, image):
    return crop_img(image, imageop["pos"], imageop["size"])