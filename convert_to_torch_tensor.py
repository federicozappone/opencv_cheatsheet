import cv2
import numpy as np


image = cv2.imread("test_image.jpg")

# convert to tensor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
half = False # model supports half precision

image = image[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
image = np.ascontiguousarray(image)

# to tensor
image = torch.from_numpy(image).to(device)
image = image.half() if half else image.float()  # uint8 to fp16/32
image /= 255.0  # 0 - 255 to 0.0 - 1.0

if image.ndimension() == 3:
    image = image.unsqueeze(0)

# convert back to image

result = result.permute(0, 2, 3, 1).cpu().data.numpy()
result = np.minimum(np.maximum(result, 0), 1)
result = (255 * result[0, :, :, :]).astype("uint8")
