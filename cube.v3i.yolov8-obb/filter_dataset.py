import os

# Sadece bu classlar kalsın (cube olanlar)
KEEP_CLASSES = [0, 2, 4]  # bluecube, greencube, redcube

def process_labels(label_path):
    with open(label_path, "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])

        if class_id in KEEP_CLASSES:
            # tüm cube classlarını tek class yap (0)
            parts[0] = "0"
            new_lines.append(" ".join(parts))

    # Dosyayı tekrar yaz
    with open(label_path, "w") as f:
        f.write("\n".join(new_lines))

def process_folder(base_path):
    for root, dirs, files in os.walk(base_path):
        if "labels" in root:
            for file in files:
                if file.endswith(".txt"):
                    process_labels(os.path.join(root, file))

# Dataset klasör yolu
dataset_path = "cube-udoei"  # klasör adını buraya yaz

process_folder(dataset_path)

print("Bitti 🚀")