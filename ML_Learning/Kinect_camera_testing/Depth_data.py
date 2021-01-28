import _thread
import pygame
from _pykinect.pykinect import nui

DEPTH_WINSIZE = 640, 480

screen_lock = _thread.allocate()
screen = None
tmp_s = pygame.Surface(DEPTH_WINSIZE, 0, 16)

def depth_frame_ready(frame):
    with screen_lock:
        frame.image.copy_bits(tmp_s._pixels_address)
        arr2d = (pygame.surfarray.pixels2d(tmp_s) >> 7)&255
        pygame.surfarray.blit_array(screen, arr2d)

        pygame.display.update()

def main():
    pygame.init()

    global screen
    screen = pygame.display.set_mode(DEPTH_WINSIZE, 0, 8)
    screen.set_palette(tuple([(i, i, i) for i in range(256)]))
    pygame.display.set_caption('PyKinect Depth Map Example')

    with nui.Runtime() as kinect:
        kinect.depth_frame_ready += depth_frame_ready
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)

        # Main game loop
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                break
if __name__ == '__main__':
    main()