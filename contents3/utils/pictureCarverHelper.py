import re # regular expressions
import zlib # compression
import cv2

faces_directory = "/Users/evega/Pictures/faces"

def get_http_headers(http_payload):
    try:
        # split the headers off if it's http traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]

        # break out the headers
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers


def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if "image" in headers['Content-Type']:
            # grab the image type and image body
            image_type = headers['Content-Type'].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n")+4]

            # if we detect compression decompress the image
            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None

    return image, image_type


# using opence-python bindings
def face_detect(path, file_name):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    # highlight the faces in the image
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img,(x1,y1), (x2,y2), (127,255,0),2)

    cv2.imwrite("%s/%s" % (faces_directory, file_name), img)

    return True

'''
@Chris Fidao 
http://www.fideloper.com/facial-detection/
'''