import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5000))

GODOT = ("127.0.0.1", 4242)

CENTER_X = 640
CENTER_Y = 360

Kp = 0.002

print("Controller running...")

while True:

    data, address = sock.recvfrom(1024)

    x, y = map(float, data.decode().split(","))

    error_x = x - CENTER_X
    error_y = y - CENTER_Y

    pan = error_x * Kp
    tilt = error_y * Kp

    command = f"{pan},{tilt}"

    sock.sendto(command.encode(), GODOT)

    print(
        f"Target=({x:.0f},{y:.0f}) "
        f"Error=({error_x:.0f},{error_y:.0f}) "
        f"Command=({pan:.3f},{tilt:.3f})"
    )