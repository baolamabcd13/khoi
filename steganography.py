class DatabaseSteganography:
    @staticmethod
    def hide_message_in_text(text, secret_message):
        """
        Giấu tin bằng cách thay đổi case của các ký tự trong text
        Bit 1 = chữ hoa, Bit 0 = chữ thường
        """
        # Chuyển secret message thành chuỗi nhị phân
        binary = ''.join(format(ord(c), '08b') for c in secret_message)
        
        # Đảm bảo text đủ dài để giấu tin
        base_text = text
        while len(base_text) < len(binary):
            base_text += text
            
        # Giấu tin bằng cách thay đổi case
        result = ''
        binary_index = 0
        
        for char in base_text:
            if not char.isalpha():
                result += char
                continue
                
            if binary_index < len(binary):
                # Bit 1 = chữ hoa, Bit 0 = chữ thường
                result += char.upper() if binary[binary_index] == '1' else char.lower()
                binary_index += 1
            else:
                result += char.lower()
                
        return result

    @staticmethod
    def extract_message_from_text(text):
        """
        Trích xuất tin từ case của các ký tự
        """
        # Lấy chuỗi bit từ case của các ký tự
        binary = ''
        for char in text:
            if char.isalpha():
                binary += '1' if char.isupper() else '0'
        
        # Chuyển binary thành text
        message = ''
        for i in range(0, len(binary) - (len(binary) % 8), 8):
            byte = binary[i:i+8]
            try:
                message += chr(int(byte, 2))
            except ValueError:
                break
                
        return message

    @staticmethod
    def hide_in_case(text, bit):
        """Giấu 1 bit thông tin bằng cách thay đổi chữ hoa/thường"""
        return text.upper() if bit == '1' else text.lower()

    @staticmethod
    def extract_from_case(text):
        """Trích xuất bit từ chữ hoa/thường"""
        return '1' if text.isupper() else '0'