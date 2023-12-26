import random

import pygame
import config
import math
import utilities

from player import Player
from npc import NPC
from game_state import GameState, CurrentGameState
from monsterfactory import MonsterFactory
from game_view.map import Map
from game_view.battle import Battle

# Se for adicionar novo sprites como obstáculos coloque aqui
obstacles = ['J', 'K', 'L', 'Z', 'N', 'B', 'C', 'V', 'R', 'E', 'T', 'U', 'I', 'A', 'S', 'D', 'Q']
# Areas de spam de monstros
monster_field = ["G"]
doors = ["D", "L", "g"]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.current_game_state = CurrentGameState.MAP
        self.player_has_moved = False
        self.monster_factory = MonsterFactory()
        self.map = Map(screen)
        self.battle = None
        self.file_name = "01"
        self.proximos = []

    def set_up(self):
        player = Player(2, 1)
        npc = NPC(1, 1, "../imgs/npc.png")
        self.player = player
        self.npc = npc
        self.objects.append(player)
        self.objects.append(npc)
        print("configure")
        self.game_state = GameState.RUNNING

        self.map.load(self.file_name)

    def update(self):
        if self.current_game_state == CurrentGameState.MAP:
            self.player_has_moved = False
            self.screen.fill(config.BLACK)
            self.handle_events()

            self.map.render(self.screen, self.player, self.objects)

            distance = 1
            for i in range(-distance, distance + 1):
                for j in range(-distance, distance + 1):
                    x = self.player.position[0] + j
                    y = self.player.position[1] + i
                    if 0 <= x < len(self.map.map_array[0]) and 0 <= y < len(self.map.map_array):
                        self.proximos.append(self.map.map_array[y][x])

            if any(item in doors for item in self.proximos):
                font = pygame.font.SysFont(None, 24)
                img = font.render("Pressione ENTER para entrar!", True, config.WHITE)
                self.screen.blit(img, (self.player.position[0] * config.SCALE - self.map.camera[0] * config.SCALE - 80,
                                       self.player.position[1] * config.SCALE - self.map.camera[1] * config.SCALE - 10))
                if "D" in self.proximos:
                    self.file_name = "02"
                if "L" in self.proximos:
                    self.file_name = "03"
                if "g" in self.proximos:
                    self.file_name = "01"
                self.proximos = []

            if self.player_has_moved:
                self.determine_game_events()

        elif self.current_game_state == CurrentGameState.BATTLE:
            self.battle.update()
            self.battle.render()

            if self.battle.monster.health <= 0:
                self.current_game_state = CurrentGameState.MAP

    def determine_game_events(self):
        map_tile = self.map.map_array[self.player.position[1]][self.player.position[0]]
        print(map_tile)

        self.determine_pokemon_found(map_tile)

    def determine_pokemon_found(self, map_tile):
        random_number = utilities.generate_random_number(1, 70)

        if random_number <= 2 and map_tile in monster_field:
            found_monster = self.monster_factory.create_monster(map_tile)
            print("Você encontrou um monstro!")
            print("Tipo: " + found_monster.type)
            print("Ataque: " + str(found_monster.attack))
            print("Vida: " + str(found_monster.health))

            self.battle = Battle(self.screen, found_monster, self.player)
            self.current_game_state = CurrentGameState.BATTLE

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w:
                    self.move_unit(self.npc, [0, -1])
                    self.move_unit(self.player, [0, -1])
                elif event.key == pygame.K_s:
                    self.move_unit(self.npc, [0, 1])
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_a:
                    self.move_unit(self.npc, [-1, 0])
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_d:
                    self.move_unit(self.npc, [1, 0])
                    self.move_unit(self.player, [1, 0])
                elif event.key == pygame.K_RETURN:
                    distance = 1
                    for i in range(-distance, distance + 1):
                        for j in range(-distance, distance + 1):
                            x = self.player.position[0] + j
                            y = self.player.position[1] + i
                            if 0 <= x < len(self.map.map_array[0]) and 0 <= y < len(self.map.map_array):
                                self.proximos.append(self.map.map_array[y][x])
                        if any(item in doors for item in self.proximos):
                            self.map.load(self.file_name)

    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]

        if new_position[0] < 0 or new_position[0] > (len(self.map.map_array[0]) - 1):
            return
        if new_position[1] < 0 or new_position[1] > (len(self.map.map_array) - 1):
            return

        if self.map.map_array[new_position[1]][new_position[0]] in obstacles:
            return

        if unit == self.npc:
            player_new_position = [self.player.position[0] + position_change[0],
                                   self.player.position[1] + position_change[1]]
            if player_new_position[0] < 0 or player_new_position[0] > (len(self.map.map_array[0]) - 1):
                return
            if player_new_position[1] < 0 or player_new_position[1] > (len(self.map.map_array) - 1):
                return
            if self.map.map_array[player_new_position[1]][player_new_position[0]] in obstacles:
                return

            if self.npc.position == self.player.position:
                return

        self.player_has_moved = True
        unit.update_position(new_position)
