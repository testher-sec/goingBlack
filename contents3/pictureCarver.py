from scapy.all import rdpcap
from scapy.layers.inet import TCP

from utils.pictureCarverHelper import get_http_headers, extract_image, face_detect

pictures_directory = "/Users/evega/Pictures/"
pcap_file = "bhp.pcap"

def http_assembler(pcap_file):
    carved_images = 0
    faces_detected = 0

    # we open the pcap file for processing with scapy function
    a = rdpcap(pcap_file)

    # separate each TCP session into a dictionary
    sessions = a.sessions()

    # filter out only HTTP traffic and concatenate its payload
    for session in sessions:
        http_payload = ""

        # This is as right clicking in Wireshark and selecting Follow TCP Stream
        for packet in sessions[session]: # sessions is a dictionary
            try:
                # find destination or source port 80
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reassemble the stream
                    http_payload += str(packet[TCP].payload)
            except:
                pass

        headers = get_http_headers(http_payload)
        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)
        if image is not None and image_type is not None:
            # store the image
            file_name = "%s-pic_carver_%d.$s" % (pcap_file, carved_images, image_type)
            fd = open("%s/$s" % (pictures_directory, file_name), "wb")
            fd.write(image)
            fd.close()

            carved_images += 1;

            # now attempt face detection
            try:
                result = face_detect("%s/%s" % (pictures_directory, file_name), file_name)

                if result is True:
                    faces_detected += 1
            except:
                pass

    return carved_images, faces_detected


carved_images, faces_detected = http_assembler(pcap_file)

print "Extracted: %d images" % carved_images
print "Detected: %d faces" % faces_detected

'''
Watch it, to use cv2 ....!!!
kali> apt-get install python-opencv python-numpy python-scipy
'''
