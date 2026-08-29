# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# sock.sendto(
#     b"Hello from Python!",
#     ("127.0.0.1", 9999)
# )

# print("Message sent!")



#part 2
# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# number = 42

# sock.sendto(
#     str(number).encode(),
#     ("127.0.0.1", 9999)
# )

# print("Sent:", number)


#part 3
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = 100
y = 250

message = f"{x},{y}"

sock.sendto(
    message.encode(),
    ("127.0.0.1", 9999)
)

print("Sent:", message)