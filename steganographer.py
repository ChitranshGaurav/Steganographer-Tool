"""
* Author: Chitransh Gaurav
* Date: 8th October 2015
* Title: Steganographer
* Description: Hides text in images
"""


from PIL import Image
import binascii

#Utility functions:

#Method to covert r g b values to a string of hexvalues of r g b
def rgb2hex(r, g, b):
	#each value lies from 0 - 255 within width two for hex
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

#Method to convert hex string to a tuple of r g b
def hex2rgb(hexstring):
	#ord is a function that is inverse of char() or unichar()
	return tuple(map(ord, hexstring[1:].decode('hex')))

#Method converts text to be encrypted to binary equivalent
def str2bin(encryptingText):
	#hexlify converts data to hexadecimal representation of binary equivalent
	binText = bin(int(binascii.hexlify(encryptingText), 16))
	return binText[2:]
	#ignoring 0b prefix


#Method converts decoded binary back to text
def bin2str(decodingText):
	#unhexlify converts it back to text
	decodedText = binascii.unhexlify('%x' % (int('0b'+decodingText, 2)))
	return decodedText

#Method to replace information in blue pixel with our binary data bit
def impress(hexstring, bit):
	if hexstring[-1] in ('0','1', '2', '3', '4', '5'):
		hexstring = hexstring[:-1] + bit
		return hexstring
	else:
		return -1

#Method to mine the binary data from the pixels
def extract(hexstring):
	if hexstring[-1] == '0' or hexstring[-1] == '1':
		return hexstring[-1]
	else:
		return -1
#Utlity functions end.

#Method to impress message in the pixels of the image:
def encrypt(filename, filenamenew, text):
	try:
		img = Image.open(filename)
	except Exception as err:
		print str(err)
		return -1
	
	#Adding a marker to indicate end of text 1x15+0 does never occur in alphabetical text
	encryptingText = str2bin(text) + '1111111111111110'
	lengthOfStream = len(encryptingText)
	if img.mode == 'RGBA' :
		imgobj = img.getdata()
		newobj = []
		bititerator = 0
		for pixels in imgobj:
			if(bititerator < lengthOfStream):
				tempobj = impress(rgb2hex(pixels[0],pixels[1],pixels[2]), encryptingText[bititerator])
				if tempobj == -1:
					newobj.append(pixels)
				else:
					(r, g, b) = hex2rgb(tempobj)
					newobj.append((r,g,b,255))
					bititerator += 1
			else:
				newobj.append(pixels)
		img.putdata(newobj)
		img.save(filenamenew, 'PNG')
		return 1
	return -1

#Method to extract information out of the image

def decrypt(filename):
	try:
		img = Image.open(filename)
	except Exception as err:
		print str(err)
		return -1
	decodingText = ''
	if img.mode == 'RGBA':
		imgobj = img.getdata()
		for pixels in imgobj:
			bit = extract(rgb2hex(pixels[0], pixels[1], pixels[2]))
			if bit != -1:
				decodingText = decodingText + bit
				if decodingText[-16:] == '1111111111111110' :
					return bin2str(decodingText[:-16])
		return bin2str(decodingText)
	return -1

#Main methods:

def func1():
	filename1 = raw_input('Enter filename of image to be used: ')
	filename2 = raw_input('Enter filename of new image: ')
	text = str(raw_input('Enter text to be encoded: '))
	if encrypt(filename1, filename2, text) != -1 :
		print "Successfully Completed"
	else:
		print "Error!"
	return

def func2():
	filename = raw_input('Enter filename of the image: ')
	cleartext = decrypt(filename)
	if cleartext != -1:
		print "Clear Text: ",cleartext
	else:
		print "Error!"
	return
	
	

def Main():
	print "Choose an option:"
	print "1. Encrypt \n2. Decipher\n3. Exit"
	choice = int(raw_input())
	options	= {1 : func1,
		   2 : func2,
	}
	while choice != 3:
		options[choice]()
		choice = int(raw_input())


if __name__ == '__main__':
	Main()

