MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Инвертируем словарь для обратного перевода
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    """Перевод текста в азбуку Морзе с переносом слов на новую строку."""
    text = text.upper()
    morse_code = '\n'.join(' '.join(MORSE_CODE_DICT[char] for char in word if char in MORSE_CODE_DICT) for word in text.split())
    return morse_code

def morse_to_text():
    """Перевод из азбуки Морзе в текст, ввод осуществляется построчно."""
    print("Введите код Морзе. Каждое слово вводите с новой строки. Для завершения ввода оставьте строку пустой.")
    morse_words = []
    while True:
        line = input().strip()
        if line == "":
            break
        morse_words.append(line)
    
    decoded_message = ' '.join(
        ''.join(REVERSE_MORSE_CODE_DICT[char] for char in word.split() if char in REVERSE_MORSE_CODE_DICT)
        for word in morse_words
    )
    return decoded_message

def auto_translate(input_text):
    """Автоматический выбор перевода в зависимости от первого символа."""
    input_text = input_text.strip()
    if input_text[0].isalpha() or input_text[0].isdigit():
        return text_to_morse(input_text)
    elif input_text[0] in ['.', '-']:
        return morse_to_text()
    else:
        return "Неверный формат ввода."

# Пример использования
if __name__ == "__main__":
    print("Введите текст для перевода. Если это текст, каждое слово будет переведено в Морзе с новой строки.\nЕсли это Морзе, каждое слово вводите с новой строки, завершите ввод пустой строкой.")
    input_text = input("Ваш ввод: ").strip()
    if input_text[0].isalpha() or input_text[0].isdigit():
        print("Результат перевода в Морзе:")
        print(text_to_morse(input_text))
    elif input_text[0] in ['.', '-']:
        print("Результат перевода из Морзе:")
        print(morse_to_text())
    else:
        print("Неверный формат ввода.")
