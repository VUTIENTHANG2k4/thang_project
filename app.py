from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
#Chuyển đổi cơ số
def convert_base(number, from_base, to_base):
    try:
        # Tách phần nguyên và phần thập phân nếu là số thực
        if '.' in str(number):
            integer_part, fractional_part = str(number).split('.')
            # Chuyển đổi phần nguyên
            dec_integer_part = int(integer_part, from_base) if integer_part else 0
            # Chuyển đổi phần thập phân
            dec_fractional_part = 0
            for i, digit in enumerate(fractional_part):
                dec_fractional_part += int(digit, from_base) / (from_base ** (i + 1))
            dec_number = dec_integer_part + dec_fractional_part
        else:
            # Xử lý số nguyên
            dec_number = int(str(number), from_base)

        # Chuyển đổi sang hệ cơ số đích
        if to_base == 10:
            return str(dec_number)
        elif to_base in [2, 8, 16]:
            # Chuyển phần nguyên
            integer_part = int(dec_number)
            if to_base == 2:
                result_integer = bin(integer_part)[2:]
            elif to_base == 8:
                result_integer = oct(integer_part)[2:]
            elif to_base == 16:
                result_integer = hex(integer_part)[2:]

            # Chuyển phần thập phân
            fractional_part = dec_number - integer_part
            result_fractional = []
            while fractional_part > 0 and len(result_fractional) < 10:  # Giới hạn 10 chữ số thập phân
                fractional_part *= to_base
                digit = int(fractional_part)
                result_fractional.append(hex(digit)[2:] if to_base == 16 else str(digit))
                fractional_part -= digit

            return result_integer + ('.' + ''.join(result_fractional) if result_fractional else '')
        else:
            raise ValueError("Base không hợp lệ!")
    except ValueError:
        return "Lỗi: Dữ liệu không hợp lệ!"

# Chuyển văn bản thành mã ASCII, nhị phân và hexa
def text_to_codes(text):
    ascii_codes = [ord(char) for char in text]
    binary_codes = [bin(code)[2:].zfill(8) for code in ascii_codes]
    hex_codes = [hex(code)[2:] for code in ascii_codes]
    return ascii_codes, binary_codes, hex_codes

# Tính checksum
def calculate_checksum(bits, mode, bit_size):
    chunk_size = bit_size // 8
    data = [int(bits[i:i+chunk_size], 2) for i in range(0, len(bits), chunk_size)]
    
    if mode == "sum":
        checksum = sum(data) % (2 ** bit_size)
    elif mode == "2s_complement":
        checksum = (~sum(data) + 1) & ((2 ** bit_size) - 1)
    elif mode == "xor":
        checksum = 0
        for value in data:
            checksum ^= value
    else:
        checksum = "Lỗi: Phương pháp không hợp lệ!"
    
    return checksum

#Kết nối api
@app.route('/')
def index():
    return render_template('index.html')

#API cho chuyển đổi cơ sốsố
@app.route('/convert_base', methods=['POST'])
def convert_base_api():
    number = request.form['number']
    from_base = int(request.form['from_base'])
    to_base = int(request.form['to_base'])
    result = convert_base(number, from_base, to_base)
    return jsonify(result=result)
#API cho chuyển đổi text sang mã ASCII
@app.route('/convert_text', methods=['POST'])
def convert_text_api():
    text = request.form['text']
    ascii_codes, binary_codes, hex_codes = text_to_codes(text)
    return jsonify(ascii=ascii_codes, binary=binary_codes, hex=hex_codes)

#API cho tính checksum
@app.route('/calculate_checksum', methods=['POST'])
def calculate_checksum_api():
    bits = request.form['bits']
    mode = request.form['mode']
    bit_size = int(request.form['bit_size'])
    checksum = calculate_checksum(bits, mode, bit_size)
    return jsonify(checksum=checksum)

if __name__ == "__main__":
    app.run(debug=True)


