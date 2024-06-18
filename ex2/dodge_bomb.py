import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1300, 800
way = {pg.K_UP:(0, -5), 
       pg.K_DOWN:(0, +5), 
       pg.K_LEFT:(-5, 0), 
       pg.K_RIGHT:(+5, 0),
       } #移動時の方向記憶辞書


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bomn(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect、または爆弾Rect
    戻り値：真理値タプル(横方向、縦方向)
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def kk_angle(sum_mv):
    img = pg.image.load("fig/3.png")
    angle = {(-5, 0) : pg.transform.rotozoom(img, 0, 2.0),   #左
            (-5, -5) : pg.transform.rotozoom(img, 315, 2.0), #左上
            (-5, +5) : pg.transform.rotozoom(img, 45, 2.0),  #左下
            (0, +5) : pg.transform.rotozoom(img, 90, 2.0),  #下
            (+5, 0) : pg.transform.rotozoom(img, 0, 2.0),    #右
            (+5, +5) : pg.transform.rotozoom(img, 45, 2.0),  #右下
            (+5, -5) : pg.transform.rotozoom(img, 315, 2.0), #右上
            (0, -5) : pg.transform.rotozoom(img, 270, 2.0),   #上
            }
    if sum_mv == [0, 0]:
        return pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
        
    for n, im in angle.items():
        if sum_mv[0] == n[0] and sum_mv[1] == n[1]:
            if n[0] >= 0:
                im = pg.transform.flip(im, True, False)
            return im


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, v in way.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1] #way回転
        
        
    
        kk_rct.move_ip(sum_mv)
        if check_bomn(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        screen.blit(kk_img, kk_rct)
        kk_img = kk_angle(sum_mv)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bomn(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
