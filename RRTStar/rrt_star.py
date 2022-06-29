import rrt_star_wrapper
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from obstacle_handler import ObstacleHandler
from obstacle_handler import Obstacle
from pathlib import Path

def main():
    """A debug script for the rrt star planner.

    This script will solve the rrt star problem in a
    standalone simulation and visualize the results or raise an error if a
    path is not found.
    """
    conds = {
        'start': [140, 60],
        'end': [180, 60],
        # obstacles initial position
        'obstacles': [
            [158, 58, 162, 62],
            [170,55,175,60],
            [165,60,170,65],
        ],
    }  # paste output from debug log

    # Create a Obstacle_handler object
    obs_handler = ObstacleHandler(step_size=1.0)
    obs1 = conds['obstacles'][0]
    obs2 = conds['obstacles'][1]
    obs3 = conds['obstacles'][2]
    
    # Moves obstacle 2 units to the left every timestep for 10 timesteps, then moved 1 unit down for 10 timesteps
    obs = Obstacle(obs1, is_dynamic=True, movement_list=[[-0.5,0], [0.5,0], [0,-1]], step_list=[10, 10, 5])  
    obs_handler.add_obstacle(obs)
    
    # Moves obstacle 1 units to the up every timestep for 10 timesteps, then moved 1 unit down for 20 timesteps
    obs = Obstacle(obs2, is_dynamic=True, movement_list=[[0,1], [0,-1], [0,1], [0,-1]], step_list=[10, 5, 10, 20])
    obs_handler.add_obstacle(obs)

    # static obstacle
    obs = Obstacle(obs3, is_dynamic=False)
    obs_handler.add_obstacle(obs)

    initial_conditions = {
        'start': np.array(conds['start']),
        'end': np.array(conds['end']),
        'obs': np.array(conds['obstacles'])
    }

    hyperparameters = {
        "step_size": 1.0,
        "max_iterations": 16000,
        "end_dist_threshold": 1.0,
        "obstacle_clearance": 1.0,
        "lane_width": 10.0,
    }

    end = conds['end']

    # simulation config
    sim_loop = 100
    area = 20.0  # animation area length [m]
    show_animation = True
    total_time = 0
    for i in range(sim_loop):
        print("Iteration: {}".format(i))
        start_time = time.time()

        # Update the initial conditions
        obs_handler.transform()
        initial_conditions['obs'] = obs_handler.get_obstacles()[0]
        
        result_x, result_y, success = \
            rrt_star_wrapper.apply_rrt_star(initial_conditions, hyperparameters)
        end_time = time.time() - start_time
        print("Time taken: {}".format(end_time))
        total_time += end_time

        if success:
            initial_conditions['start'] = np.array([result_x[1], result_y[1]])
        else:
            print("Failed unexpectedly")

        if np.hypot(result_x[1] - end[0], result_y[1] - end[1]) <= 1.0:
            print("Goal")
            break

        if show_animation:  # pragma: no cover
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None]
            )
            ax = plt.gca()
            (obs, dynamic) = obs_handler.get_obstacles()
            for o, d in zip(obs, dynamic):
                if d:
                    rect = patch.Rectangle((o[0], o[1]),
                                        o[2] - o[0],
                                        o[3] - o[1], facecolor = 'r')
                else:
                    rect = patch.Rectangle((o[0], o[1]),
                                        o[2] - o[0],
                                        o[3] - o[1], facecolor = 'b')
                ax.add_patch(rect)
            plt.plot(result_x[1], result_y[1], "og")
            plt.plot(end[0], end[1], "or")
            if success:
                plt.plot(result_x[1:], result_y[1:], ".r")
                plt.plot(result_x[1], result_y[1], "vc")
                plt.xlim(result_x[1] - area, result_x[1] + area)
                plt.ylim(result_y[1] - area, result_y[1] + area)
            plt.xlabel("X axis")
            plt.ylabel("Y axis")
            plt.grid(True)
            plt.pause(0.1)
            Path("img/frames").mkdir(parents=True, exist_ok=True)
            plt.savefig("img/frames/{}.png".format(i))

    print("Finish")
    print("Average time per iteration: {}".format(total_time/i))
    if show_animation:  # pragma: no cover
        plt.grid(True)
        plt.pause(1)
        plt.show()


if __name__ == '__main__':
    main()
