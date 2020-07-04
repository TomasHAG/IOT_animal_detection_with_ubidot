import ubinascii
# Here are the keys that are used to initilize LORAWAN
def eui():
    return ubinascii.unhexlify('70B3D57ED0030CC1')

def key():
    return ubinascii.unhexlify('214C55A7F7D6107B6BDA01338307DB25')
