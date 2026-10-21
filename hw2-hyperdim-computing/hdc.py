import string
import random
import operator
import numpy as np
import tqdm
import matplotlib.pyplot as plt


class HDC:
    SIZE = 10000

    @classmethod
    def rand_vec(cls):
        # raise Exception("generate atomic hypervector with size HDC.SIZE")
        threshold = 0.5
        return np.array([1 if random.random() < threshold else 0 for _ in range(HDC.SIZE)], dtype=np.int8)

    @classmethod
    def dist(cls, x1, x2):
        # raise Exception("Hamming distance between hypervectors")
        return np.sum(x1 != x2)/HDC.SIZE

    @classmethod
    def bind(cls, x1, x2):
        # raise Exception("bind two hypervectors together")
        # bitwise XOR between x1 and x2
        return np.bitwise_xor(x1, x2)


    @classmethod
    def bind_all(cls, xs):
        # raise Exception("convenience function. bind together a list of hypervectors")
        output = xs[0].copy()
        for x in xs[1:]:
            output = cls.bind(output, x)
        return output

    @classmethod
    def bundle(cls, xs):
        if len(xs) == 0:
            raise ValueError("Cannot bundle an empty sequence")
        count_ones = np.sum(np.stack(xs), axis=0, dtype=np.int64)
        K = len(xs)
        output = (count_ones > K / 2).astype(np.int8)
        ties = count_ones == K / 2
        output[ties] = np.random.randint(0, 2, size=np.count_nonzero(ties))
        return output

    @classmethod
    def permute(cls, x, i):
        # raise Exception("permute x by i, where i can be positive or negative")
        return np.roll(x, i)

    @classmethod
    def apply_bit_flips(cls, x, p=0.0):
        # raise Exception("return a corrupted hypervector, given a per-bit bit flip probability p")
        error_vector = np.array([1 if random.random() < p else 0 for _ in range(HDC.SIZE)], dtype=np.int8)
        return np.bitwise_xor(x, error_vector)


class HDItemMem:

    def __init__(self, name=None) -> None:
        self.name = name
        self.item_mem = {}
        # per-bit bit flip probabilities for the Hamming distance
        self.ber = 0.0

    def add(self, key, hv):
        assert (hv is not None)
        self.item_mem[key] = hv
        return hv

    def get(self, key):
        return self.item_mem[key]

    def has(self, key):
        return key in self.item_mem

    def distance(self, query):
        # raise Exception("compute hamming distance between query vector and each row in item memory. Introduce bit flips if the bit flip probability is nonzero")
        distances = {}
        for key, hv in self.item_mem.items():
            distance = HDC.dist(query, hv)
            if self.ber > 0.0:
                distance = HDC.apply_bit_flips(distance, self.ber)
            distances[key] = distance
        return distances

    def all_keys(self):
        return list(self.item_mem.keys())

    def all_hvs(self):
        return list(self.item_mem.values())

    def wta(self, query):
        # raise Exception("winner-take-all querying")
        distances = self.distance(query)
        # return the key with the smallest distance
        return min(distances, key=distances.get)

    def matches(self, query, threshold=0.49):
        # raise Exception("threshold-based querying")
        distances = self.distance(query)
        # return the keys with distances less than the threshold
        return [key for key, distance in distances.items() if distance < threshold]


# a codebook is simply an item memory that always creates a random hypervector
# when a key is added.
class HDCodebook(HDItemMem):

    def __init__(self, name=None):
        HDItemMem.__init__(self, name)

    def add(self, key):
        self.item_mem[key] = HDC.rand_vec()
        return self.item_mem[key]


def make_letter_hvs():
    # raise Exception("return a codebook of letter hypervectors")
    codebook = HDCodebook()
    for letter in string.ascii_lowercase:
        codebook.add(letter)
    return codebook


def make_word(letter_codebook, word):
    # raise Exception("make a word using the letter codebook")
    word_hvs = []
    for index, letter in enumerate(word):
        word_hvs.append(HDC.permute(letter_codebook.get(letter), index))
        # word_hvs.append(letter_codebook.get(letter))
    return HDC.bundle(word_hvs)


def monte_carlo(fxn, trials):
    results = list(map(lambda i: fxn(), tqdm.tqdm(range(trials))))
    return results


def plot_dist_distributions(key1, dist1, key2, dist2, png_name=None):
    plt.hist(dist1,
            alpha=0.75,
            label=key1)

    plt.hist(dist2,
            alpha=0.75,
            label=key2)

    plt.legend(loc='upper right')
    plt.title('Distance distribution for Two Words')
    if png_name is not None:
        plt.savefig(png_name)
    else:
        plt.show()
    plt.clf()


def study_distributions():
    def gen_codebook_and_words(w1, w2, prob_error=0.0):
        codebook = make_letter_hvs()
        hv1 = make_word(codebook, w1)
        hv2 = make_word(codebook, w2)
        if prob_error > 0.0:
            hv2 = HDC.apply_bit_flips(hv2, prob_error)
        return HDC.dist(hv1, hv2)

    trials = 1000
    d1 = monte_carlo(lambda: gen_codebook_and_words("fox", "box"), trials)
    d2 = monte_carlo(lambda: gen_codebook_and_words("fox", "car"), trials)
    plot_dist_distributions("box", d1, "car", d2, "images/box_car.png")
    for perr in [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49]:
        d1 = monte_carlo(lambda: gen_codebook_and_words("fox", "box", prob_error=perr), trials)
        d2 = monte_carlo(lambda: gen_codebook_and_words("fox", "car", prob_error=perr), trials)
        plot_dist_distributions("box", d1, "car", d2, f"images/Q3/box_car_error_{perr*100:.0f}.png")


if __name__ == '__main__':
    HDC.SIZE = 10000

    letter_cb = make_letter_hvs()
    hv1 = make_word(letter_cb, "fox")
    hv2 = make_word(letter_cb, "box")
    hv3 = make_word(letter_cb, "xfo")
    hv4 = make_word(letter_cb, "car")

    print(HDC.dist(hv1, hv2))
    print(HDC.dist(hv1, hv3))
    print(HDC.dist(hv1, hv4))

    study_distributions()
