import pygame as pg
class Car:
    def __init__(self):
        # 車の初期位置を設定
        self.position = (100, 100)  # 例としての初期値
        self.path = [self.position]  # 車の軌跡を保存するリスト

    def move(self, new_position):
        # 車を新しい位置に移動させるメソッド
        self.position = new_position
        self.path.append(new_position)

    def draw_path(self, screen):
        # 車の軌跡を描画するメソッド
        if len(self.path) > 1:
            pg.draw.lines(screen, (255, 0, 0), False, self.path, 2)