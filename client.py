import poplib
import email


def get_body(b):
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return part.get_payload(decode=True)
    else:
        return b.get_payload(decode=True)


def main():
    print('Server: ')
    server = input()  # "pop.yandex.ru"
    print('Login: ')
    login = input()  # "server5mtp"
    print('Pass: ')
    password = input()  # "1q1a2w2s"

    box = poplib.POP3_SSL(server)
    box.user(login)
    box.pass_(password)

    idx = 1

    while 1:
        print('Command: ')
        c = input()
        if c == 'headers':
            lines = box.top(str(idx), 0)[1]
            for line in lines:
                print(line.decode('utf-8'))

        elif c == 'top':
            print('Number of lines: ')
            n = int(input())
            header_size = len(box.top(str(idx), 0)[1])
            lines = box.top(str(idx), n)[1]
            for line in lines[header_size:]:
                if line:
                    print(line.decode('utf-8'))

        elif c == 'body':
            lines = box.retr(str(idx))[1]
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = email.message_from_string(msg_content)
            print(get_body(msg).decode('utf-8'))

        elif c == 'save':
            lines = box.retr(str(idx))[1]
            with open('email', 'wb') as file:
                file.writelines(lines)
        elif c == 'exit':
            break

    box.quit()


if __name__ == '__main__':
    main()

