import pygame
import numpy as np
import math
import random
class Ball:
    def __init__(self, postion, velocity):
        self.pos = np.array(postion, dtype=np.float64)
        self.vel = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_in = True
        
# LƯU Ý khi làm việc với vector trong numpy phải ép kiểu dữ liệu về float64 để tránh trường hợp tự làm chẵn số khi thực hiện phép nhân

# Tính xem quả bóng đã chạm vào nơi hở của đường tròn hay chưa
def is_ball_in_arc(ball_position, CIRCLE_CENTER, start_angle, end_angle):
    dx = ball_position[0] - CIRCLE_CENTER[0]
    dy = ball_position[1] - CIRCLE_CENTER[1]
    # Tính góc của quả bóng
    # Hàm atan2 sẽ trả về góc giữa 2 điểm, góc này sẽ nằm trong khoảng từ -pi đến pi
    ball_angle = math.atan2(dy, dx)
    # Normalize góc của quả bóng vì nếu không mod cho 2pi, góc sẽ luôn tục cộng dồn thành
    # một góc rất lớn
    start_angle = start_angle % (2 * math.pi)
    end_angel = end_angle % (2 * math.pi)
    # Ép end_angle *2pi để end_angle về 1 góc luôn lớn hơn start_angle
    if start_angle > end_angel:
        end_angel += 2 * math.pi
    if start_angle < ball_angle < end_angel or (start_angle <= ball_angle + 2 * math.pi <= end_angel):
        return True
    
# Hàm vẽ tam giác
def draw_arc(window, center, radius, start_angle, end_angle):
    p1 = center + (radius +1000) * np.array([math.cos(start_angle), math.sin(start_angle)], dtype=np.float64)
    p2 = center + (radius +1000) * np.array([math.cos(end_angle), math.sin(end_angle)], dtype=np.float64)
    pygame.draw.polygon(window, BLACK, [center, p1, p2], 0)


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
# Set tốc độ quay của hình tam giác 
spinning_speed = 0.01
# Logic của is_ball_in_arc là khi quả bóng chạm vào dây cung, góc của quả bóng sẽ nằm trong khoảng
# góc của hình tam giác, thì ta sẽ xem quả bóng đã ở ngoài hình tròn & để nó tiếp tục rơi
balls = [Ball(ball_postion, ball_velocity)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    start_angle += spinning_speed
    end_angel += spinning_speed
    for ball in balls:
        if ball.pos[1] > HEIGHT or ball.pos[0] < 0 or ball.pos[0] > WIDTH or ball.pos[1] < 0:
            balls.remove(ball)
            balls.append(Ball(postion=[WIDTH/2, HEIGHT/2 - 120], velocity=[random.uniform(-4,4), random.uniform(-1,1)]))
            balls.append(Ball(postion=[WIDTH/2, HEIGHT/2 - 120], velocity=[random.uniform(-4,4), random.uniform(-1,1)]))
        ball.vel[1] += GRAVITY
        # ball_postion[0] += ball.vel[0]
        # ball_postion[1] += ball.vel[1]
        # Do đã dùng Numpy vector nên có thể rút gọn 2 đoạn code trên thành 1 dòng như dưới đây
        ball.pos += ball.vel

        # linalg = Linear Algebra (Đại số tuyến tính), norm = normarlize (chuẩn hóa) của vector hoặc ma trận
        # Hàm norm sẽ tính độ dài của vector từ Ball Position đến Tâm hình tròn
        distance = np.linalg.norm(ball.pos - CIRCLE_CENTER)

        # Logic khi bóng chạm vào hình tròn
        if distance + BALL_RADIUS > CIRCLE_RADIUS:
            # ĐẦU TIÊN: check xem quả bóng có chạm đường tròn & có ở giữa 2 cái góc của tam giác hay không
            if is_ball_in_arc(ball.pos, CIRCLE_CENTER, start_angle, end_angel):
                ball.is_in = False
            if ball.is_in:
                # BƯỚC 1: tính ra vector d: từ tâm hình tròn đến vị trí quả bóng chạm vào vành hình tròn
                d = ball.pos - CIRCLE_CENTER
                # Vector đơn vị của d
                d_unit = d / np.linalg.norm(d)
                # Vector đơn vị của d dùng để reset position của quả bóng, khi tốc độ quá cao, bóng có thể
                # sẽ đi ra khỏi viền hình tròn, nên đoạn code bên dưới sẽ reset lại vị trí mỗi khi quả bóng
                # vượt ra khỏi hình tròn
                ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
                # BƯỚC 2: tính vector t ~ vector tiếp tuyến với vị trí quả bóng chạm vành hình tròn
                # Công thức: vị trí của d[x,y] => t sẽ là t[-y, x], công thức đã được chứng minh toán học
                # Ép kiểu thành chuỗi numby float64 để tránh lỗi khi thực hiện phép nhân
                t = np.array([-d[1],d[0]], dtype=np.float64)

                # BƯỚC 3: tính hình chiều của vector d xuống vector t
                # Công thức: dùng hàm dot của numpy để tính tích vô hướng của 2 vector
                projection_v_t = (np.dot(ball.vel, t)/np.dot(t,t)) * t

                # BƯỚC 4: tính vận tốc mới
                ball.vel = 2 * projection_v_t - ball.vel
                # Tăng vận tốc quả bóng khi chạm vào đường tròn dựa theo công thức ( v = r*w (w là tốc độ quay)
                # ) gia tăng lực kéo tiếp tuyến
                ball.vel += t * spinning_speed 
    window.fill(BLACK)
    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)
    # Vẽ tam giác đè lên hình tròn
    draw_arc(window, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angel)
    for ball in balls:
        pygame.draw.circle(window, ball.color, ball.pos, BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()