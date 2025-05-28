"""
This module defines what needs to be done before starting testing
"""
import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from app.gui.utils.loader import loader

loader.load_images()
