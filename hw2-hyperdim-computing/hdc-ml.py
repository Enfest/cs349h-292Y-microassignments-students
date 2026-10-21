from torchvision.datasets import MNIST
from torch.utils.data import Subset
import tqdm
import torch.utils
from hdc import *
import itertools
import PIL

MAX = 26


class MNISTClassifier:

    def __init__(self):
        self.classifier = HDItemMem()
        # raise Exception("initialize other stuff here")
        self.black_hv = HDC.rand_vec()
        self.white_hv = HDC.rand_vec()
        self.loc_hv = HDC.rand_vec()


    def encode_coord(self, i, j):
        # raise Exception("encode a coordinate in the image as a hypervector")
        return HDC.permute(self.loc_hv, i*MAX+j)

    def encode_pixel(self, i, j, v):
        # raise Exception("encode a pixel in the image as a hypervector")
        color_hv = self.white_hv if v == 255 else self.black_hv
        return HDC.bind(color_hv, self.encode_coord(i, j))


    def encode_image(self, image):
        pixels = []
        for i, j in itertools.product(range(MAX), range(MAX)):
            v = image.getpixel((i, j))
            # print("TODO: do something with encoded pixel value")
            pixels.append(self.encode_pixel(i, j, v))

        return HDC.bundle(pixels)

        # raise Exception("return hypervector encoding of image")

    def decode_pixel(self, image_hypervec, i, j):
        # raise Exception("retrieve the value of the pixel at coordinate i,j in the image hypervector")
        position = self.encode_coord(i, j)
        amplified_hv = HDC.bind(image_hypervec, position)
        white_hd = HDC.dist(amplified_hv, self.white_hv)
        black_hd = HDC.dist(amplified_hv, self.black_hv)
        return 255 if white_hd < black_hd else 0

    def decode_image(self, image_hypervec):
        im = PIL.Image.new(mode="1", size=(MAX, MAX))
        for i, j in list(itertools.product(range(MAX), range(MAX))):
            v = self.decode_pixel(image_hypervec, i, j)
            im.putpixel((i, j), v)
        return im

    def train(self, train_data):
        train_datas = {}
        for image, label in tqdm.tqdm(list(train_data)):
            # raise Exception("do something with the image, label pair from the dataset")
            image_hv = self.encode_image(image)
            if label not in train_datas:
                train_datas[label] = []
            train_datas[label].append(image_hv)
        for label, images in train_datas.items():
            self.classifier.add(label, HDC.bundle(images))

    def classify(self, image, bit_flip_error=0.0):
        image_hv = self.encode_image(image)
        if bit_flip_error > 0.0:
            image_hv = HDC.apply_bit_flips(image_hv, bit_flip_error)
        distances = self.classifier.distance(image_hv)
        label = min(distances, key=distances.get)
        return label, distances[label]

    def build_gen_model(self, train_data):
        self.gen_model = {}
        database = {}
        count = {}
        for image, label in tqdm.tqdm(list(train_data)):
            # raise Exception("build generative model")
            if label not in database:
                database[label] = np.zeros(10000)
            if label not in count:
                count[label] = 0
            count[label] += 1
            database[label] += self.encode_image(image)

        for label, db in database.items():
            self.gen_model[label] = db / count[label]

    def generate(self, cat, trials=10):
        gen_hv = self.gen_model[cat]
        # raise Exception("generate random image with label <cat> using generative model. Average over <trials> trials.")
        result_hvs = []
        for i in range(trials):
            image = np.zeros(HDC.SIZE)
            for i in range(HDC.SIZE):
                if random.random() < gen_hv[i]:
                    image[i] = 1
            result_hvs.append(image)
        return self.decode_image(HDC.bundle(result_hvs))



def initialize(N=1000, size=10000):
    alldata = MNIST(root='data', train=True, download=True)
    dataset = list(map(lambda datum: (datum[0].convert("1"), datum[1]),  \
                Subset(alldata, range(N))))

    train_data, test_data = torch.utils.data.random_split(dataset, [0.6, 0.4])
    HDC.SIZE = size
    classifier = MNISTClassifier()
    return train_data, test_data, classifier


def test_encoding():
    train_data, test_data, classifier = initialize()
    image0, _ = train_data[0]
    hv_image0 = classifier.encode_image(image0)
    result = classifier.decode_image(hv_image0)
    image0.save("sample0.png")
    result.save("sample0_rec.png")


def test_classifier():
    hdc_sizes = [10000, 9000, 8000, 7000, 6000, 5000, 4000, 3900, 3800, 3700, 3600, 3500, 3400, 3300, 3200, 3100, 3000, 2900, 2800, 2700, 2600, 2500, 2400, 2300, 2200, 2100, 2000, 1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
    accuracies = []
    for size in hdc_sizes:
        print("======= testing HDC size: %d =====" % size)
        train_data, test_data, classifier = initialize(2000, size)

        print("======= training classifier =====")
        classifier.train(train_data)

        print("======= testing classifier =====")
        correct, count = 0, 0
        for image, category in (pbar := tqdm.tqdm(test_data)):
            cat, dist = classifier.classify(image)
            if cat == category:
                correct += 1
            count += 1

            pbar.set_description("accuracy=%f" % (float(correct)/count))

        print("ACCURACY: %f" % (float(correct)/count))
        accuracies.append(float(correct)/count)
    # save the plot of accuracies vs hdc sizes
    plt.plot(hdc_sizes, accuracies)
    plt.xlabel("HDC size")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs HDC size")
    plt.savefig("images/accuracy_vs_hdc_size.png")
    plt.close()

def test_classifier_bit_flip_error():
    hdc_sizes = [10000] #, 9000, 8000, 7000, 6000, 5000, 4000, 3900, 3800, 3700, 3600, 3500, 3400, 3300, 3200, 3100, 3000, 2900, 2800, 2700, 2600, 2500, 2400, 2300, 2200, 2100, 2000, 1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
    bit_flip_errors = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    accuracies = []
    for size in hdc_sizes:
        for bit_flip_error in bit_flip_errors:
            print("======= bit flip error: %f, HDC size: %d =====" % (bit_flip_error, size))
            train_data, test_data, classifier = initialize(2000, size)
            classifier.train(train_data)
            correct, count = 0, 0
            for image, category in (pbar := tqdm.tqdm(test_data)):
                cat, dist = classifier.classify(image, bit_flip_error)
                count += 1
                if cat == category:
                    correct += 1
                    pbar.set_description("accuracy=%f" % (float(correct)/count))
            print("ACCURACY: %f" % (float(correct)/count))
            accuracies.append(float(correct)/count)
    # save the plot of accuracies vs hdc sizes
    plt.plot(bit_flip_errors, accuracies)
    plt.xlabel("Bit flip error")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Bit flip error")
    plt.savefig("images/accuracy_vs_bit_flip_error.png")
    plt.close()

def test_generative_model():
    train_data, test_data, classifier = initialize(1000)
    print("======= building generative model =====")
    classifier.build_gen_model(train_data)

    print("======= generate images =====")
    for i in range(10):
        img = classifier.generate(i)
        print("generated image for class %d" % i)
        img.save(f"images/C5/generated_{i}.png")


if __name__ == '__main__':
    # test_encoding()
    # test_classifier()
    # test_classifier_bit_flip_error()
    test_generative_model()
