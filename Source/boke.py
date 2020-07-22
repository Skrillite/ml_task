import cv2
import numpy
from progress.bar import ChargingBar

original_path = input("\nimage path: ")
kernel_path = input("kernel path: ")

original = cv2.imread(original_path)
kernel = cv2.imread(kernel_path, cv2.IMREAD_GRAYSCALE)

# проверка ядра на равенство и нечетность сторон

if kernel.shape[0] != kernel.shape[1] or not kernel.shape[0] & 1:
    bs = min(kernel.shape[0], kernel.shape[1])
    bs -= not bs & 1
    kernel = cv2.resize(kernel, (bs, bs))

print('\n')

# создание дополнения изображения
# copy - неизменяемое дополненное изображения

addition_size = len(kernel) // 2
copy = numpy.full((len(original) + addition_size * 2, len(original[0]) + addition_size * 2, 3), 1)
tmp = numpy.concatenate((numpy.full((addition_size, 3), original[0][0]), original[0], numpy.full((addition_size, 3), original[0][-1])))
for i in range(addition_size):
    copy[i] = tmp
for i in range(addition_size, addition_size + len(original)):
    copy[i] = numpy.concatenate((numpy.full((addition_size, 3), original[i - addition_size][0]), original[i - addition_size]
                                , numpy.full((addition_size, 3), original[i - addition_size][-1]))) 
tmp = numpy.concatenate((numpy.full((addition_size, 3), original[-1][0]), original[-1], numpy.full((addition_size, 3), original[-1][-1])))
for i in range(addition_size + len(original), addition_size * 2 + len(original)):
    copy[i] = tmp

# операция свертки

bar = ChargingBar("Computing", max=original.shape[0])
kernel_sum = numpy.sum(kernel)
for w in range(original.shape[0]):
    for h in range(original.shape[1]):
        for channel in range(0, 3):
            original[w, h, channel] = numpy.sum(copy[w : addition_size * 2 + w + 1, h : addition_size * 2 + h + 1, channel : channel + 1] 
                * numpy.reshape(kernel, (kernel.shape[0], kernel.shape[1], 1))) / kernel_sum
    bar.next()
bar.finish()

output_path = 'results\\' + original_path.split('\\')[-1].split('.')[0] + '_' + kernel_path.split('\\')[-1].split('.')[0] + '.png'
cv2.imwrite(output_path, original)
print(f"result: {output_path}")