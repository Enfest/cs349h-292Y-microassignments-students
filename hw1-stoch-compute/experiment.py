from stochastic import *

def experiment_A1():

    bitstream_lens = [10, 20, 40, 80, 160, 320, 480, 640, 960, 1280, 1600, 2240, 2560, 3200, 4096, 5120, 7680, 10240]

    bitstream_reference_mean_values = []
    bitstream_stochastic_mean_values = []
    bitstream_reference_std_values = []
    bitstream_stochastic_std_values = []

    for bitstream_len in bitstream_lens:
        reference_values = []
        stochastic_values = []
        for _ in range(20):
            reference_value, stochastic_value = PART_A_example_computation(bitstream_len)
            reference_values.append(reference_value)
            stochastic_values.append(stochastic_value)
        
        bitstream_reference_mean_values.append(np.mean(reference_values))
        bitstream_stochastic_mean_values.append(np.mean(stochastic_values))
        bitstream_reference_std_values.append(np.std(reference_values))
        bitstream_stochastic_std_values.append(np.std(stochastic_values))

    # plot the results with error bars  and the x-axis as the bitstream length
    plt.errorbar(bitstream_lens, bitstream_stochastic_mean_values, yerr=bitstream_stochastic_std_values, label='Stochastic Mean')
    plt.errorbar(bitstream_lens, bitstream_reference_mean_values, yerr=bitstream_reference_std_values, label='Reference Mean')
    plt.xlabel('Bitstream Length')
    plt.ylabel('Mean Value')
    plt.legend()
    plt.grid(True)
    plt.title('Experiment A1')
    # save the plot as a png file with dpi 300
    plt.savefig('./images/experiment_A1.png', dpi=300)

    return bitstream_lens, bitstream_reference_mean_values, bitstream_stochastic_mean_values, bitstream_reference_std_values, bitstream_stochastic_std_values

def experiment_A2():
    target_value = 1.0/1000

    result = []

    for _ in range(1000):
        bitstream = PosStochasticComputing.to_stoch(target_value, 1000)
        value = PosStochasticComputing.from_stoch(bitstream)
        # print(value)
        result.append(value)

    # plot the results with a histogram
    plt.figure()
    bins = np.arange(-0.0005, 0.0205, 0.001)  # optional: zoom range
    plt.hist(result, bins=bins)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Experiment A2')
    plt.xlim(-0.0005, 0.02)  # optional: makes bars visible
    plt.grid(True)
    plt.savefig('./images/experiment_A2.png', dpi=300)
    plt.close()

    return 

def experiment_X1():
    # bitflip error = 0.0001
    num_bits = 1000
    num_trials = 1000
    target_value = 0.1

    result_0001 = []
    PosStochasticComputing.FLIP_PROB = 0.0001
    PosStochasticComputing.APPLY_FLIPS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitflip(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_0001.append(value)

    # bitflip error = 0.1
    result_1 = []
    PosStochasticComputing.FLIP_PROB = 0.1
    PosStochasticComputing.APPLY_FLIPS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitflip(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_1.append(value)

    # plot the results with a histogram
    plt.figure()
    bins = np.arange(-0.0005, 0.3005, 0.001)
    plt.hist(result_0001, bins=bins, label='Bitflip Error = 0.0001')
    plt.hist(result_1, bins=bins, label='Bitflip Error = 0.1')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Experiment X1')
    plt.legend()
    plt.grid(True)
    plt.savefig('./images/experiment_X1.png', dpi=300)
    plt.close()

    return 

def experiment_X2():
    # bitflip error = 0.0001
    num_bits = 1000
    num_trials = 1000
    target_value = 0.1

    result_0001 = []
    PosStochasticComputing.SHIFT_PROB = 0.0001
    PosStochasticComputing.APPLY_SHIFTS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitshift(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_0001.append(value)

    # bitflip error = 0.1
    result_1 = []
    PosStochasticComputing.SHIFT_PROB = 0.1
    PosStochasticComputing.APPLY_SHIFTS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitshift(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_1.append(value)

    # plot the results with a histogram
    plt.figure()
    bins = np.arange(-0.0005, 0.3005, 0.001)
    plt.hist(result_0001, bins=bins, label='Bitshift Error = 0.0001')
    plt.hist(result_1, bins=bins, label='Bitshift Error = 0.1')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Experiment X2')
    plt.legend()
    plt.grid(True)
    plt.savefig('./images/experiment_X2.png', dpi=300)
    plt.close()
    return 

def experiment_X3():
    # bitflip error = 0.0001
    num_bits = 10000
    num_trials = 1000
    target_value = 0.1

    result_0001 = []
    PosStochasticComputing.FLIP_PROB = 0.0001
    PosStochasticComputing.APPLY_FLIPS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitflip(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_0001.append(value)

    # bitflip error = 0.1
    result_1 = []
    PosStochasticComputing.FLIP_PROB = 0.1
    PosStochasticComputing.APPLY_FLIPS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitflip(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_1.append(value)

    # plot the results with a histogram
    plt.figure()
    bins = np.arange(-0.0005, 0.3005, 0.001)
    plt.hist(result_0001, bins=bins, label='Bitflip Error = 0.0001')
    plt.hist(result_1, bins=bins, label='Bitflip Error = 0.1')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Experiment X3 (bitflip error)')
    plt.legend()
    plt.grid(True)
    plt.savefig('./images/experiment_X3-1.png', dpi=300)
    plt.close()

    # bitflip error = 0.0001

    num_trials = 1000
    target_value = 0.1

    result_0001 = []
    PosStochasticComputing.SHIFT_PROB = 0.0001
    PosStochasticComputing.APPLY_SHIFTS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitshift(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_0001.append(value)

    # bitflip error = 0.1
    result_1 = []
    PosStochasticComputing.SHIFT_PROB = 0.1
    PosStochasticComputing.APPLY_SHIFTS = True
    for _ in range(num_trials):
        bitstream = PosStochasticComputing.to_stoch(target_value, num_bits)
        bitstream = PosStochasticComputing.apply_bitshift(bitstream)
        value = PosStochasticComputing.from_stoch(bitstream)
        result_1.append(value)

    # plot the results with a histogram
    plt.figure()
    bins = np.arange(-0.0005, 0.3005, 0.001)
    plt.hist(result_0001, bins=bins, label='Bitshift Error = 0.0001')
    plt.hist(result_1, bins=bins, label='Bitshift Error = 0.1')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Experiment X3-2 (bitshift error)')
    plt.legend()
    plt.grid(True)
    plt.savefig('./images/experiment_X3-2.png', dpi=300)
    plt.close()
    return 

def experiment_Z1():
    for _ in range(5):
        v = round(np.random.uniform(),1)
        print(f"x = {v}")
        print("running with save_rngs disabled")
        run_stochastic_computation(lambda : PART_Z_execute_rng_efficient_computation(value=v, N=1000, save_rngs=False), ntrials=1000, visualize=False, summary=True)
        print("running with save_rngs enabled")
        run_stochastic_computation(lambda : PART_Z_execute_rng_efficient_computation(value=v, N=1000, save_rngs=True), ntrials=1000, visualize=False, summary=True)

def experiment_W1():

    from PIL import Image

    # image downsampling
    image = Image.open('experiment_W_images/test_png.webp').convert('L')
    pixels = np.asarray(image, dtype=np.float64) / 255.0

    height, width = pixels.shape

    print(f"height: {height}, width: {width}")
    
    bitstream_lengths = [16,32,64,128,256,512]

    output_ref_images = np.zeros((height // 4, width // 4), dtype=np.uint8)
    output_stoch_images = np.zeros((height // 4, width // 4), dtype=np.uint8)
    for bitstream_length in bitstream_lengths:
        for y in range(height // 4):
            for x in range(width // 4):
                value = pixels[y * 4 : y * 4 + 4, x * 4 : x * 4 + 4]
                ref_value = value.mean()
                # flatten value to single dimension array
                value = value.flatten()
                stoc_bitstream = []
                for v in value:
                    stoc_bitstream.append(PosStochasticComputing.to_stoch(v, bitstream_length))
                index = 0
                while index < len(stoc_bitstream)-1:
                    stoc_bitstream.append(PosStochasticComputing.stoch_add(stoc_bitstream[index], stoc_bitstream[index+1]))
                    index += 2
                stoch_value = PosStochasticComputing.from_stoch(stoc_bitstream[-1])
                output_stoch_images[y, x] = stoch_value*255
                output_ref_images[y, x] = ref_value*255

        output_stoch_images = output_stoch_images.astype(np.uint8)
        output_ref_images = output_ref_images.astype(np.uint8)
        output_stoch_image = Image.fromarray(output_stoch_images)
        output_ref_image = Image.fromarray(output_ref_images)
        output_stoch_image.save(f'experiment_W_images/output_downsampled_{bitstream_length}_stoch.png')
        output_ref_image.save(f'experiment_W_images/output_downsampled_{bitstream_length}_ref.png')

def experiment_W2():
    from PIL import Image
    image = Image.open('experiment_W_images/test_image_5.png').convert('L')
    pixels = np.asarray(image, dtype=np.float64) / 255.0
    height, width = pixels.shape
    print(f"height: {height}, width: {width}")
    bitstream_lengths = [8,16,32,64,128,256,512,1024]
    output_ref_images = np.zeros((height // 2, width // 2), dtype=np.uint8)
    output_stoch_images = np.zeros((height // 2, width // 2), dtype=np.uint8)
    for bitstream_length in bitstream_lengths:
        print(f"bitstream length: {bitstream_length}")
        for y in range(height // 2):
            for x in range(width // 2):
                value = pixels[y * 2 : y * 2 + 2, x * 2 : x * 2 + 2]
                a = value[0, 0]
                b = value[0, 1]
                c = value[1, 0]
                d = value[1, 1]
                if bitstream_length == bitstream_lengths[0]:
                    ref_value = (abs(a-d) + abs(b-c)) / 2
                    output_ref_images[y, x] = ref_value*255

                # stochastic bitstream 
                bitstream_a = [np.random.random() for _ in range(bitstream_length)]
                bitstream_b = [np.random.random() for _ in range(bitstream_length)]
                a = bitstream_a < a
                b = bitstream_b < b
                c = bitstream_b < c
                d = bitstream_a < d
                output = PosStochasticComputing.stoch_add(
                    PosStochasticComputing.stoch_diff(a, d),
                    PosStochasticComputing.stoch_diff(b, c)
                )
                output_stoch_images[y, x] = PosStochasticComputing.from_stoch(output)*255

        output_stoch_images = output_stoch_images.astype(np.uint8)
        output_stoch_image = Image.fromarray(output_stoch_images)
        output_stoch_image.save(f'experiment_W_images/output_edge_detection_{bitstream_length}_stoch.png')
        if bitstream_length == bitstream_lengths[0]:
            output_ref_images = output_ref_images.astype(np.uint8)
            output_ref_image = Image.fromarray(output_ref_images)
            output_ref_image.save(f'experiment_W_images/output_edge_detection_ref.png')

if __name__ == "__main__":
    experiment_W2()