# Top-Down Zombie Shooter

A fast-paced, 2D top-down arcade survival shooter built with Python and **Pygame**. Defend your base against escalating waves of zombies using an arsenal of three distinct weapons!

---

## 🎮 Gameplay Overview

In **Shooter**, your goal is to survive as long as possible while racking up the highest score. Zombies spawn at the top of the screen and march downward toward your base. 

* **Health System:** You start with **10 HP**, displayed by the red health bar at the bottom of the screen. You lose 1 HP if a zombie reaches the bottom border or collides directly with you.
* **Difficulty Progression:** For every **10 zombies** you eliminate, the game advances to the next level (up to **Level 3**), introducing tougher zombie variants with higher health pools and higher point values.

---

## 🔫 Arsenal & Weapon Stats

Switch between three different weapons on the fly to adapt to different enemy types:

| Key | Weapon | Damage | Bullet Speed | Reload Cooldown | Best Used For |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **`1`** | **Pistol** | 1 | Fast (`10`) | 0.5s (`30` frames) | Balanced accuracy & speed |
| **`2`** | **Bazooka** | 3 | Slow (`5`) | 1.0s (`60` frames) | One-shotting Level 3 zombies |
| **`3`** | **Minigun** | 1 | Medium (`8`) | 0.25s (`15` frames) | Rapid-fire crowd control |

---

## 🧟 Enemy Types

As you level up, stronger zombies begin appearing in the wave:

* **Level 1 Zombie (`zombie1.png`):** 1 HP | Awards **1 point**
* **Level 2 Zombie (`zombie2.png`):** 2 HP | Awards **2 points** *(Starts appearing at Level 2)*
* **Level 3 Zombie (`zombie3.png`):** 3 HP | Awards **3 points** *(Starts appearing at Level 3)*

---

## 🕹️ Controls

* **Move Up:** `W`
* **Move Down:** `S`
* **Move Left:** `A`
* **Move Right:** `D`
* **Shoot:** `Spacebar`
* **Equip Pistol:** `1`
* **Equip Bazooka:** `2`
* **Equip Minigun:** `3`

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have **Python 3.x** installed on your system, along with the `pygame` library.

1. **Install Pygame:**
   ```bash
   pip install pygame
   ```

2. **Verify Project Structure:**
   Ensure all required image and audio assets are located in the same directory as `shooting.py`:
   ```text
   ├── shooting.py          # Main game script
   ├── map1.png             # Background map
   ├── gun1.png             # Pistol sprite
   ├── gun2.png             # Bazooka sprite
   ├── gun3.png             # Minigun sprite
   ├── zombie1.png          # Level 1 zombie sprite
   ├── zombie2.png          # Level 2 zombie sprite
   ├── zombie3.png          # Level 3 zombie sprite
   ├── bullet.png           # Projectile sprite
   ├── back_music.ogg       # Background soundtrack
   └── destroy_sound.ogg    # Zombie elimination sound effect
   ```

3. **Run the Game:**
   ```bash
   python shooting.py
   ```
