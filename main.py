import pygame
import numpy as np
import math
# LƯU Ý khi làm việc với vector trong numpy phải ép kiểu dữ liệu về float64 để tránh trường hợp tự làm chẵn số khi thực hiện phép nhân
pygame.init()
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
CIRCLE_CENTER = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64)
CIRCLE_RADIUS = 150
BALL_RADIUS = 5
ball_postion = np.array([WIDTH/2, HEIGHT/2 - 120], dtype=np.float64)
running  = True
GRAVITY = 0.2
# Vận tốc ban đầu của quả bóng Velocity
ball_velocity = np.array([0,0], dtype=np.float64)

# BƯỚC 5: Tạo 1 tam giác gọi là dây dung với độ mở là 60 độ, chồng lên trên hình tròn, đỉnh
# của tam giác sẽ là tâm đường tròn

arc_deg = 60
# Đỉnh 1 là tâm hình tròn, Đỉnh 2 gọi là Start, Đỉnh 3 gọi là End
start_angle = math.radians(-arc_deg / 2)
end_angel = math.radians(arc_deg / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ball_velocity[1] += GRAVITY
    # ball_postion[0] += ball_velocity[0]
    # ball_postion[1] += ball_velocity[1]
    # Do đã dùng Numpy vector nên có thể rút gọn 2 đoạn code trên thành 1 dòng như dưới đây
    ball_postion += ball_velocity

    # linalg = Linear Algebra (Đại số tuyến tính), norm = normarlize (chuẩn hóa) của vector hoặc ma trận
    # Hàm norm sẽ tính độ dài của vector từ Ball Position đến Tâm hình tròn
    distance = np.linalg.norm(ball_postion - CIRCLE_CENTER)

    # Logic khi bóng chạm vào hình tròn
    if distance + BALL_RADIUS > CIRCLE_RADIUS:

        # BƯỚC 1: tính ra vector d: từ tâm hình tròn đến vị trí quả bóng chạm vào vành hình tròn
        d = ball_postion - CIRCLE_CENTER
        # Vector đơn vị của d
        d_unit = d / np.linalg.norm(d)
        # Vector đơn vị của d dùng để reset position của quả bóng, khi tốc độ quá cao, bóng có thể
        # sẽ đi ra khỏi viền hình tròn, nên đoạn code bên dưới sẽ reset lại vị trí mỗi khi quả bóng
        # vượt ra khỏi hình tròn
        ball_postion = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
        # BƯỚC 2: tính vector t ~ vector tiếp tuyến với vị trí quả bóng chạm vành hình tròn
        # Công thức: vị trí của d[x,y] => t sẽ là t[-y, x], công thức đã được chứng minh toán học
        # Ép kiểu thành chuỗi numby float64 để tránh lỗi khi thực hiện phép nhân
        t = np.array([-d[1],d[0]], dtype=np.float64)

        # BƯỚC 3: tính hình chiều của vector d xuống vector t
        # Công thức: dùng hàm dot của numpy để tính tích vô hướng của 2 vector
        projection_v_t = (np.dot(ball_velocity, t)/np.dot(t,t)) * t

        # BƯỚC 4: tính vận tốc mới
        ball_velocity = 2 * projection_v_t - ball_velocity

    window.fill(BLACK)
    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)
    pygame.draw.circle(window, RED, ball_postion, BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()