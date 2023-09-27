import cv2
import numpy as np

x, y, contours = 0, 0, 0
# Mendapatkan citra dari sumber video atau webcam
cap = cv2.VideoCapture(0)

# Beri nama window dan atur pada ukuran 800 x 600 piksel
cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Webcam", 800, 600)
min_contour = 500
jml_contour = 0
while True:
    # Baca frame dari video
    ret, frame = cap.read()

    # Putar frame secara horizontal
    flipped_frame = cv2.flip(frame, 1)

    # Konversi citra ke model warna HSV
    hsv = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2HSV)

    # Tentukan rentang warna yang ingin dideteksi dalam HSV berdasarkan praktikum labsheet 1
    lower_range = np.array([40, 50, 50])
    upper_range = np.array([80, 255, 255])

    # Buat mask untuk area yang sesuai dengan rentang warna
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Lakukan operasi morfologi pada mask
    kernel = np.ones((5, 5), np.uint8)
    color = cv2.dilate(mask, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Temukan kontur objek yang terdeteksi
    contours, _ = cv2.findContours(color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if c > min_contour:
            cv2.putText(
                flipped_frame,
                str(len(c)),
                (240, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

    # Buat teks 'Koordinat X: ' dan 'Koordinat Y: ' pada window
    cv2.putText(
        flipped_frame,
        "Koordinat X:",
        (0, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        flipped_frame,
        "Koordinat Y:",
        (0, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        flipped_frame,
        str(int(x)),
        (200, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        flipped_frame,
        str(int(y)),
        (200, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        flipped_frame,
        "Jumlah Warna:",
        (0, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    # Loop melalui setiap kontur
    for contour in contours:
        # Dapatkan lingkaran terkecil yang mengelilingi kontur
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Buat teks yang berisi nilai koordinat (x, y) pada window
        cv2.putText(
            flipped_frame,
            str(int(x)),
            (200, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            flipped_frame,
            str(int(y)),
            (200, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

        # Gambar lingkaran pada citra
        cv2.circle(flipped_frame, center, radius, (0, 255, 0), 2)

    # Tampilkan citra dan mask
    cv2.imshow("Webcam", flipped_frame)

    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Tutup video capture dan jendela tampilan
cap.release()
cv2.destroyAllWindows()
