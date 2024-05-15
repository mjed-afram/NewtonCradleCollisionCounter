import cv2 as cv
from preprocessor import FramePreprocessor
from tracker import Tracker
from counter import CollisionCounter


def main():

    # Read the video from the file
    cap = cv.VideoCapture('data-mp4/9.mp4')
    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
    
    # Create an instance of the CollisionCounter class for counting collisions
    collision_counter = CollisionCounter()

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

            
        hsvSegment = FramePreprocessor.HSVsegment(frame)
        processed_frame = FramePreprocessor.binarizeImage(hsvSegment)
        filledGaps = FramePreprocessor.fillGaps(processed_frame)
        frame_, box_positions = Tracker.extractCoordinates(filledGaps)

        
        count = collision_counter.countCollisions(frame_, box_positions)

        # Display the resulting frame
        cv.putText(frame, f"Total Collisions: {count}", (180, 300), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.putText(frame_, f"Total Collisions: {count}", (180, 300), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.imshow("Result", frame)
        cv.imshow("Original frame", frame_)

        if cv.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()