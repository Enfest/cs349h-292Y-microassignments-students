from re import S
from hdc import *
from hdc-db import *

def experiment_1():
    
    # fox, box, xfo, car
    HDC.SIZE = 10000
    letter_cb = make_letter_hvs()
    word1 = make_word(letter_cb, "fox")
    word2 = make_word(letter_cb, "box")
    word3 = make_word(letter_cb, "xfo")
    word4 = make_word(letter_cb, "car")
    print("distance between fox and box: %f" % HDC.dist(word1, word2))
    print("distance between fox and xfo: %f" % HDC.dist(word1, word3))
    print("distance between fox and car: %f" % HDC.dist(word1, word4))

    study_distributions()

def experiment_Q3():

    size = [11, 12, 13, 14, 15, 16, 17, 18, 19]
    error_rate = 0.1
    for s in size:
        HDC.SIZE = s
        def gen_codebook_and_words(w1, w2, prob_error=0.0):
            codebook = make_letter_hvs()
            hv1 = make_word(codebook, w1)
            hv2 = make_word(codebook, w2)
            if prob_error > 0.0:
                hv2 = HDC.apply_bit_flips(hv2, prob_error)
            return HDC.dist(hv1, hv2)

        trials = 1000
        d1 = monte_carlo(lambda: gen_codebook_and_words("fox", "box", error_rate), trials)
        d2 = monte_carlo(lambda: gen_codebook_and_words("fox", "car", error_rate), trials)
        plot_dist_distributions("box", d1, "car", d2, f"images/Q4/box_car_size_{s}bits.png")

if __name__ == "__main__":
    # experiment_1()
    experiment_Q3()