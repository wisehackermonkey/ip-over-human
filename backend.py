#!/bin/python
import crcmod
from scapy.all import *

def convert_to_base(n, base):
   result = []
   while n > 0:
       remainder = n % base
       result.append(remainder)
       n = n // base
   return result[::-1]

def convert_packet_to_emoji_base(packet_arr,charset, base):
   return "".join([charset[x] for x in  convert_to_base(int("".join(map(str,packet_arr))),base)])

def simple_emoji_convert(packet_number,charset, base):
       return [charset[x] for x in convert_to_base(packet_number,base)]

def convert_from_base(digits, base):
    result = 0
    for digit in digits:
        result = result * base + digit
    return result

def decode_emoji_packet(packet_str, base, charset):
    charset_dict = {char: index for index, char in enumerate(charset)}
    packet_arr = [charset_dict[char] for char in packet_str]
    decoded_number = convert_from_base(packet_arr, base)
    return decoded_number

def crc(data, polynomial=0x131, init_crc=0x00):
    """
    Check CRC for given data against an expected CRC value.
    
    Args:
        data (bytes or str): The data for which you want to check the CRC. If provided as a string, it will be encoded as bytes.
        expected_crc (int): The expected CRC value in base 10.
        polynomial (int): The CRC polynomial to use (default is CRC-8 polynomial 0x131).
        init_crc (int): The initial CRC value (default is 0x00).

    Returns:
        bool: True if the calculated CRC matches the expected CRC, False otherwise.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    crc_func = crcmod.mkCrcFun(polynomial, initCrc=init_crc, rev=True)
    checksum = crc_func(data)
    return checksum 

def check_crc(data, expected_crc):
    """
    Check CRC for given data against an expected CRC value.
    
    Args:
        data (bytes): The data for which you want to check the CRC.
        expected_crc (int): The expected CRC value in base 10.
        polynomial (int): The CRC polynomial to use (default is CRC-8 polynomial 0x131).
        init_crc (int): The initial CRC value (default is 0x00).

    Returns:
        bool: True if the calculated CRC matches the expected CRC, False otherwise.
    """
   
    return crc(data) == expected_crc

charset = "💎🏠🚗✈️🛳🚌🏫🏥🗼🗽🎡🎢🪑🛏💻🖨🖱📀📸📺📞💡🔦🗑🧻🧼🧴🪒🧹🎈🎁🎃🎄🧩🧸🪄🎮🎲🎰🪅🪆🪡🧶🏥🏦🏭🏰🗿🎡🎢💈🎪🎭🎨🧵🧶👓👕👖🧣🧤🧥🧦👗🩲👙👛👜🎒👞👑🎩🎓🧢💄💍"
base = 77

# INPUT_IP = input("IP address you want to ping?")

# Create an IP packet object
ip = IP(dst="192.168.1.20")
# ip = IP(dst=INPUT_IP)

# Create an ICMP packet object
icmp = ICMP()

# Combine both to create the final packet
packet = ip/icmp
raw_packet_list = list(raw(packet))


emoji_packet = convert_packet_to_emoji_base(raw_packet_list, charset, base)

correction_code = crc("".join(map(str,raw_packet_list)))
emoji_crc = "".join(simple_emoji_convert(correction_code,charset, base))
print(f"""var currentArray = {repr(list(emoji_packet) + ['crc'] +list(emoji_crc))}
""")


