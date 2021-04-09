# Project ATLAS Beacon Detectoin Platform

import pyb, sensor, image, time, math, ustruct, mjpeg


# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track pink, lime, and yellow.
# At the moment, the thresholds are very wide and should rarely require adjusmtent.
thresholds = [(0, 100, 40, 80, -20, 20),
              (0, 100, -80, -40, 20, 60),
              (0, 100, -40, 20, 30, 70)]
# Pink: (0, 100, 40, 80, -20, 20)
# Orange: (0, 100, 40, 80, 40, 80)
# Green: (0, 100, -80, -40, 20, 60)
# Blue/Purple: (0, 100, 20, 60, -80, -40)
# Yellow: (0, 100, -20, 20, 30, 70)

# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.

uart = pyb.UART(3, 57600, timeout_char=1000)                         # init with given baudrate
uart.init(57600, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False, gain_db=7.5) # must be turned off for color tracking
sensor.set_auto_whitebal(False, rgb_gain_db=(-6.02073, -4.64378, -4.878651)) # must be turned off for color tracking
clock = time.clock()
# rgb_gain_db=(-5.753914, -6.02073, -6.02073)
# Initializing onboard LED. For testing purposes only.

red_led = pyb.LED(1)
green_led = pyb.LED(2)
blue_led = pyb.LED(3)

# Initialize for recording purposes

#m = mjpeg.Mjpeg('Makerspace_Test2.mjpeg')
#i=0 # The loop needs to iterate for a certain number of frames if recording

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. Don't set "merge=True" becuase that will merge blobs which we don't want here.

# Set loop time in while args for recording
while(True):
    clock.tick()
    img = sensor.snapshot()
    color = 0;
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=50):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        #if blob.elongation() > 0.5:
            #img.draw_edges(blob.min_corners(), color=(255,0,0))
            #img.draw_line(blob.major_axis_line(), color=(0,255,0))
            #img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        # img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

        cx = blob.cx()
        cy = blob.cy()
        #desiredx = 160
        #desiredy = 120
        #yaw = 1 # 0: Left ; 1: No move ; 2: Right
        #pitch = 1 # 0: Down ; 1: No Move ; 2: Up

        #if cx < desiredx:
            #yaw = 0
        #if cx > desiredx:
            #yaw = 2
        #if cx < 170 and cx > 150:
            #yaw = 1

        #if cy < desiredy:
            #pitch = 0
        #if cy > desiredy:
            #pitch = 2
        #if cy < 130 and cy > 110:
            #pitch = 1

        # no color 0
        # pink 1
        # orange 2
        # lime 3

        if blob.code() == 1:
            red_led.on()
            color = 1;
        else:
            red_led.off()
        if blob.code() == 2:
            green_led.on()
            color = 2;
        else:
            green_led.off()
        if blob.code() == 4:
            blue_led.on()
            color = 3;
        else:
            blue_led.off()
    if color == 0:
        #yaw = 1;
        #pitch = 1;
        cx = 0;
        cy = 0;
        red_led.off()
        green_led.off()
        blue_led.off()

    uart.write("<")
    uart.write("%d"%color)
    uart.write(",")
    uart.write("%d"%cx)
    uart.write(",")
    uart.write("%d"%cy)
    uart.write(">")

    # These print statements allow for the calibration of the exposure and rgb gains
    #print(sensor.get_exposure_us())
    #print(sensor.get_rgb_gain_db())
    print("<",color," ,", cx," ,",cy,">")

    # For recording purposes only

    #m.add_frame(sensor.snapshot())
    #i = i+1


# For recording purposes only

# m.close(clock.fps())
# blue_led.on()
