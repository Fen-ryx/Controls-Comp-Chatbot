import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from matplotlib.animation import FuncAnimation

# def generate_pulley_sim(M1, M2):
def generate_pulley_sim():
    # Constants
    M1 = float(input("Enter M1 (kg): "))
    M2 = float(input("Enter M2 (kg): "))
    g = 9.81  # Acceleration due to gravity in m/s^2
    R = 0.5   # Radius of the pulley in m
    L1 = 1.5  # Length of thread on the side of M1 in m
    L2 = 1.0  # Length of thread on the side of M2 in m
    time_interval = 0.05  # Time interval for the simulation in seconds


    # Acceleration of the system (assuming a frictionless pulley)
    acceleration = g * (M2 - M1) / (M1 + M2)

    # Function to draw the pulley system
    def draw_pulley_system(ax, m1_pos, m2_pos):
        # Clear the axes for the new frame
        ax.clear()
        ax.set_facecolor('black')
        # Set the limits of the plot
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, L1 + L2 + 2*R + 0.5)


        # Draw the pulley
        pulley_circle = plt.Circle((1, L1 + L2 + R), R, color='white', fill=False)
        ax.add_patch(pulley_circle)
        # Draw the masses
        ax.plot(0.5, m1_pos, 'bo', ms=20)  # Mass 1
        ax.plot(1.5, m2_pos, 'ro', ms=20)  # Mass 2
        # floting text with the mass for indication 
        ax.text(0.0, m1_pos, f'{M1}kg', color='white', fontsize=12, ha='center')
        ax.text(2.0, m2_pos, f'{M2}kg', color='white', fontsize=12, ha='center')
        # Draw the strings
        ax.plot([0.5, 0.5], [m1_pos, L1 + L2 + R], color='white')  # String for Mass 1
        ax.plot([1.5, 1.5], [m2_pos, L1 + L2 + R], color='white')  # String for Mass 2
        

    def clamp(n, min, max): 
        if n < min: 
            return min
        elif n > max: 
            return max
        else: 
            return n 
        
    # Function to update the positions of the masses for each frame
    def update(frame):
        # Calculate the displacement
        displacement = 0.5 * acceleration * (frame * time_interval)**2
        # Calculate new positions
        # m1_pos = max(R, min(L2 + R - displacement, L1 + L2 + R))
        # m2_pos = max(R, min(L1 + R - displacement, L1 + L2 + R))
        m1_pos = clamp(L2 + R + displacement,R, L1 + L2 + R) 
        m2_pos = clamp(L1 + R - displacement,R, L1 + L2 + R) 
        # Draw the updated system
        draw_pulley_system(ax, m1_pos, m2_pos)
        return ax
        

    aspect_ratio = (L1 + L2 + R )/3.0

    # Create the figure and axes
    fig, ax = plt.subplots()
    # Draw the initial pulley system
    draw_pulley_system(ax, L2+R, L1+R)
    ax.set_aspect(aspect_ratio)
    # Start the animation
    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 100), interval=time_interval*1000, blit=False, repeat=False)

    #plt.show()

    # Set up formatting for the movie files
    print("Writing video...")
    Writer = animation.writers['imagemagick']
    writer = Writer(fps=25, metadata=dict(artist='Sergey Royz'), bitrate=1800)
    ani.save('pulley_free_fall.gif', writer=writer)