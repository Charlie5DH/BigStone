
def read_barcode_one_time():
    '''
    Function that reads a single input from the barcode scanner
    and returns the string of the barcode
    Input: None
    Output: String of the barcode
    '''
    print(f'called read_barcode_one_time()')
    print(f'awaiting input from barcode scanner...')
    barcode = input('Please scan the barcode: ')
    print(f'barcode scanned: {barcode}')
    return barcode

def read_barcode_multiple_times(exit_code='7121100004'):
    '''
    Function that reads multiple inputs from the barcode scanner
    and returns a list of the barcodes
    Input: None
    Output: List of the barcodes
    '''
    print(f'called read_barcode_multiple_times()')
    print(f'awaiting input from barcode scanner...')
    barcodes = []
    while True:
        barcode = input('Please scan the barcode: ')
        if barcode == exit_code:
            break
        else:
            barcodes.append(barcode)
    print(f'barcodes scanned: {barcodes}')
    return barcodes

if __name__ == '__main__':
    read_barcode_multiple_times()
    