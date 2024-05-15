import cv2 as cv
from preprocessor import ImagePreprocessor


def main():
    # Read the video from the file
    cap = cv.VideoCapture('1.mp4')
    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

            
        segmentor = ImagePreprocessor()
        processed_frame = segmentor.binarizeImage(frame)

        # Display the resulting frame
        cv.imshow("processed frame", processed_frame)

        if cv.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()