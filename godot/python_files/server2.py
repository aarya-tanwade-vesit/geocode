import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5000))

print("Waiting for Godot...")

while True:
    data, address = sock.recvfrom(1024)

    message = data.decode()
    x, y = map(float, message.split(","))

    print(f"Target: X={x:.1f}, Y={y:.1f}")