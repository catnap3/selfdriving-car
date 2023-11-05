import pygame as pg
import sys
import matplotlib
from Car import Car  # Car.pyモジュールからCarクラスをインポート

# 車の移動速度
auto_speed = 40

# グリッドサイズ
grid_size = 40

# ゲームループの前に、前回のフレームからの経過時間を測るための変数を初期化
last_time = pg.time.get_ticks()

# 初期設定
pg.init()
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Driving You to the Destination")
clock = pg.time.Clock()
car = Car()

# 車の画像をロード
car_image = pg.image.load('car.png')  
original_size = car_image.get_size()

# 縮小したい幅を設定
desired_width = 50
aspect_ratio = original_size[1] / original_size[0]

# 縦横比を保った新しいサイズを計算
new_size = (desired_width, int(desired_width * aspect_ratio))

# 画像を新しいサイズにスケール
car_image = pg.transform.scale(car_image, new_size)
car_rect = car_image.get_rect()
car_rect.center = (width // 2, height // 2)

# FamilyMartの画像をロード
familymart_image = pg.image.load('familymart.jpeg')

# 縮小したい幅を設定
desired_width = 50
original_fm_size = familymart_image.get_size()
aspect_ratio = original_size[1] / original_size[0]

# 縦横比を保った新しいサイズを計算
new_size = (desired_width, int(desired_width * aspect_ratio))

# 画像を新しいサイズにスケール
familymart_image = pg.transform.scale(familymart_image, new_size)

# 画像のrectを取得し、希望の位置に配置
familymart_rect = familymart_image.get_rect()
familymart_rect.topleft = (40, 40)

# 郵便局の画像をロード
post_office_image = pg.image.load('post_office.png')
# ここで座標を指定します
post_office_rect = post_office_image.get_rect()
post_office_rect.topleft = (30, 20)

# 縮小したい幅を設定
desired_width = 50
original_fm_size = post_office_image.get_size()
aspect_ratio = original_size[1] / original_size[0]

# 縦横比を保った新しいサイズを計算
new_size = (desired_width, int(desired_width * aspect_ratio))

# 画像を新しいサイズにスケール
post_office_image = pg.transform.scale(post_office_image, new_size)

# 画像のrectを取得し、希望の位置に配置
post_office_rect = post_office_image.get_rect()
post_office_rect.topleft = (730, 200)

# 衝突検出のための変数を追加
at_familymart = False
at_post_office = False

# グリッドの描画関数
def draw_grid():
    for x in range(0, width, 40):  # 40ピクセルごとに縦線を引く
        pg.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
    for y in range(0, height, 40):  # 40ピクセルごとに横線を引く
        pg.draw.line(screen, (200, 200, 200), (0, y), (width, y))

# 車を動かす際の境界値を設定
CAR_SPEED = 10
left_boundary = car_rect.width // 2
right_boundary = width - car_rect.width // 2
top_boundary = car_rect.height // 2
bottom_boundary = height - car_rect.height // 2

# フォントの設定
pg.font.init()  # フォントモジュールの初期化
myfont = pg.font.SysFont('Arial', 30)

# 目的地の変数を初期化
destination_x, destination_y = None, None

# 車の経路を記録するためのリスト
car_path = []

# ゲームループ
while True:
    # 経過時間（ミリ秒）を計算
    current_time = pg.time.get_ticks()
    dt = current_time - last_time
    last_time = current_time

    # 車の経路を描画する関数
    def draw_path(screen):
        if len(car_path) > 1:
            pg.draw.lines(screen, (255, 0, 0), False, car_path, 5)

    # 車の経路を更新する関数（車が動くたびに呼び出す）
    def update_path(position):
        car_path.append(position)
  
    # 自動移動の処理の前に、目的地が設定されているかをチェック
    if destination_x is not None and destination_y is not None:
        # 自動移動の処理
        move_distance = auto_speed * dt/1000  # 移動距離 = 速度 × 経過時間

    # X方向の移動
    if destination_x is not None:
        if car_rect.x < destination_x:
            car_rect.x += min(move_distance, destination_x - car_rect.x)
            print(car_rect.x)
        elif car_rect.x > destination_x:
            car_rect.x -= min(move_distance, car_rect.x - destination_x)
    
    # Y方向の移動
    if destination_y is not None:
        if car_rect.y < destination_y:
            car_rect.y += min(move_distance, destination_y - car_rect.y)
        elif car_rect.y > destination_y:
            car_rect.y -= min(move_distance, car_rect.y - destination_y)    
    
    # 車が目的地に到達したかどうかを判定するフラグ
    at_destination = False
    if destination_x is not None and destination_y is not None:
        at_destination = car_rect.x == destination_x and car_rect.y == destination_y

    # 車が目的地に到達したら、グリッドにスナップさせる
    if at_destination:
        car_rect.x = (car_rect.x // grid_size) * grid_size
        car_rect.y = (car_rect.y // grid_size) * grid_size
        # 目的地をリセット（次の目的地を設定するまで）
        destination_x, destination_y = None, None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:  # マウスのボタンが押されたとき
            if event.button == 1:  # 左クリックの場合
                # クリックされた位置を目的地として設定
                destination_x, destination_y = event.pos
                # 目的地を罫線上に設定
                destination_x = (destination_x // grid_size) * grid_size
                destination_y = (destination_y // grid_size) * grid_size
                print(f"New destination set to: {destination_x}, {destination_y}")

    # 画面の更新
    screen.fill((255, 255, 255))  # 白色で画面をクリア
    draw_grid()  # グリッドを描画
    screen.blit(familymart_image, familymart_rect)  # FamilyMartの画像を描画
    screen.blit(post_office_image, post_office_rect)  # 郵便局の画像を描画
    screen.blit(car_image, car_rect)  # 車の新しい位置を画面に描画
    if destination_x is not None and destination_y is not None:
        pg.draw.rect(screen, (255, 0, 0), (destination_x, destination_y, grid_size, grid_size), 2)# 目的地を示す赤い四角形を描画
    
    # 車とFamilyMartの衝突を検出
    if car_rect.colliderect(familymart_rect):
        at_familymart = True

    # 車と郵便局の衝突を検出
    if car_rect.colliderect(post_office_rect):
        at_post_office = True

    # 車と郵便局の衝突を検出
    if car_rect.x== destination_x and car_rect.y == destination_y:
        at_destination = True

    # 衝突が発生した場合のテキスト描画
    if at_familymart:
        goal_text = "Enjoy Shopping!"
        text_surface = myfont.render(goal_text, True, (255, 0, 0))  # 赤色のテキストを作成
        text_rect = text_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(text_surface, text_rect)  # テキストを画面の中央に描画
    
    elif at_post_office:
        goal_text = "post_office"
        text_surface = myfont.render(goal_text, True, (255, 0, 0))  # 赤色のテキストを作成
        text_rect = text_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(text_surface, text_rect)  # テキストを画面の中央に描画

    elif at_destination:
        goal_text = "We've got to the destinataion!"
        text_surface = myfont.render(goal_text, True, (255, 0, 0))  # 赤色のテキストを作成
        text_rect = text_surface.get_rect(center=(width / 2, height / 2))
        screen.blit(text_surface, text_rect)  # テキストを画面の中央に描画


    pg.display.flip()
    # フレームレートの設定
    clock.tick(20)
pg.quit()