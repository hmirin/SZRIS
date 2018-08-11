import base64
import math
import string
import sys

base = 15
chars = "0123456789abcde"
padding_char = "f"


def base_n_encode(s, b):
    # encode UTF-8 string to base10 number
    n = int.from_bytes(s.encode("UTF-8"), 'little')
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return "".join([chars[i] for i in digits[::-1]])


def base_n_decode(s, b):
    return int(s, 15).to_bytes(int(s, 15).bit_length() // 8+1, 'little').decode("UTF-8").replace('\x00', '')


def gengou2address(gengou):
    if (type(gengou) != str):
        raise Exception("元号はUTF-8で表現可能な文字列で入力してください")
    else:
        encoded_gengou = base_n_encode(gengou, base)
        if len(encoded_gengou) > 42 - 2:
            raise Exception("元号が長すぎてアドレスにエンコードできませんでした")
        else:
            address = "0x" + encoded_gengou + \
                padding_char * (42 - 2 - len(encoded_gengou))
            if (address2gengou(address) == gengou):
                return address
            else:
                raise Exception("何らかの理由で復号時に元号を元の文字列に戻すことができませんでした")


def address2gengou(address):
    if (type(address) != str or not address.startswith("0x") or len(address) != 42 or set(address) > set(string.ascii_lowercase + string.digits)):
        raise Exception("有効なEthereumのアドレスでありません")
    if address.lower() != address:
        raise Exception("小文字形式のEthereumアドレスに変換して入力してください")
    else:
        decoded_gengou = base_n_decode(
            address[2:].replace(padding_char, ""), base)
        return decoded_gengou


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "gengou2address":
        s = input("投票する元号を入力してください：")
        if not s:
            raise Exception("元号をなくすことはできません")
        print("次のアドレスにSZRISトークンを送付してください： " + gengou2address(s))
    elif len(sys.argv) == 2 and sys.argv[1] == "address2gengou":
        s = input("投票先をチェックしたいアドレスを入力してください：")
        if not s:
            raise Exception("有効なEthereumのアドレスを入力してください")
        try:
            print("このアカウントは次の元号に対応しています： " + address2gengou(s))
        except UnicodeDecodeError as e:
            print("このアカウントは投票先でありません")
        except Exception as e:
            raise e

    else:
        print("""
アドレスを元号に変換する場合：　python3 converter.py address2gengou
元号をアドレスに変換する場合：　python3 converter.py gengou2address
*環境によってはpythonコマンドがpython3コマンドと同等の場合があります
        """)


if __name__ == '__main__':
    main()
