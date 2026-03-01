import os
import random
import shutil

source_dir = "dataset"
target_dir = "dataset_split" 

splits = ["train", "val", "test"]

for split in splits:
    for cls in os.listdir(source_dir):
        os.makedirs(os.path.join(target_dir, split, cls), exist_ok=True)

for cls in os.listdir(source_dir):
    images = os.listdir(os.path.join(source_dir, cls))
    random.shuffle(images)

    train_size = int(0.7 * len(images))
    val_size = int(0.15 * len(images))

    train_images = images[:train_size]
    val_images = images[train_size:train_size + val_size]
    test_images = images[train_size + val_size:]

    for img in train_images:
        shutil.copy(
            os.path.join(source_dir, cls, img),
            os.path.join(target_dir, "train", cls, img)
        )

    for img in val_images:
        shutil.copy(
            os.path.join(source_dir, cls, img),
            os.path.join(target_dir, "val", cls, img)
        )

    for img in test_images:
        shutil.copy(
            os.path.join(source_dir, cls, img),
            os.path.join(target_dir, "test", cls, img)
        )

print("Dataset successfully split!")