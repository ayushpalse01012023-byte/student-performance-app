import tkinter as tk
from tkinter import messagebox
import math
import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Vec2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)


class Terrain:
    """Generate and store the hill terrain"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.points: List[Tuple[float, float]] = []
        self.generate_terrain()
    
    def generate_terrain(self):
        """Generate a smooth, bumpy hill terrain"""
        self.points = []
        for x in range(self.width + 1):
            # Create a base hill shape
            base_height = self.height * 0.7 - (x / self.width) * 200
            
            # Add smooth bumps using sine waves
            bump1 = 30 * math.sin(x / 40)
            bump2 = 20 * math.sin(x / 80 + 2)
            bump3 = 15 * math.sin(x / 120 + 4)
            
            y = base_height + bump1 + bump2 + bump3
            self.points.append((x, min(y, self.height - 50)))
    
    def get_height_at(self, x: float) -> float:
        """Get terrain height at a specific x position"""
        if x < 0 or x >= self.width:
            return self.height
        
        idx = int(x)
        if idx >= len(self.points) - 1:
            return self.points[-1][1]
        
        # Linear interpolation between points
        x1, y1 = self.points[idx]
        x2, y2 = self.points[idx + 1]
        t = x - idx
        return y1 + (y2 - y1) * t
    
    def get_slope_at(self, x: float) -> float:
        """Get terrain slope (angle) at position"""
        if x < 0 or x >= self.width - 1:
            return 0
        
        idx = int(x)
        if idx >= len(self.points) - 1:
            return 0
        
        x1, y1 = self.points[idx]
        x2, y2 = self.points[idx + 1]
        return (y2 - y1) / (x2 - x1)


class Car:
    """The player's car with physics"""
    def __init__(self, x: float, y: float):
        self.pos = Vec2(x, y)
        self.vel = Vec2(0, 0)
        self.acc = Vec2(0, 0)
        self.angle = 0  # Rotation angle
        self.width = 30
        self.height = 15
        self.fuel = 100
        self.max_fuel = 100
        self.speed = 0
        self.damage = 0
        self.distance_traveled = 0
        self.last_x = x
    
    def update(self, terrain: Terrain, keys: dict, dt: float):
        """Update car physics"""
        # Input handling
        acceleration = 0
        if keys.get('up', False):
            acceleration = 800  # Forward acceleration
            self.fuel = max(0, self.fuel - 2 * dt)
        elif keys.get('down', False):
            acceleration = -300  # Reverse
            self.fuel = max(0, self.fuel - 1 * dt)
        
        # Rotation
        if keys.get('left', False):
            self.angle += 5
        if keys.get('right', False):
            self.angle -= 5
        
        # Keep angle reasonable
        self.angle = self.angle % 360
        
        # Apply acceleration based on car angle
        rad = math.radians(self.angle)
        self.acc.x = acceleration * math.cos(rad)
        self.acc.y = acceleration * math.sin(rad)
        
        # Gravity
        self.acc.y += 1500
        
        # Air resistance
        if self.vel.length() > 0:
            resistance = self.vel * (-0.1)
            self.acc = self.acc + resistance
        
        # Update velocity
        self.vel = self.vel + self.acc * dt
        self.vel.x *= 0.98  # Friction
        
        # Update position
        new_pos = self.pos + self.vel * dt
        
        # Get terrain height at new position
        terrain_y = terrain.get_height_at(new_pos.x)
        
        # Collision with terrain
        if new_pos.y > terrain_y:
            new_pos.y = terrain_y
            
            # Get terrain slope for bounce
            slope = terrain.get_slope_at(new_pos.x)
            slope_rad = math.atan(slope)
            
            # Bounce (inelastic)
            bounce_factor = 0.3
            speed = self.vel.length()
            
            # Reflect velocity based on slope
            normal_x = -math.sin(slope_rad)
            normal_y = math.cos(slope_rad)
            
            dot = self.vel.x * normal_x + self.vel.y * normal_y
            self.vel.x = (self.vel.x - dot * normal_x * 2) * bounce_factor
            self.vel.y = (self.vel.y - dot * normal_y * 2) * bounce_factor
            
            # Damage on impact
            if speed > 300:
                impact_damage = min(50, (speed - 300) / 100)
                self.damage = min(100, self.damage + impact_damage)
        
        self.pos = new_pos
        
        # Clamp to screen
        self.pos.x = max(0, min(new_pos.x, 1200))
        
        # Track distance
        distance_delta = self.pos.x - self.last_x
        self.distance_traveled += distance_delta
        self.last_x = self.pos.x
        
        # Game over condition
        if self.damage >= 100:
            return False
        if self.fuel <= 0:
            return False
        
        return True


class HillClimberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hill Climber Racing")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        self.won = False
        
        # Canvas
        self.canvas = tk.Canvas(root, width=1200, height=800, bg='lightblue')
        self.canvas.pack()
        
        # Input handling
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
        }
        
        self.root.bind('<KeyPress-Up>', lambda e: self.keys.update({'up': True}))
        self.root.bind('<KeyRelease-Up>', lambda e: self.keys.update({'up': False}))
        self.root.bind('<KeyPress-Down>', lambda e: self.keys.update({'down': True}))
        self.root.bind('<KeyRelease-Down>', lambda e: self.keys.update({'down': False}))
        self.root.bind('<KeyPress-Left>', lambda e: self.keys.update({'left': True}))
        self.root.bind('<KeyRelease-Left>', lambda e: self.keys.update({'left': False}))
        self.root.bind('<KeyPress-Right>', lambda e: self.keys.update({'right': True}))
        self.root.bind('<KeyRelease-Right>', lambda e: self.keys.update({'right': False}))
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<r>', self.restart_game)
        
        # Initialize game objects
        self.terrain = Terrain(2000, 800)
        self.car = Car(100, 400)
        self.time = 0
        self.win_distance = 1800
        
        # Start game loop
        self.update_game()
    
    def toggle_pause(self, event=None):
        self.paused = not self.paused
    
    def restart_game(self, event=None):
        self.terrain = Terrain(2000, 800)
        self.car = Car(100, 400)
        self.time = 0
        self.game_over = False
        self.won = False
    
    def update_game(self):
        if not self.paused and not self.game_over:
            dt = 0.016  # ~60 FPS
            self.time += dt
            
            # Update car
            car_alive = self.car.update(self.terrain, self.keys, dt)
            if not car_alive:
                self.game_over = True
            
            # Check win condition
            if self.car.distance_traveled >= self.win_distance:
                self.game_over = True
                self.won = True
        
        # Render
        self.render()
        
        # Schedule next frame
        self.root.after(16, self.update_game)
    
    def render(self):
        self.canvas.delete('all')
        
        # Draw sky
        self.canvas.create_rectangle(0, 0, 1200, 400, fill='lightblue')
        
        # Calculate camera position (follow car)
        camera_x = max(0, min(self.car.pos.x - 300, self.terrain.width - 1200))
        
        # Draw terrain
        terrain_points = []
        for i, (x, y) in enumerate(self.terrain.points):
            screen_x = x - camera_x
            if -50 < screen_x < 1250:
                terrain_points.append((screen_x, y))
        
        if len(terrain_points) > 1:
            self.canvas.create_polygon(
                terrain_points + [(terrain_points[-1][0], 800), (terrain_points[0][0], 800)],
                fill='green',
                outline='darkgreen',
                width=2
            )
        
        # Draw car
        car_screen_x = self.car.pos.x - camera_x
        car_screen_y = self.car.pos.y
        
        # Car body
        rad = math.radians(self.car.angle)
        corners = [
            (-self.car.width/2, -self.car.height/2),
            (self.car.width/2, -self.car.height/2),
            (self.car.width/2, self.car.height/2),
            (-self.car.width/2, self.car.height/2),
        ]
        
        rotated_corners = [
            (car_screen_x + x*math.cos(rad) - y*math.sin(rad),
             car_screen_y + x*math.sin(rad) + y*math.cos(rad))
            for x, y in corners
        ]
        
        color = 'red' if self.car.damage > 50 else 'yellow'
        self.canvas.create_polygon(rotated_corners, fill=color, outline='black', width=2)
        
        # Draw wheels
        wheel_offset = 0.4
        wheel_rad = 4
        wheels = [
            (-self.car.width/2 * wheel_offset, -self.car.height/2),
            (-self.car.width/2 * wheel_offset, self.car.height/2),
            (self.car.width/2 * wheel_offset, -self.car.height/2),
            (self.car.width/2 * wheel_offset, self.car.height/2),
        ]
        for wx, wy in wheels:
            rx = car_screen_x + wx*math.cos(rad) - wy*math.sin(rad)
            ry = car_screen_y + wx*math.sin(rad) + wy*math.cos(rad)
            self.canvas.create_oval(rx-wheel_rad, ry-wheel_rad, 
                                   rx+wheel_rad, ry+wheel_rad, fill='black')
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over message
        if self.game_over:
            if self.won:
                self.canvas.create_text(
                    600, 200,
                    text="YOU WIN!",
                    font=('Arial', 48, 'bold'),
                    fill='green'
                )
                self.canvas.create_text(
                    600, 250,
                    text=f"Distance: {self.car.distance_traveled:.0f}m",
                    font=('Arial', 24),
                    fill='darkgreen'
                )
            else:
                self.canvas.create_text(
                    600, 200,
                    text="GAME OVER",
                    font=('Arial', 48, 'bold'),
                    fill='red'
                )
                reason = "Out of fuel!" if self.car.fuel <= 0 else "Too much damage!"
                self.canvas.create_text(
                    600, 250,
                    text=reason,
                    font=('Arial', 24),
                    fill='darkred'
                )
            
            self.canvas.create_text(
                600, 350,
                text="Press R to restart",
                font=('Arial', 20),
                fill='black'
            )
    
    def draw_hud(self):
        """Draw heads-up display"""
        # Distance
        self.canvas.create_text(
            20, 20,
            text=f"Distance: {self.car.distance_traveled:.0f}m / {self.win_distance}m",
            font=('Arial', 14),
            fill='black',
            anchor='nw'
        )
        
        # Speed (simplified)
        speed = self.car.vel.length() / 10
        self.canvas.create_text(
            20, 50,
            text=f"Speed: {speed:.1f}",
            font=('Arial', 14),
            fill='black',
            anchor='nw'
        )
        
        # Fuel bar
        self.canvas.create_rectangle(20, 80, 220, 100, outline='black', width=2)
        fuel_width = (self.car.fuel / self.car.max_fuel) * 200
        fuel_color = 'red' if self.car.fuel < 20 else 'green'
        self.canvas.create_rectangle(20, 80, 20 + fuel_width, 100, fill=fuel_color)
        self.canvas.create_text(
            130, 90,
            text=f"Fuel: {self.car.fuel:.0f}%",
            font=('Arial', 12, 'bold'),
            fill='black'
        )
        
        # Damage bar
        self.canvas.create_rectangle(20, 120, 220, 140, outline='black', width=2)
        damage_width = (self.car.damage / 100) * 200
        damage_color = 'red' if self.car.damage > 50 else 'orange' if self.car.damage > 25 else 'green'
        self.canvas.create_rectangle(20, 120, 20 + damage_width, 140, fill=damage_color)
        self.canvas.create_text(
            130, 130,
            text=f"Damage: {self.car.damage:.0f}%",
            font=('Arial', 12, 'bold'),
            fill='black'
        )
        
        # Instructions
        self.canvas.create_text(
            1180, 20,
            text="↑↓←→ Move | SPACE Pause | R Restart",
            font=('Arial', 10),
            fill='black',
            anchor='ne'
        )


if __name__ == '__main__':
    root = tk.Tk()
    game = HillClimberGame(root)
    root.mainloop()