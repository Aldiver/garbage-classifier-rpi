import usb.core
import usb.util
import time

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS
USB_VENDOR  = 0xffff # Vendor-ID:
USB_PRODUCT = 0x0035 # Product-ID

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
    dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

receivedNumber = 0

while True:
    control = None

    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)

        if control[0] == 2:
            # Convert ascii to a number, there's probably better ways to do so.
            receivedDigit = control[2] - 29

            if receivedDigit == 10:
                receivedDigit = 0

            # Append the digit to the number
            receivedNumber = 10 * receivedNumber + receivedDigit

        # Check if the received character is CRLF
        if (( control[0] == 0 )) & (( control[2] == 40 )) & (( not receivedNumber == 0 )):
            print("card: " + str(receivedNumber))
            time.sleep(1)

            print
            receivedNumber = 0
    except KeyboardInterrupt:
        print("Interrupted")
    except:
        pass

    time.sleep(0.001) # Let CTRL+C actually exit
