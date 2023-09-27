import cv2
import numpy as np
import tkinter as tk

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Buat jendela Tkinter
jendela = tk.Tk()
jendela.title("Deteksi Warna")

# Baca frame pertama dari webcam
ret, frame = cap.read()

# Konversi ke ruang warna HSV
citra_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Variabel untuk menyimpan nilai batas HSV
var_min_hue = tk.IntVar()
var_max_hue = tk.IntVar()

var_min_saturation = tk.IntVar()
var_max_saturation = tk.IntVar()

var_min_value = tk.IntVar()
var_max_value = tk.IntVar()

# Label untuk Hue Min
label_min_hue = tk.Label(jendela, text="Hue Min (H)")
label_min_hue.pack()

# Scale untuk Hue Min
skala_min_hue = tk.Scale(
    jendela, from_=0, to=179, orient="horizontal", length=200, variable=var_min_hue
)
skala_min_hue.set(0)
skala_min_hue.pack()

# Label untuk Hue Min
label_max_hue = tk.Label(jendela, text="Hue Max (H)")
label_max_hue.pack()

# Scale untuk Hue Max
skala_max_hue = tk.Scale(
    jendela, from_=0, to=179, orient="horizontal", length=200, variable=var_max_hue
)
skala_max_hue.set(179)
skala_max_hue.pack()

# Label untuk Saturation Min
label_min_saturation = tk.Label(jendela, text="Saturation Min (S)")
label_min_saturation.pack()

# Scale untuk Saturation Min
skala_min_saturation = tk.Scale(
    jendela,
    from_=0,
    to=255,
    orient="horizontal",
    length=200,
    variable=var_min_saturation,
)
skala_min_saturation.set(0)
skala_min_saturation.pack()

# Label untuk Saturation Max
label_max_saturation = tk.Label(jendela, text="Saturation Max (S)")
label_max_saturation.pack()

# Scale untuk Saturation Max
skala_max_saturation = tk.Scale(
    jendela,
    from_=0,
    to=255,
    orient="horizontal",
    length=200,
    variable=var_max_saturation,
)
skala_max_saturation.set(255)
skala_max_saturation.pack()

# Label untuk Value Min
label_min_value = tk.Label(jendela, text="Value Min (V)")
label_min_value.pack()

# Scale untuk Value Min
skala_min_value = tk.Scale(
    jendela, from_=0, to=255, orient="horizontal", length=200, variable=var_min_value
)
skala_min_value.set(0)
skala_min_value.pack()

# Label untuk Value Max
label_max_value = tk.Label(jendela, text="Value Max (V)")
label_max_value.pack()

# Scale untuk Value Max
skala_max_value = tk.Scale(
    jendela, from_=0, to=255, orient="horizontal", length=200, variable=var_max_value
)
skala_max_value.set(255)
skala_max_value.pack()

# Loop utama
while True:
    min_hue = var_min_hue.get()
    max_hue = var_max_hue.get()
    min_saturation = var_min_saturation.get()
    max_saturation = var_max_saturation.get()
    min_value = var_min_value.get()
    max_value = var_max_value.get()

    # Baca frame dari webcam
    ret, frame = cap.read()

    # Konversi ke ruang warna HSV
    citra_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rentang_bawah = np.array([min_hue, min_saturation, min_value])
    rentang_atas = np.array([max_hue, max_saturation, max_value])

    # Buat mask berdasarkan rentang warna HSV
    masker = cv2.inRange(citra_hsv, rentang_bawah, rentang_atas)

    # Aplikasikan mask pada citra asli
    hasil = cv2.bitwise_and(frame, frame, mask=masker)

    # Tampilkan citra hasil deteksi
    cv2.imshow("Deteksi Warna", hasil)

    # Tampilkan frame asli
    cv2.imshow("Webcam", frame)

    # Perbarui jendela Tkinter
    jendela.update()

    # Jika tombol 'q' ditekan, keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Tutup webcam dan jendela OpenCV
cap.release()
cv2.destroyAllWindows()
