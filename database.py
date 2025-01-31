import sqlite3
import os
from classes.object_classes.enemy_classes import Enemy, Enemy_Shooter
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.wall_classes import Wall
from classes.object_classes.base_classes import Base, Cannon


def initialize_database():

    # Подключаемся к базе данных
    conn = sqlite3.connect('data/game_state.db')
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS base_state (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            health INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enemies (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            health INTEGER,
            type TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mirrors (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            orientation INTEGER,
            health INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS walls (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            health INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def save_game_state(base, enemies, mirrors, walls):
    conn = sqlite3.connect('data/game_state.db')
    cursor = conn.cursor()

    # Очистка старых данных
    cursor.execute('DELETE FROM base_state')
    cursor.execute('DELETE FROM enemies')
    cursor.execute('DELETE FROM mirrors')
    cursor.execute('DELETE FROM walls')

    # Сохранение состояния базы
    cursor.execute('''
        INSERT INTO base_state (x, y, health)
        VALUES (?, ?, ?)
    ''', (base.x, base.y, base.health))

    # Сохранение состояния врагов
    for enemy in enemies:
        cursor.execute('''
            INSERT INTO enemies (x, y, health, type)
            VALUES (?, ?, ?, ?)
        ''', (enemy.x, enemy.y, enemy.health, enemy.__class__.__name__))

    # Сохранение состояния зеркал
    for mirror in mirrors:
        cursor.execute('''
            INSERT INTO mirrors (x, y, orientation, health)
            VALUES (?, ?, ?, ?)
        ''', (mirror.x, mirror.y, mirror.orientation, mirror.health))

    # Сохранение состояния стен
    for wall in walls:
        cursor.execute('''
            INSERT INTO walls (x, y, health)
            VALUES (?, ?, ?)
        ''', (wall.x, wall.y, wall.health))

    conn.commit()
    conn.close()

def load_game_state():
    conn = sqlite3.connect('data/game_state.db')
    cursor = conn.cursor()

    # Загрузка состояния базы
    cursor.execute('SELECT x, y, health FROM base_state')
    base_data = cursor.fetchone()
    if base_data:
        base = Base([Cannon(9, 8, -90), Cannon(9, 10, 90), Cannon(8, 9, 180), Cannon(10, 9, 0)])
        base.x, base.y, base.health = base_data

    # Загрузка состояния врагов
    cursor.execute('SELECT x, y, health, type FROM enemies')
    enemies_data = cursor.fetchall()
    enemies = []
    for enemy_data in enemies_data:
        x, y, health, enemy_type = enemy_data
        if enemy_type == 'Enemy':
            enemy = Enemy(x, y, None, None, health=health)  # Передаем None для boards, так как они будут установлены позже
        elif enemy_type == 'EnemyShooter':
            enemy = Enemy_Shooter(x, y, None, None, health=health)
        enemies.append(enemy)

    # Загрузка состояния зеркал
    cursor.execute('SELECT x, y, orientation, health FROM mirrors')
    mirrors_data = cursor.fetchall()
    mirrors = []
    for mirror_data in mirrors_data:
        x, y, orientation, health = mirror_data
        mirror = Mirror(x, y, orientation, None, health=health)  # Передаем None для board
        mirrors.append(mirror)

    # Загрузка состояния стен
    cursor.execute('SELECT x, y, health FROM walls')
    walls_data = cursor.fetchall()
    walls = []
    for wall_data in walls_data:
        x, y, health = wall_data
        wall = Wall(x, y, None, health=health)  # Передаем None для board
        walls.append(wall)

    conn.close()
    return base, enemies, mirrors, walls