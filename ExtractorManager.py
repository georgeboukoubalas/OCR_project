def preprocessing(img):
    import numpy as np
    import cv2

    # Convert PIL to NumPy
    img_np = np.array(img)

    # Convert to grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Resize (optional but helps OCR if text is too small)
    height, width = gray.shape
    if width < 1000:
        scale = 2
        gray = cv2.resize(gray, (width * scale, height * scale), interpolation=cv2.INTER_LINEAR)

    # Denoise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Otsu thresholding
    _, bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optional: Morphology (closing small holes)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Optional: Deskew image
    coords = np.column_stack(np.where(morph == 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = morph.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(morph, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return deskewed


def postprocessing(text):
    from spellchecker import SpellChecker
    import re
    # 1. Remove weird symbols & extra spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces

    # 2. Optional: Fix spelling
    spell = SpellChecker()
    words = text.split()
    corrected_words = [spell.correction(word) or word for word in words]

    text = ' '.join(corrected_words)

    # 3. Remove super short lines that are likely garbage
    lines = text.split('\n')
    lines = [line for line in lines if len(line.strip()) > 2]
    text = "\n".join(lines)

    return text


def cleaning_text(text: str) -> str:
    import re
    """
    Cleans the input text by normalizing newlines, removing long lines of symbols or non-alphanumerics,
    repeated garbage sequences, fixing common OCR errors, cleaning extra whitespace, and stripping leading/trailing whitespace.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """

    # Normalize newlines first
    text = re.sub(r"\r\n|\r", "\n", text)

    # Remove long lines of symbols or non-alphanumerics (fake dividers, OCR junk)
    text = re.sub(r"^[\W_]+|[\W_]+$", "", text, flags=re.MULTILINE) #removes lines containing non-alphanumeric character

    # Remove repeated garbage sequences (e.g. "οοοοοο", "τττττ", etc.)
    text = re.sub(r"([^\W\d_])\1{3,}", r"\1", text)

    # Fix common OCR errors
    text = text.replace("|||", " | ")
    text = text.replace("||", " | ")
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    text = text.replace(" :", ":")
    text = text.replace(" ;", ";")
    text = text.replace("..", ".")
    text = text.replace("`", "'")
    text = text.replace("´", "'")

    # Clean extra whitespace
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

def crop_to_roi(img):
    import cv2
    import numpy as np

    # Convert PIL to NumPy if needed
    if not isinstance(img, np.ndarray):
        img = np.array(img)

    img_copy = img.copy()

    # Convert to grayscale if colored
    if len(img_copy.shape) == 3:
        gray = cv2.cvtColor(img_copy, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_copy

    # Threshold to get text as white on black
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find external contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return img_copy  # No contours = return original image

    # Get bounding box of all text
    x, y, w, h = cv2.boundingRect(np.concatenate(contours))

    # Add some padding around text
    pad = 10
    x = max(x - pad, 0)
    y = max(y - pad, 0)
    w = min(w + 2 * pad, img.shape[1] - x)
    h = min(h + 2 * pad, img.shape[0] - y)

    roi = img[y:y + h, x:x + w]
    return roi





