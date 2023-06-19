import tkinter as tk
import cv2
from PIL import ImageTk, Image
from newWindow import NewWindow
import threading
import multiprocessing


# class to create graphical user-interface module for visualization of simulations
class VideoPlayer:

    nw = None

    # initialization function
    def __init__(self, root):
        self.root = root
        self.video_path = "media/earth_video.mp4"  # Replace with the path to your MP4 video file
        
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)  # Fill the entire frame with the video
        
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire canvas with the video
        
        self.video_thread = threading.Thread(target=self.play_video())
        self.video_thread.daemon = True  # Set the thread as a daemon thread to automatically terminate it on program exit
        
        
    # start video thread
    def start(self):
        self.video_thread.start()  # Start the video playback thread
        

    # render video for main screen
    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        
        # Get the dimensions of the video
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Set the initial size of the window to match the video dimensions
        self.root.geometry(f"{width}x{height}")
        
        # Get the original video's frame rate
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        # Calculate the desired frame delay to achieve half the original speed
        frame_delay = int(1000 / (original_fps / 2))
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img = img.resize((width, height))  # Resize the image to match the video dimensions
            
            self.canvas.image = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)
            
            self.root.update_idletasks()
            self.root.update()
            
            # Delay the frame to achieve the desired speed
            self.root.after(frame_delay)
        
        cap.release()


    # start the simulation and open new window on unique process
    def start_simulation():
        global nw
        nw = multiprocessing.Process(target=NewWindow.main()) #.main() to invoke cooperative coevolution
        nw.start()


    # end the simulation and return to the main window
    def stop_simulation():
        global nw
        if nw and nw.is_alive(): # only works if there is a running instance of multiprocessing available
            nw.terminate()
            nw.join()
        else:
            print("no nw")
            
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cellular Intelligence Simulation")

    # Create a frame for the video and buttons with a black background
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(fill=tk.BOTH)

    # Create a frame for the buttons with a black background
    button_frame = tk.Frame(main_frame, bg="black")
    button_frame.pack(side=tk.BOTTOM, pady=10)

    # Configure the style for the buttons
    button_style = {
        "background": "#76B900",
        "foreground": "white",
        "borderwidth": 0,
        "highlightthickness": 0,
        "font": ("Arial", 12, "bold")
    }

    # Create the "Start Simulation" button
    start_button = tk.Button(button_frame, text="Start Simulation", command=VideoPlayer.start_simulation, **button_style)
    start_button.pack(side=tk.LEFT, padx=10)

    # Create the "End Simulation" button
    end_button = tk.Button(button_frame, text="End Simulation",command=VideoPlayer.stop_simulation, **button_style)
    end_button.pack(side=tk.LEFT, padx=10)

    # Create the "Exit" button
    exit_button = tk.Button(button_frame, text="Exit", **button_style, command=root.destroy)
    exit_button.pack(side=tk.LEFT, padx=10)
    
    
    player = VideoPlayer(root)
    player.start()
    
    root.mainloop()