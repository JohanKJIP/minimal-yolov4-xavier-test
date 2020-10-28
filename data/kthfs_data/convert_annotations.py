import os

image_folder = 'all_images'
label_folder = 'all_labels'

with open('train.txt', 'w') as train_file:
    for file_name in os.listdir(image_folder):
        with open(f'{label_folder}/{file_name}'.split('.')[0] + '.txt') as label_file:
            train_file.write(f'{image_folder}/{file_name}')
            for line in label_file:
                line = line.split(' ')
                line[-1] = line[-1].strip()
                print(line)
                x2 = float(line[1]) + float(line[3])
                y2 = float(line[2]) + float(line[4])
                train_file.write(f' {line[1]},{line[2]},{x2},{y2},{line[0]}')
        train_file.write('\n')
        


if __name__ == "__main__":
    pass