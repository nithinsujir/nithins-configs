import os
import random

colors = [
    ['fffff7', 'black'],
#    ['54788e', 'grey100'],
#    ['4c8186', 'grey100'],
#    ['4e4c86', 'grey100'],
#    ['794243', 'grey100'],
#    ['7d5f39', 'grey100'],
#    ['747c3b', 'grey100'],
#    ['41723e', 'grey100'],
#    ['583c36', 'grey100'],
#    ['52584f', 'white'],
#    ['525358', 'white'],
#    ['475829', 'white'],
#    ['524822', 'white'],
#    ['425839', 'white'],
]

index = random.randint(0, len(colors) - 1)

os.system('mrxvt -bg \#' + colors[index][0] + ' -fg ' + colors[index][1] + ' -xft -xftaa -xftfn "Liberation Mono" -xftsz 9 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 65534 -hold 0 -bt')

