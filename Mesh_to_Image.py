from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from os import path, makedirs
import numpy as np
from PIL import Image, ImageChops

def get_image(data):
    img = np.array(data)
    (X, Y, A) = img.shape
    x_min, y_min = X, Y
    x_max, y_max = 0, 0

    for x in range(X):
        for y in range(Y):
            if tuple(img[x, y]) != (255, 255, 255):
                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y

    offset = 5
    my_image = data[x_min - offset:x_max + offset, y_min - offset:y_max + offset]
    return Image.fromarray(my_image)

def get_trim_image(data):

    def trim(im, border):
      bg = Image.new(im.mode, im.size, border)
      diff = ImageChops.difference(im, bg)
      bbox = diff.getbbox()
      if bbox:
        print(bbox)
        return im.crop(bbox)

    image = Image.fromarray(data)
    image.thumbnail((500, 500), Image.ANTIALIAS)
    return trim(image, (255, 255, 255))

def get_angles():
    the = (1 + np.sqrt(5)) / 2
    in_the = 1/the

    def cart2sph(coordinates):
        (x, y, z) = coordinates
        hxy = np.hypot(x, y)
        r = np.hypot(hxy, z)
        el = np.arctan2(z, hxy)
        az = np.arctan2(y, x)
        az, el, r = float("{0:.2f}".format(np.rad2deg(az))), \
                    float("{0:.2f}".format(np.rad2deg(el))), \
                    float("{0:.2f}".format(r))
        return (el, az, r)

    Cartesian_coordinates = [(1,1,1), (-1,1,1), (1,-1,1), (-1,-1,1), (1,1,-1), (-1,1,-1), (1,-1,-1), (-1,-1,-1),
                             (0, the, in_the), (0, -the, in_the), (0, the, -in_the), (0, -the, -in_the),
                             (in_the, 0, the), (-in_the, 0, the), (in_the, 0, -the), (-in_the, 0, -the),
                             (the, in_the, 0), (-the, in_the, 0), (the, -in_the, 0), (-the, -in_the, 0)]

    angles = []
    for cc in Cartesian_coordinates:
        angles.append(cart2sph(cc))

    return angles



class Mesh_to_Image:
    def __init__(self, image_folder='data_train', files_list='file_list.txt', rot_angle=None):
        """
        :param image_folder: Folder where all the images of mesh model will be saved
        :param files_list: .txt file which contain all mesh models name
        :param rot_angle: tuple of set of angles from which the model is rotated and taken images
        """
        rot_angle = get_angles()

        if rot_angle == None:
            rot_angle = [(0, 0), (0, 180), (0, 90),  (0, 270), (90, 0), (-90, 0)]
        if not path.exists(image_folder):
            makedirs(image_folder)
        self.rot_angle = rot_angle
        self.files_list = files_list
        self.image_folder = image_folder
        self.genrete_Image()

    def genrete_Image(self):
        file_no = 0
        files = open(self.files_list, 'r')
        for file in files:
            file_no += 1
            file_path = file[:-1]
            self.file_name, exe = path.splitext(file_path)
            print(str(file_no) + " " + self.file_name + exe)
            # Create a new plot
            figure = plt.figure(figsize=(10, 10))
            axes = mplot3d.Axes3D(figure)

            # Load the STL files and add the vectors to the plot
            Mesh = mesh.Mesh.from_file(file_path)
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(Mesh.vectors, edgecolor='k'))

            # Auto scale to the mesh size
            scale = Mesh.points.flatten(1)
            axes.auto_scale_xyz(scale, scale, scale)
            axes.set_axis_off()

            # Generate Image from Different angle
            angle_no = 0
            for angle in self.rot_angle:
                angle_no += 1
                axes.view_init(angle[0], angle[1])
                category_folder = file_path.split('/')[-2]

                # if angle == self.rot_angle[0] or angle == self.rot_angle[1]:
                #     folder_path = path.join(self.image_folder, 'data_1', category_folder)
                # elif angle == self.rot_angle[2] or angle == self.rot_angle[3]:
                #     folder_path = path.join(self.image_folder, 'data_2', category_folder)
                # elif angle == self.rot_angle[4] or angle == self.rot_angle[5]:
                #     folder_path = path.join(self.image_folder, 'data_3', category_folder)
                # else:
                #     raise Exception("self.rot_angle are more then 6")


                file_base_name, _ = path.splitext(path.basename(file_path))
                folder_path = path.join(self.image_folder, category_folder, file_base_name)
                file_name = str(angle[0]) + "_" + str(angle[1]) + ".png"
                image_file_path = path.join(folder_path, file_name)
                if not path.exists(folder_path):
                    makedirs(folder_path)
                    print('Folder Created ', folder_path)

                # Image Creation
                figure.canvas.draw()
                # Now we can save it to a numpy array.
                data = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
                data = data.reshape(figure.canvas.get_width_height()[::-1] + (3,))
                image = get_trim_image(data)
                image.save(image_file_path)
                print(str(file_no) + "," + str(angle_no) + " >> " + image_file_path + "  Done!")
                # figure.clf()
                # plt.close(figure)


if __name__ == "__main__":

    Mesh_to_Image(image_folder='Data_lfd', files_list= 'file_list.txt')

