import os
import shutil
import cv2

"""
# Rename files and place them into a single directory
image_source_folder = 'image_dir'
label_source_folder = 'annotation_dir'

image_target_folder = 'images'
label_target_folder = 'labels'

count = -1
for subdir, dirs, files in os.walk(image_source_folder):
    if count == -1: 
        count += 1
        continue
    subdir_name = subdir.split('\\')[1]
    for file_name in files:
        with open(f'{image_source_folder}/{subdir_name}/{file_name}') as image_file, \
             open(f'{label_source_folder}/{subdir_name}/{file_name}'.split('.')[0] + '.txt') as label_file:
            shutil.copy2(image_file.name, f'{image_target_folder}/{"%06d" % count}.jpg')
            shutil.copy2(label_file.name, f'{label_target_folder}/{"%06d" % count}.txt')
        # print "%04d" % 1
        count += 1
        print(count)
"""


image_folder = 'images'
label_folder = 'labels'
validation_split = 0.10

# Convert annotations and split into validation and train set
number_images = len(os.listdir(image_folder))
max_samples = 200
train_size = int(max_samples * (1 - validation_split))
val_size = max_samples - train_size

print(f'Training dataset size: {train_size}')
print(f'Validation dataset size: {val_size}')

count = 0
with open('train.txt', 'w') as train_file, open('val.txt', 'w') as val_file:
    for file_name in os.listdir(image_folder):
        if count < train_size:
            file_to_write = train_file
        else:
            file_to_write = val_file
        with open(f'{label_folder}/{file_name}'.split('.')[0] + '.txt') as label_file:
            file_to_write.write(f'{image_folder}/{file_name}')
            for line in label_file:
                line = line.split(' ')
                line[-1] = line[-1].rstrip()

                img = cv2.imread(f'{image_folder}/{file_name}')
                img_height = img.shape[0]
                img_width = img.shape[1]
                
                x = float(line[1]) * img_width
                y = float(line[2]) * img_height
                w = float(line[3]) * img_width
                h = float(line[4]) * img_height

                xmin = x - w/2
                ymin = y - h/2
                xmax = x + w/2
                ymax = y + h/2

                """
                x1 = float(line[1]) * img_width
                y1 = float(line[2]) * img_height
                x2 = x1 + float(line[3]) * img_width
                y2 = y1 + float(line[4]) * img_height
                """
                file_to_write.write(f' {xmin},{ymin},{xmax},{ymax},{line[0]}')
        file_to_write.write('\n') 
        print(count)
        count += 1
        if count > max_samples:
            break

if __name__ == "__main__":
    pass